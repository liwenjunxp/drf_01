from django.db import models


class Tag(models.Model):
    caption = models.CharField(verbose_name='标签',max_length=32)

class Course(models.Model):
    title = models.CharField(verbose_name='课程名称',max_length=32)

class Module(models.Model):
    name = models.CharField(verbose_name='模块名称',max_length=32)
    course = models.ForeignKey(verbose_name='课程',to='Course',on_delete=models.CASCADE)

class Video(models.Model):
    title = models.CharField(verbose_name='视频名称',max_length=32)
    vid = models.CharField(verbose_name='保利威视频ID',max_length=64)
    tag = models.ManyToManyField(verbose_name='标签',to='Tag')
