from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .models import Doctor, Student, Level

admin.site.unregister(Group)


class BaseUserAdminCreate(UserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('full_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(Doctor)
class DoctorAdmin(BaseUserAdminCreate):
    list_display = ('full_name', 'email', 'subject', 'is_staff')
    fieldsets = BaseUserAdminCreate.fieldsets + (
        (_('Doctor Information'), {'fields': ('subject',)}),
    )
    add_fieldsets = BaseUserAdminCreate.add_fieldsets + (
        (_('Doctor Information'), {'fields': ('subject',)}),
    )

@admin.register(Student)
class StudentAdmin(BaseUserAdminCreate):
    list_display = ('full_name', 'email', 'level', 'id_number', 'is_staff')
    fieldsets = BaseUserAdminCreate.fieldsets + (
        (_('Student Information'), {'fields': ('level', 'id_number')}),
    )
    add_fieldsets = BaseUserAdminCreate.add_fieldsets + (
        (_('Student Information'), {'fields': ('level', 'id_number')}),
    )
    list_filter = []


@admin.register(Level)
class LevelAdmin (admin.ModelAdmin) : 
    list_display = ['name', 'created_at', 'id']
    search_fields = ['name']