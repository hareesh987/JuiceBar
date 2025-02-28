"""
URL configuration for juiceBar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from myapp import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('myapp.urls')),
    path('login/',views.login_user,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_user,name='logout'),
    path("forgot-password/", views.forgot_password, name="forgot"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset"),
    path('signupotp/', views.otp_verification, name='otp_verification'),
    path('upload/', views.upload_image, name='upload'),
    path('gallery/', views.gallery, name='gallery'),
    #path('login/', views.login, name='login'),
    #path('home/', views.home, name='home'),
    #path('signup/', views.signup, name='signup'),
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
