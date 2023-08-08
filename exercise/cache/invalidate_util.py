from __future__ import annotations
from typing import Callable, Dict, Generator, Iterable, List, Optional, Tuple, TYPE_CHECKING, Union

from course.models import CourseModule, CourseInstance
from deviations.models import SubmissionRuleDeviation
from lib.request_globals import OptInGlobal
from notification.models import Notification
from userprofile.models import UserProfile
from ..models import BaseExercise, Submission, RevealRule, LearningObject, LearningObjectCategory

if TYPE_CHECKING:
    from .content import CachedContentData, ExerciseEntry, ModuleEntry


class CachedContents(OptInGlobal):
    """An opt-in in-memory cache for database signal based cache invalidators"""
    instances: Dict[int, Optional[CachedContentData]]
    modules: Dict[int, ModuleEntry]
    exercises: Dict[int, ExerciseEntry]

    def init(self):
        self.instances = {}
        self.modules = {}
        self.exercises = {}

    def _load_instance(self, instance_id: int):
        from .content import CachedContentData # pylint: disable=import-outside-toplevel
        try:
            instance_entry = CachedContentData.get(instance_id)
        except CourseInstance.DoesNotExist:
            self.instances[instance_id] = None
            return

        self.instances[instance_id] = instance_entry
        for module in instance_entry.modules:
            self.modules[module.id] = module
        self.exercises.update(instance_entry.exercise_index)

    def get_instance(self, instance_id: int) -> Optional[CachedContentData]:
        """Gets the instance entry for the instance. May return None
        if the instance was deleted"""
        if instance_id not in self.instances:
            self._load_instance(instance_id)
        return self.instances[instance_id]

    def get_exercise(self, lobj: LearningObject) -> Optional[ExerciseEntry]:
        """Gets the exercise entry for the learning object. May return None
        if the learning object, its module or its instance was deleted"""
        if lobj.id not in self.exercises:
            self._load_instance(lobj.course_module.course_instance_id)
        entry = self.exercises.get(lobj.id)
        return entry

    def get_module(self, module: CourseModule) -> Optional[ModuleEntry]:
        """Gets the module entry for the course module. May return None
        if the course module or its instance was deleted"""
        if module.id not in self.modules:
            self._load_instance(module.course_instance_id)
        entry = self.modules.get(module.id)
        return entry


def exercise_entry_ancestors(entry: Optional[Union[ExerciseEntry, LearningObject]]) -> Generator[int, None, None]:
    while entry is not None:
        yield entry.id
        entry = entry.parent


def learning_object_ancestors(lobj: LearningObject) -> Generator[int, None, None]:
    cached = CachedContents()
    entry = cached.get_exercise(lobj)
    if entry is None:
        yield lobj.id
        return

    yield from exercise_entry_ancestors(entry)
    # Invalidate new parent as well if it changed
    if entry.id != lobj.parent_id and lobj.parent is not None:
        entry = cached.get_exercise(lobj.parent)
        if entry is None:
            yield lobj.parent_id
        else:
            yield from exercise_entry_ancestors(entry)


def learning_object_modules(lobj: LearningObject) -> Generator[int, None, None]:
    cached = CachedContents()
    entry = cached.get_exercise(lobj)
    if entry is None:
        yield lobj.course_module_id
        return

    yield entry.module.id
    # Invalidate new module as well if it changed
    if entry.module.id != lobj.course_module_id :
        yield lobj.course_module_id


def category_learning_objects(generator: Callable[[ExerciseEntry], Iterable[int]]):
    def inner(category: LearningObjectCategory) -> Generator[int, None, None]:
        cached = CachedContents()
        cached_instance = cached.get_instance(category.course_instance_id)
        if cached_instance is None:
            return

        seen = set()
        for exercise in cached_instance.exercise_index.values():
            if exercise.category_id == category.id:
                for model_id in generator(exercise):
                    if model_id in seen:
                        continue
                    seen.add(model_id)
                    yield model_id
    return inner


def module_learning_objects(module: CourseModule):
    cached = CachedContents()
    entry = cached.get_module(module)
    if entry is None:
        for lobj in LearningObject.bare_objects.filter(course_module=module).only("id"):
            yield lobj.id
    else:
        for exercise_entry in entry.get_descendants():
            yield exercise_entry.id


