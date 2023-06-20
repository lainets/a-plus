import pstats

try:
    import cProfile as profile
except ImportError:
    import profile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import django
from django.conf import settings
from django.http import HttpResponse

class ProfilerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def can(self, request):
        return settings.DEBUG and 'prof' in request.GET

    def __call__(self, request):
        if self.can(request):
            self.profiler = profile.Profile()

            response = self.profiler.runcall(self.get_response, request)

            self.profiler.create_stats()
            if 'download' in request.GET:
                import marshal

                output = marshal.dumps(self.profiler.stats)
                response = HttpResponse(
                    output, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment;' \
                                                  ' filename=view.prof'
                response['Content-Length'] = len(output)
            else:
                io = StringIO()
                stats = pstats.Stats(self.profiler, stream=io)

                stats.strip_dirs().sort_stats(request.GET.get('sort', 'time'))
                stats.print_stats(int(request.GET.get('count', 100)))

                response = HttpResponse('<pre>%s</pre>' % io.getvalue())

            return response

        return self.get_response(request)
