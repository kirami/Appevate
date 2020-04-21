from django.contrib import admin

from .models import User
from django.contrib.admin.sites import AdminSite

class UserAdmin(admin.ModelAdmin):
	list_display = ['id',  'email', 'redeem_threshold']
	search_fields = [  'email']

#AdminSite.app_index_template = "admin/my_index.html"
admin.site.register(User, UserAdmin)
