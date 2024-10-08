from django.contrib import admin
from .models import Project, Technology
from django import forms
from django.forms.widgets import TextInput




@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    list_display_links = ['id', 'name',]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published',]
    list_display_links = ['name',]
    list_editable = ['is_published',]
    prepopulated_fields = {'slug': ('name',)}