"""gear_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from store.views import LandingPageView, SignupView
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # parent store url
    path('store/',include('store.urls', namespace='store')),

    # landing page
    path('', LandingPageView.as_view(), name='landing_page'),

    # sign in and sign up
    path('sign_in/', LoginView.as_view(), name='sign_in_page'),
    path('sign_up/', SignupView.as_view(), name='sign_up_page'),
    path('logout/', LogoutView.as_view(), name='log_out_page'),
    
    # password reset flow urls
    path('password-reset/', PasswordResetView.as_view(), name='password_reset_view'),
    path('passowrd_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('passowrd_reset_complete/', PasswordResetCompleteView.as_view(), name='passowrd_reset_complete'),
    
]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)