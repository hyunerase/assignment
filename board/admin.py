from django.contrib import admin
from .models import Post

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    readonly_field = ('date',)
admin.site.register(Post, BlogAdmin)