ModelTypes = Union[Submission, Notification, RevealRule, SubmissionRuleDeviation]
def model_user_ids(obj: ModelTypes) -> List[int]:
    if isinstance(obj, Submission):
        submitters = obj.submitters.all()
    elif isinstance(obj, Notification):
        submitters = [obj.recipient]
    elif isinstance(obj, RevealRule):
        exercise = model_exercise(obj)
        if exercise is None:
            return []
        submitters = UserProfile.objects.filter(submissions__exercise=exercise).distinct()
    else:
        submitters = UserProfile.objects.filter(
            submissions__exercise=obj.exercise,
            submissions__submitters=obj.submitter
        ).distinct()
        # We need to invalidate for the submitter even if they haven't submitted anything
        if not submitters:
            submitters = [obj.submitter]
    return [profile.user.id for profile in submitters]


def model_exercise(obj: ModelTypes) -> Optional[LearningObject]:
    if isinstance(obj, Notification):
        if obj.submission is None:
            return None
        exercise = obj.submission.exercise
    # pre_delete hook sets obj.exercise
    elif isinstance(obj, RevealRule) and not hasattr(obj, "exercise"):
        try:
            exercise = BaseExercise.objects.get(submission_feedback_reveal_rule=obj)
        except BaseExercise.DoesNotExist:
            return None
    else:
        exercise = obj.exercise
    return exercise


def model_module_id(obj: ModelTypes):
    exercise = model_exercise(obj)
    if exercise is None:
        return
    yield exercise.course_module_id


def model_instance_id(obj: ModelTypes):
    if isinstance(obj, Notification) and obj.course_instance_id:
        instance_id = obj.course_instance_id
    else:
        exercise = model_exercise(obj)
        if exercise is None:
            return
        instance_id = exercise.course_module.course_instance_id

    yield instance_id


def model_exercise_ancestors(obj: ModelTypes) -> Generator[int, None, None]:
    exercise = model_exercise(obj)
    if exercise is None:
        return
    yield from learning_object_ancestors(exercise)


def exercise_siblings_confirms_the_level(lobj: LearningObject) -> Generator[int, None, None]:
    cached = CachedContents()
    exercise = cached.get_exercise(lobj)
    if exercise is None:
        return

    if exercise.parent is not None:
        parent = exercise.parent
    else:
        parent = exercise.module

    for entry in parent.children:
        if entry.confirm_the_level:
            yield entry.id

    parent = None
    if lobj.parent_id is not None:
        if exercise.parent is None or exercise.parent.id != lobj.parent_id:
            parent = cached.get_exercise(lobj.parent)
    elif exercise.module.id != lobj.course_module_id:
        parent = cached.get_module(lobj.course_module)

    if parent is not None:
        for entry in parent.children:
            if entry.confirm_the_level:
                yield entry.id


def model_exercise_siblings_confirms_the_level(obj: ModelTypes) -> Generator[int, None, None]:
    exercise = model_exercise(obj)
    if exercise is None:
        return
    yield from exercise_siblings_confirms_the_level(exercise)


def with_user_ids(
        generator: Callable[[ModelTypes], Generator[int, None, None]],
        ):
    def inner(obj: ModelTypes) -> Generator[Tuple[int, int], None, None]:
        user_ids = model_user_ids(obj)
        for model_id in generator(obj):
            for user_id in user_ids:
                yield (model_id, user_id)
    return inner


def m2m_submission_userprofile(generator: Callable[[Submission], Generator[int, None, None]]):
    def inner(
            obj: Union[Submission, UserProfile],
            action: str,
            pk_set: Iterable[int],
            ) -> Generator[Tuple[int, int], None, None]:
        if action not in ('post_add', 'pre_remove'):
            return
        if isinstance(obj, UserProfile):
            submissions = Submission.objects.filter(pk__in=pk_set)
            seen = set()
            for submission in submissions:
                for model_id in generator(submission):
                    if model_id in seen:
                        continue
                    seen.add(model_id)
                    yield (model_id, obj.id)
        else:
            user_ids = model_user_ids(obj)
            for model_id in generator(obj):
                for user_id in user_ids:
                    yield (model_id, user_id)
    return (inner, ["action", "pk_set"])
