from django.contrib import admin
from .models import Blog,BlogType
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','author','get_read_num','creat_time']




class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name',]

admin.site.register(BlogType,BlogTypeAdmin)
admin.site.register(Blog,BlogAdmin)