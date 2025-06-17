from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'phone', 'created_by')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'student_id', 'phone')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'