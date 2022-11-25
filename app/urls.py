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
    #path('edit',views.edit_1,name="edit"),
    #path('update/<int:id>',views.update_1,name="update"),
    #path('delete', views.delete_1,name='delete'),
]
