from django.contrib import admin
from django.urls import path
from app import views
app_name='app'
urlpatterns = [
    path('',views.index,name="index"),
    path('login',views.login_1,name="login"),
    path('logout',views.logout_1,name="logout"),
    path('upload',views.upload_1,name="upload"),
    path('view',views.view_1,name="view"),
]
