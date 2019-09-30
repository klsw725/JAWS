"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework import routers
from knox import views as knox_views

import api.api

router = routers.DefaultRouter()
router.register('upload', api.api.ImagesViewSet)
router.register('signup', api.api.SignupViewSet)
router.register('login', api.api.LoginViewSet)
router.register('user', api.api.UserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r"^api/logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
