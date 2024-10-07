from django.contrib import admin
from .models import Project, Technology
from django import forms
from django.forms.widgets import TextInput


class TechnologyAdminForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = '__all__'

    color = forms.CharField(widget=TextInput(attrs={'type': 'color'}))


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    form = TechnologyAdminForm
    list_display = ['id', 'name', 'color',]
    list_display_links = ['id', 'name',]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published',]
    list_display_links = ['name',]
    list_editable = ['is_published',]
    prepopulated_fields = {'slug': ('name',)}