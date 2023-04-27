from django.urls import path, include
from CustomerApp.views import UserCreateApi,LogoutView,ForgetUserView,Usersdetail,UpdateUserApi


urlpatterns = [
    path('signup/',UserCreateApi.as_view(),name='signup_url'),
    path('logout/',LogoutView.as_view(),name='logout_url'),
    path('password_reset/',include('django_rest_passwordreset.urls',namespace='password_reset')),
    path('forget_user/',ForgetUserView.as_view(),name='forget_user'),
    path('htmlrender/',Usersdetail.as_view(),name='alluserdata'),
    path('update/<int:pk>/',UpdateUserApi.as_view(),name='updateapi_url')
    
]