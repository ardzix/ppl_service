from django.contrib import admin
from ..models import Category, Activity, UserPoint, ActivityLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'point_impact', 'category', 'type', 'code')
    search_fields = ('name', 'category__name', 'type', 'code')

@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = ('user_hash', 'email', 'phone', 'points')
    search_fields = ('user_hash', 'email', 'phone')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'timestamp', 'nonce')
    search_fields = ('user__user_hash', 'activity__name', 'nonce')
