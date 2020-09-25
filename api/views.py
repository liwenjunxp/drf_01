from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.versioning import URLPathVersioning


### 获取请求端 url中的版本号 ###
class VersionView(APIView):
    #versioning_class = URLPathVersioning
    def get(self,request,*args,**kwargs):
        print(request.version)
        return Response('...')

### 获取服务端文件内容，并返回给请求端。 ###
class XmlView(APIView):

    def get(self,request,*args,**kwargs):
        with open('abc.xml') as f:
            data = f.read()
        return Response(data)

### 操作数据库 ###
from api import models
from api.ser import CourseSerializer

#手动增删改查
class Sql01View(APIView):

    def get(self,request,*args,**kwargs):
        result = {'status': True, 'data': None, 'error': None}
        queryset = models.Course.objects.all()
        ser = CourseSerializer(instance=queryset,many=True)
        result['data'] = ser.data
        return Response(result)

    def post(self,request,*args,**kwargs):
        """
        1. 获取用户提交的数据 request.data
        2. 校验数据的合法性、序列化
        3. 校验通过save
        4. 不通过则报错
        """
        result = {'status':True,'data':None,'error':None}
        ser = CourseSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(result)
        result['error'] = ser.errors
        return Response(result)

# 独立自动增删改查
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView

class Sql02View(ListAPIView,CreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

 # 统一自动增删改查
from rest_framework.viewsets import ModelViewSet

class Sql03View(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


class Sql04View(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):  #只重写查询全部数据的 list方法，不再查询数据库，而是查询文件。
        with open('abc.xml') as f:
            data = f.read()
        return Response(data)

###################### 以下是对module表进行的操作 ##########################
from api.ser import ModuleSerializer,ModuleNewSerializer,ModuleSetSerializer

class ModuleView(APIView):   #查询所有的数据
    def get(self,request,*args,**kwargs):
        queryset = models.Module.objects.all()

        # for row in queryset:
        #     print(row.id,row.name,row.level,row.get_level_display(),row.course.title)
        """
        说明：
        row.get_level_display()  #显示level字段的中文
        row.course.title   #连表查询row对象的course属性的title属性
        输出结果如下：
        1 数据类型 1 初级 python
        2 网络编程 1 初级 python
        """
        ser = ModuleSerializer(instance=queryset,many=True)
        return Response(ser.data)

class ModuleNewView(RetrieveAPIView,CreateAPIView):   #查询单条数据或增加单条数据
    queryset = models.Module.objects.all()
    serializer_class = ModuleNewSerializer
    """
    说明：
    当在浏览器中输入：http://127.0.0.1:8000/api/v3/module/new/2/?format=json 时，输出：
    {"id":2,"level":1,"name":"网络编程","course":1}
    
    当在Postman中输入：http://127.0.0.1:8000/api/v3/module/new/ 发送POST请求，body为json格式为：
    {"name":"前端开发","level":2,"course":1}，数据库module表中会增加这条数据。
   
    """

class ModuleSetView(ModelViewSet):
    queryset = models.Module.objects.all()
    serializer_class = ModuleSetSerializer
    """"
    说明：
    GET类型请求http://127.0.0.1:8000/api/v3/module/set/ 时，显示所有数据。
    GET类型请求http://127.0.0.1:8000/api/v3/module/set/2/ 时，显示id为2的那条数据。
    
    POST类型请求http://127.0.0.1:8000/api/v3/module/set/ 时，会增加一条数据。
    
    PUT类型请求http://127.0.0.1:8000/api/v3/module/set/4/ 时，
    如果body设为json数据{"name":"dango框架之drf","level":3,"course":1} 更新id为4的那条数据。
    
    PATCH类型请求http://127.0.0.1:8000/api/v3/module/set/4/ 时，
    如果body设为json数据{"name":"dango框架} 只更新id为4的那条数据中name字段。
    
    """
    #下面来实现像PATCH那样的局部更新功能，以便了解PATCH的原理：
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')  #获取行号
        model_object = models.Module.objects.filter(id=pk).first()
        ser = ModuleSetSerializer(instance=model_object,data=request.data,many=False,partial=True) #partial表示局部更新
        if ser.is_valid():
            ser.save()
            return Response('成功')
        return Response(ser.errors)

###################### 以下是对 video 表进行的操作 ##########################
from api.ser import VideoSerializer,VideoSetSerializer

class VideoView(ListAPIView,RetrieveAPIView):  #查询video表中所有数据或单条数据
    queryset = models.Video.objects.all()
    serializer_class = VideoSerializer


class VideoViewSet(ModelViewSet):
    queryset = models.Video.objects.all()
    serializer_class = VideoSetSerializer
    """
    说明：
    当POST请求http://127.0.0.1:8000/api/v3/video_set/ 时，
    如果body设为json数据 {"title":"loggin模块","vid":"aacddk123kfl","tag":[1,2]}  # tag的值是id为1和2的标签，
    则会在video表中增加一条数据。
    """

