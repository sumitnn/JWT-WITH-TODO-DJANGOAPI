from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializer import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.reverse import reverse
from .models import Todo
# home view 
class HomeApiView(APIView):
    def get(self,request):
    
        data={
            'Sign-Up':reverse('signup',request=request),
            # 'Confirm-Email':reverse('confirm-email',args=[token],request=request),
            'Login':reverse('login',request=request),
            'Home':reverse('home',request=request),
            'Token-Generator':reverse('token_obtain_pair',request=request),
            'Token-Refresh':reverse('token_refresh',request=request),
            'Create-Todo':reverse('create-todo',request=request)
        }
        return Response(data)

# Create your views here.
class CreateTodoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
       user=User.objects.get(email=request.user.email)
       data=Todo.objects.filter(user=user)
       serializer=TodoSerializer(data,many=True)
       return Response({'success':True,'data':serializer.data})


    def post(self,request):
        if request.user.email_activated:
            data=request.data
            user=User.objects.get(email=request.user.email)
            serializer=TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({'success': True,'message':serializer.data,'status':status.HTTP_201_CREATED})
            return Response({'success': False,'message':serializer.errors})
        return Response({'success': False,'message':'User Email Is Not Varified'})




