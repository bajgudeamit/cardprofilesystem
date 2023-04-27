from django.contrib import admin
from CustomerApp.models import Custom_user
# Register your models here.


class CustomAdmin(admin.ModelAdmin):
    list_display=['address','phone_no','profile_pic']

admin.site.register(Custom_user,CustomAdmin) 
