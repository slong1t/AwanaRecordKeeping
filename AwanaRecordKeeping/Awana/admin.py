from django.contrib import admin

# Register your models here.
from .models import Clubber, MeetingNight, ClubPoints, HandBookPoint
class MeetingNightAdmin(admin.ModelAdmin):
    filter_horizontal = ('attendees',)

admin.site.register(Clubber)
admin.site.register(ClubPoints)
admin.site.register(MeetingNight,MeetingNightAdmin)
admin.site.register(HandBookPoint)
