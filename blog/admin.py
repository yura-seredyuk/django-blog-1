from blog.models import Post, Comment
from django.contrib import admin



# Register your models here.

# admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date')
    list_filter = ('author', 'create_date', 'publish_date')
    search_fields = ('title', 'text')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_date'
    ordering = ['author', 'publish_date']

admin.site.register(Post, PostAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)