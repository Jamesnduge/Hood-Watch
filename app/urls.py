from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.signup, name='signup'),
    url(r'^accounts/login/$', views.Login, name='login'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)