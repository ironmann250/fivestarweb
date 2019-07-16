"""fivestarweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from backend import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^add/', views.add),
    url(r'^search/', views.search),
    url(r'^adminpg/', views.adminpg),
    url(r'^added/(?P<packagenum>.*)', views.added),
    url(r'^package/(?P<packagenum>.*)', views.package),
    url(r'^render_ticket/(?P<packagenum>.*\.jpg)',views.renderTicket),
    url(r'^login/$',auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout/$',auth_views.logout, {'next_page': '/'}),
]
media_urls=[static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)]
for url in media_urls:
	urlpatterns+=url