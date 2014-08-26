from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from dss import settings

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v2/', include('api.urls', namespace='api_v2')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('user_sessions.urls', 'user_sessions')),
    (r'^channel\.html$', TemplateView.as_view(template_name='boiler/fb_channel.html')),
    (r'^privacy\.html$', TemplateView.as_view(template_name='boiler/privacy.html')),
    (r'^robots\.txt', TemplateView.as_view(template_name='boiler/robots.txt')),
    (r'^tos\.html$', TemplateView.as_view(template_name='boiler/tos.html')),
    (r'^test\.html$', TemplateView.as_view(template_name='boiler/test.html')),
    (r'^500', 'django.views.defaults.server_error'),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/', include('allauth.urls')),
    (r'^avatar/', include('avatar.urls')),
    url(r'^', include('spa.urls')),
)
handler500 = 'spa.views.debug_500'

if settings.DEBUG:
    from django.views.static import serve

    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns(
            '',
            (r'^%s(?P<path>.*)$' % _media_url,
             serve,
             {'document_root': settings.MEDIA_ROOT}))
    del (_media_url, serve)
