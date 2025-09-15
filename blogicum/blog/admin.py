from django.contrib import admin

from .models import Category, Post, Location, Comment

admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {"slug": ("title",)}


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category',
                    'location', 'pub_date', 'is_published')
    list_filter = ('is_published', 'pub_date', 'category')
    search_fields = ('title', 'text')
    date_hierarchy = 'pub_date'
    autocomplete_fields = ('author', 'category', 'location')


admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
