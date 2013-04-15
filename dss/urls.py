from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from dss import settings

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    (r'^channel\.html$', TemplateView.as_view(template_name='boiler/fb_channel.html')),
    (r'^privacy\.html$', TemplateView.as_view(template_name='boiler/privacy.html')),
    (r'^robots\.txt', TemplateView.as_view(template_name='boiler/robots.txt')),
    (r'^tos\.html$', TemplateView.as_view(template_name='boiler/tos.html')),
    (r'^test\.html$', TemplateView.as_view(template_name='boiler/test.html')),
    (r'^500', 'django.views.defaults.server_error'),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/', include('allauth.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('spa.urls')),
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