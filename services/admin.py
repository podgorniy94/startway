from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import Post, Testimonial, Page, Email


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_on_top = True
    list_display = ('id', 'title', 'created_at', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'get_photo')
    fields = ('title', 'slug', 'created_at', 'banner_published', 'content', 'photo', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50"')
        return '-'

    get_photo.short_description = 'Фотография'


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('created_at', )
    fields = ('name', 'comment', 'created_at')


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title',)
    readonly_fields = ('inc',)
    # fields = ('title', 'slug')


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')


admin.site.register(Post, PostAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Email, EmailAdmin)
