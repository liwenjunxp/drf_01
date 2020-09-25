from rest_framework import serializers
from api import models

# 单表查询
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'

# 一对多外键连表查询
class ModuleSerializer(serializers.ModelSerializer):
    cname = serializers.CharField(source='course.title')  #取course对象的title属性
    level_text = serializers.CharField(source='get_level_display')  #显示level字段的中文
    class Meta:
        model = models.Module
        # fields = '__all__'  #显示所有字段
        # exclude = ['course']  #排除course字段
        # fields = ['id','name']  #只显示id和name字段
        # fields = ['id','name','level','cname']  #显示id、name、level以及cname字段的名称（即连表查询）
        fields = ['id','name','level_text','cname']  #显示id、name、level字段的中文名称以及cname字段的名称
        """
        说明：
        当在浏览器中输入：http://127.0.0.1:8000/api/v3/module/?format=json时，输出：
        [{"id":1,"name":"数据类型","level_text":"初级","cname":"python"},{"id":2,"name":"网络编程","level_text":"初级","cname":"python"}]
        """

class ModuleNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = '__all__'

class ModuleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = '__all__'

#多对多连表查询
class VideoSetSerializer(serializers.ModelSerializer):
    tag_text = serializers.SerializerMethodField()
    class Meta:
        model = models.Video
        fields = ['id','title','vid','tag','tag_text']

    def get_tag_text(self,obj):  #钩子函数，就是为了返回tag_text的内容。这里的obj就是video表中的一行数据
        tag_list =  obj.tag.all()
        print(tag_list)  #输出如<QuerySet [<Tag: Tag object (1)>, <Tag: Tag object (2)>]>
        # return [row.caption for row in tag_list ]  #tag_text字段里只显示tag表中的caption
        return [{'id':row.id,'caption':row.caption} for row in tag_list]  #tag_text字段里显示tag表中的id和caption



