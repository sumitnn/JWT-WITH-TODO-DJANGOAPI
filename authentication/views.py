from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializer import SignupSerializer,LoginupSerializer
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from main.models import Todo
from main.serializer import TodoSerializer
# mytoken custom 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import uuid

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email']=user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# function send_email  
def send_email(useremail):
    user=User.objects.get(email=useremail)
    if user :
        code=uuid.uuid4()
        print(code)
        user.emailtoken=code
        user.save()
        text="http://127.0.0.1:8000/api/confirm-email/"+str(code)+"/"
        print(text)
    print("invalid user")


#confirm email view
class ConfirmEmailView(APIView):
    def get(self, request,token):
        print(token)
        user=User.objects.get(emailtoken=token)
        print(user)
        if user.emailtoken == token:
            user.email_activated=True
            user.save()
            return Response({'success': True,'status':status.HTTP_201_CREATED})
        print('token error')




# Create your views here.

class SignupView(APIView):
   
    def post(self, request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            send_email(data.get('email'))

            return Response({'success': True,'data':serializer.data,'status':status.HTTP_201_CREATED,'message':'Activation For Email is Sending in Your EMAIL'})
        return Response({'success': False,'data':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})

class LoginView(APIView):

    def post(self, request):

        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(username=email, password=password)
        if user and user.email_activated:
            return Response({'success': True,'message':'Successfully Login ','status':status.HTTP_201_CREATED})
        return Response({'success': False,'message':'Invalid Credentials ','status':status.HTTP_400_BAD_REQUEST})


class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.email_activated:
            data=Todo.objects.all()
            serializer=TodoSerializer(data,many=True)
            return Response({'success': True,'message':serializer.data,'status':status.HTTP_201_CREATED})
        return Response({'success': False,'message':'User Email Is Not Varified'})