from django.shortcuts import render, HttpResponse, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.models import Registerdetail
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import io
import asyncio
from pangres import upsert
from sqlalchemy.ext.asyncio import create_async_engine
from django.core.files import File
from django.core.management.base import BaseCommand
from app.models import pangresdata
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def index(request):
    print(request)
    print(request.method)
    if request.method =='POST':
        print("post start")
        your_name=request.POST['name']
        your_email=request.POST['email']
        password=request.POST['psw1']
        password2=request.POST['psw2']
        myuser = User.objects.create_user(your_name,your_email,password)
        myuser.save()
        print("post done")
        return redirect("app:login")

    else:
        print("get")
        return render(request,'index.html')
        


def login_1(request):
    if request.method =='POST':
        username=request.POST['email_login']
        password=request.POST['psw_login']
        user = authenticate(username =username, password =password)
        print(username)
        print(password)
        if user is not None:
            print(user,"Login page")
            login(request, user)
            return render(request,"logout.html")
        return redirect("app:login")

    else:
        return render(request,"login.html")


def logout_1(request):
    if request.method == 'POST':
        #id=request.POST['Id']
        #name=request.POST['Student_name']
        #marks=request.POST['Student_Mark']
        #grade=request.POST['Grade']
        #objs  = Studentdetail.objects.all()
        #print(objs)
        #pd.DataFrame(objs).to_excel('student.xlsx')

        #file= request.POST.get('submit')
        #my_file = request.FILES['myfile']
        #wb = openpyxl.load_workbook(my_file)
        #worksheet = wb["Sheet1"]
        #print(worksheet)
        #obj = Studentdetail.objects.create(myfile=file)
        #path = myfile.
        
        #print(myfile)

        #df=tmp_data.to_sql(name='studentdata',con=engine,index=False,if_exists='append')
        #print(df)
        #with engine.connect() as con:
            #con.execute("ALTER TABLE studentdata ADD PRIMARY KEY (Id);")
            #f.set_index(['Id'], inplace = True, drop = False)
        #for Id,name,mark,grade in zip(tmp_data.Id,tmp_data.Student_name,tmp_data.Student_Mark,tmp_data.Grade):
            #model=Studentdetail(Id=Id,Student_name=name,Student_Mark=mark,Grade=grade)
            #model.save()
        #obj=Studentdetail(id=tmp_data,name=tmp_data,marks=tmp_data,grade=tmp_data,)
        #obj.save()
 
        #products = [
            #Studentdetail(
                #Id = tmp_data.ix[row]['Id'], 
                #Student_name = tmp_data.ix[row]['Student_name'],
                #Student_Mark = tmp_data.ix[row]['Student_Mark'],
                #Grade = tmp_data.ix[row]['Grade'],
                    
                    #for row in tmp_data['ID']
                   #]
        #print('productrs',products)
        #Studentdetail.objects.bulk_create(products)
        #xlrd.open_workbook(filename)
        #document = FileUpload.objects.create(file=filename)
        #document.save()
        #with open(filename,'r') as data:
            #file = data.readlines()
        #print(file)
        #name=request.POST['Student_name']
        #marks=request.POST['Student_Mark']
        #grade=request.POST['Grade']
        #b=Studentdetail(id=Id,name=Student_name,marks=Student_Mark,grade=Grade)

        #with open('studentdata.xlsx','r') as data:
        #print(data.read())
        print(request.user)
        logout(request)
        return redirect("app:login")
    return render(request,"logout.html")

    
#def create_upload(request):
   #if request.method == 'GET':
        #form = UploadForm()
        #return render(request, 'logout.html', {'form': form})

# Create your views here.
#C:\Users\admin\Documents\studentdata.xlsx

def view_1(request):
    data=pangresdata.objects.all()
    all_page=request.GET.get('page',1)
    print('All_page',all_page)
    page = Paginator(data,per_page=10)
    print("page",page)    
    page_obj=page.get_page(all_page)
    print("Page Obj",page_obj)
    nums = "a" * page_obj.paginator.num_pages
    context = {}

    #try:
        #users = page.page(page)
    #except PageNotAnInteger:
        #users = page.page(1)
    #except EmptyPage:
        #users = page.page(page.num_pages)
    #data=serializers.serialize("python",pangresdata.objects.all())

    if request.method == 'POST':
        search = request.POST["query"]
        print(search)
        mulitple_q = Q(id__icontains=search) | Q(name__icontains=search) | Q(marks__icontains=search) | Q(grade__icontains=search)
        data1=pangresdata.objects.filter(mulitple_q).order_by('-id','-name','-marks','-grade')
        #context['data']= data
        #data=pangresdata.objects.all()
        all_page1=request.GET.get('page',1)
        print('All_page1',all_page1)
        page1 = Paginator(data1,per_page=10)
        print("page1",page1)    
        page_obj1=page1.get_page(all_page1)
        print("Page Obj1",page_obj1)
        nums1 = "a" * page_obj1.paginator.num_pages
        print('num1',nums1)
        context = {}
        #context={'data':data,
        #'data':page_obj}
        context['data']= page_obj1
        #context['data']= data1
        #context['nums']= nums1
        #data=serializers.serialize("python",pangresdata.objects.filter(name__icontains=search).order_by('-name'))
        #data=pangresdata.objects.all()
        #print(alldata)
        #print(data)
        return render(request,"view.html",context)
    #context= {'data':data,
    #'data':page_obj}
    context['data']= page_obj
    context['nums']= nums
    return render(request,"view.html",context)


def upload_1(request):
    if request.method == 'POST':
        filename=request.POST['file']
        print(filename)
        tmp_data=pd.read_excel(filename)
        print(tmp_data)
        tmp_data=tmp_data.set_index('id')
        print('Tmp file',tmp_data)
        engine=create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/jupyterdata")
        con = engine.connect()
        print(con)
        d_f=upsert(con=engine,df=tmp_data,table_name='app_pangresdata',if_row_exists='update',dtype=None)
        print(d_f)
        return render(request,"upload.html")
    return render(request,"upload.html")