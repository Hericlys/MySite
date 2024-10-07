
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django import forms
from django.forms.widgets import TextInput
from .models import Post, Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    color = forms.CharField(widget=TextInput(attrs={'type': 'color'}))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'author', 'category', 'published', 'created_at', 'updated_at']
    list_filter = ['published', 'created_at', 'category']
    list_editable = ['published',]
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ['content',]
