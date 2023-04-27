from django.shortcuts import render
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets,generics
from rest_framework.response import Response
from CustomerApp.models import Custom_user
from CustomerApp.serializer import CustomUserSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import AccessToken
from rest_framework.permissions import IsAuthenticated
from CustomerApp.permission import IsOwnerOrReadOnly
from rest_framework import status
# Create your views here.


class UserCreateApi(generics.CreateAPIView):
    queryset=Custom_user.objects.all()
    serializer_class=CustomUserSerializer

    def get(self,request,*args,**kwargs):
        form=self.serializer_class()
        return render(request,'CustomerApp/registeruser.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        print(request.data)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return render(request,'CustomerApp/registeruser.html',{'form':serializer})



class Usersdetail(APIView):
    def get(self,request):
        data=Custom_user.objects.all()
        serializer=CustomUserSerializer(data, many=True)
        context={'data':serializer.data}
        return render(request,'CustomerApp/alluser.html',context,status=status.HTTP_200_OK)


class UpdateUserApi(APIView):
    authentication_classes=[OAuth2Authentication]
    permission_classes=[IsAuthenticated,IsOwnerOrReadOnly]

    def get_object(self,pk):
        try:
            return Custom_user.objects.get(pk=pk)
        except Custom_user.DoesNotExist:
            msg={'msg':'Record Not Found'}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk):
        print(request.data)
        obj=self.get_object(pk=pk)
        serializer=CustomUserSerializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        obj=self.get_object(pk)
        if obj.user != request.user:
            return Response({'message':'You Dont have the permission to modify this record'},status=status.HTTP_403_FORBIDDEN)
        serializer=CustomUserSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    authentication_classes=[OAuth2Authentication]
    permission_classes=[IsAuthenticated]

    @csrf_exempt
    def post(self,request,*args ,**kwargs):
        token=AccessToken.objects.get(token=request.auth)
        token.delete()   
        return Response({'message':'You are Logged Out'},status=status.HTTP_200_OK)
    
class ForgetUserView(APIView):
    authentication_classes=[OAuth2Authentication]
    permission_classes=[IsAuthenticated]

    def delete(self,request):
        user=request.user
        user.delete()
        return Response({'message':'Account deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
    


