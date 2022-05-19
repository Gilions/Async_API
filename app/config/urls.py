from config import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import mimetypes

    import debug_toolbar

    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
