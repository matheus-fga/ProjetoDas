from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views

import accounts.views
import photos.views

urlpatterns = patterns('',
					    url(r'^admin/', include(admin.site.urls)),
                        url(r'^$', accounts.views.index, name='home'),
                        url(r'^signup/$', accounts.views.signup, name='signup'),
                        url(r'^signin/$', accounts.views.signin, name='signin'),
                        url(r'^photos/$', photos.views.image_upload, name='photos'),
                        url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
			  )


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)