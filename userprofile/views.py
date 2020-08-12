import logging
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.template.loader import TemplateDoesNotExist, get_template
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext

from lib.helpers import settings_text
from authorization.permissions import ACCESS
from .viewbase import UserProfileView


logger = logging.getLogger('aplus.userprofile')


class CustomLoginView(LoginView):
    """This login view class extends the default Django login class and
    overrides some of the default settings. Namely, the template and its context."""

    template_name = "userprofile/login.html"
    redirect_authenticated_user = True
    # Redirecting authenticated users enables "social media fingerprinting"
    # unless images are hosted on a different domain from the Django app.
    extra_context = {
        'shibboleth_login': 'shibboleth_login' in settings.INSTALLED_APPS,
        'mooc_login': 'social_django' in settings.INSTALLED_APPS,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The following template context parameters can not be defined in
        # the class variable extra_context because they require that Django
        # translations are active. That is, there must be an HTTP request so
        # that the language can be defined. There is no request in the code
        # in the class level, but there is a request when this method is called
        # (self.request).
        context.update({
            'login_title_text': settings_text('LOGIN_TITLE_TEXT'),
            'login_body_text': settings_text('LOGIN_BODY_TEXT'),
            'login_button_text': settings_text('LOGIN_BUTTON_TEXT'),
            'shibboleth_title_text': settings_text('SHIBBOLETH_TITLE_TEXT'),
            'shibboleth_body_text': settings_text('SHIBBOLETH_BODY_TEXT'),
            'shibboleth_button_text': settings_text('SHIBBOLETH_BUTTON_TEXT'),
            'mooc_title_text': settings_text('MOOC_TITLE_TEXT'),
            'mooc_body_text': settings_text('MOOC_BODY_TEXT'),
        })
        return context


def try_get_template(name):
    try:
        return get_template(name)
    except TemplateDoesNotExist:
        logger.info("Template %s not found", name)
        return None


class PrivacyNoticeView(UserProfileView):
    access_mode=ACCESS.ANONYMOUS
    template_name="userprofile/privacy.html"

    def get_common_objects(self):
        super().get_common_objects()
        lang = "_" + get_language().lower()
        key = make_template_fragment_key('privacy_notice', [lang])
        privacy_text = cache.get(key)
        if not privacy_text:
            template_name = "privacy_notice{}.html"
            template = try_get_template(template_name.format(lang))
            if not template and len(lang) > 3:
                template = try_get_template(template_name.format(lang[:3]))
            if not template:
                logger.warning("No localized privacy notice for language %s", lang)
                template = try_get_template(template_name.format(''))
            if not template:
                logger.error("No privacy notice at all!")

            privacy_text = template.render() if template else _("No privacy notice. Please notify administration!")
            cache.set(key, privacy_text)
        self.privacy_text = privacy_text
        self.note("privacy_text")


class AccessibilityStatementView(UserProfileView):
    access_mode = ACCESS.ANONYMOUS
    template_name="userprofile/accessibility.html"

    def get_common_objects(self):
        super().get_common_objects()
        lang = "_" + get_language().lower()
        key = make_template_fragment_key('accessibility_statement', [lang])
        accessibility_statement = cache.get(key)
        # TODO: refactor to a helper function
        if not accessibility_statement:
            local_template_name = "institution_accessibility_text{}.html"
            local_template = try_get_template(local_template_name.format(lang))
            if not local_template and len(lang) > 3:
                local_template = try_get_template(local_template_name.format(lang[:3]))
            if not local_template:
                logger.warning("No localized accessibility statement for language %s", lang)
                local_template = try_get_template(local_template_name.format(''))
            if not local_template:
                logger.error("No local accessibility content at all!")

            local_accessibility_statement = local_template.render() if local_template else gettext("No local accessibility statement. Please notify the site's owner!")

            system_template_name = "accessibility_issues{}.html"
            system_template = try_get_template(system_template_name.format(lang))
            if not system_template and len(lang) > 3:
                system_template = try_get_template(system_template_name.format(lang[:3]))
            if not system_template:
                logger.warning("No localized system accessibility content for language %s", lang)
                system_template = try_get_template(system_template_name.format(''))
            if not system_template:
                logger.error("No system accessibility content at all!")

            system_accessibility_statement = system_template.render() if system_template else gettext("No system-wide accessibility statement found.")

            accessibility_statement = local_accessibility_statement + system_accessibility_statement
            cache.set(key, accessibility_statement)
        self.accessibility_statement = accessibility_statement
        self.note("accessibility_statement")


class ProfileView(UserProfileView):
    template_name = "userprofile/profile.html"
