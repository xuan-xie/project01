from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from read_num.models import ReadNum,GetReadNum
#博客类型的类
class BlogType(models.Model):
    type_name = models.CharField('博客类型', max_length=40)

    def __str__(self):
        return self.type_name
    class Meta:

        verbose_name='博客类型'
        verbose_name_plural=verbose_name

# 博客类
class Blog(models.Model,GetReadNum):

    title = models.CharField('标题', max_length=40)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    #内容字段
    content = RichTextUploadingField('内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creat_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='博客列表'
        verbose_name_plural = verbose_name
        ordering=['-creat_time']