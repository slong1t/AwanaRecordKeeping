from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^AwanaRecordKeeping/', include('AwanaRecordKeeping.urls')),
    url(r'^admin/', admin.site.urls),
]