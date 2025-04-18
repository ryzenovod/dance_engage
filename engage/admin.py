from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Dance, UserProfile, Engagement

admin.site.register(Dance)
admin.site.register(UserProfile)
admin.site.register(Engagement)

# Добавляем профиль в админку пользователя
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)