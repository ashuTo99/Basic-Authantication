from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.UserRegister.as_view(), name='user.register'),
    path('register2/',views.RegisterUser.as_view(), name='user.register2'),
    path('login/',views.LoginView.as_view(), name='user.login'),


]
