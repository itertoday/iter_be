"""backend URL Configuration

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
from django.urls import path, include
from rest_framework import routers
from api import views
from knox import views as knox_views
from api.views import RequestViewSet, OrderViewSet
from rest_framework import routers
from price.views import PriceViewset


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register('requests', RequestViewSet)
router.register('orders', OrderViewSet)

router.register('pricing', PriceViewset, basename="pricing")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path(r'api/auth/', include('knox.urls')),
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path(r'password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('hello/', views.HelloView.as_view(), name='hello'),
]
