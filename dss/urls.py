from django.conf.urls import patterns, include, url
from django.contrib import admin
from dss import settings

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    url(r'^', include('spa.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/', include('allauth.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    from django.views.static import serve

    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % _media_url,
             serve,
                 {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)