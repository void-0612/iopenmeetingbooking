from django.contrib import admin

from web.models import UserInfo, MeetingRoom,Booking

# Register your models here.
admin.site.register([UserInfo,MeetingRoom,Booking])