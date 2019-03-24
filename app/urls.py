from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.home, name='signup'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)