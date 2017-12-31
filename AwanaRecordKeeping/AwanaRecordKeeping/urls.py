"""AwanaRecordKeeping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from Awana import views 
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^CheckInPuggles/', views.CheckInPuggles, name='CheckInPuggles'),
    url(r'^CheckInCubbies/', views.CheckInCubbies, name='CheckInCubbies'),
    url(r'^CheckInSparks/', views.CheckInSparks, name='CheckInSparks'),
    url(r'^CheckInTTGirls/', views.CheckInTTGirls, name='CheckInTTGirls'),
    url(r'^CheckInTTBoys/', views.CheckInTTBoys, name='CheckInTTBoys'),
    url(r'^BookTTBoys/', views.BookTTBoys, name='BookTTBoys'),
    url(r'^BookTTGirls/', views.BookTTGirls, name='BookTTGirls'),
    url(r'^BookSparks/', views.BookSparks, name='BookSparks'),
    url(r'^PointsSparks/', views.PointsSparks, name='PointsSparks'),
    url(r'^PointsTTGirls/', views.PointsTTGirls, name='PointsTTGirls'),
    url(r'^PointsTTBoys/', views.PointsTTBoys, name='PointsTTBoys'),
    url(r'^AwardsSparks/', views.AwardsSparks, name='AwardsSparks'),
    url(r'^AwardsTT/', views.AwardsTT, name='AwardsTT'),
    url(r'^$', views.index, name='index'),
    url(r'^DefaultInfo', TemplateView.as_view(template_name='DefaultInfo.html')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

