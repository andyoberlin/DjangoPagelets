from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('DjangoPagelets.views.applications.public',
    url(r'^$', 'Home.Application.renderAction')
)

'''
urlpatterns += patterns('DjangoPagelets.views.applications.admin',
    
)
'''

urlpatterns += patterns('', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static_site/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0]}),
    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/usr/local/lib/python2.6/dist-packages/django/contrib/admin/media'})
)
