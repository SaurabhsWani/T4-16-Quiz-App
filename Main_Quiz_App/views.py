from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from bson.objectid import ObjectId
from pymongo import MongoClient

# con="mongodb://127.0.0.1:27017/" 
# client = MongoClient(con)
# db=client.get_database("ssw")
# collection = db.get_collection("ssw_collection")
# dest1=Destination.objects.all()
# filter={"_id":ObjectId("6088d8d58c7aa79f3bc2bb63")}
# cursor=collection.find(filter)
# print(cursor.count())
# for each_doc in cursor:
#     print(each_doc)
    # for x in each_doc['arr']:
    #     print(x)


def HomePageView(request):
    if request.user.is_authenticated:
        forms = Formtitle.objects.filter(User_id =request.user.id) 
        return render(request,'index.html',{'forms':forms})
    else:
        return redirect('login')
def ViewForm(request):
    if request.user.is_authenticated:
        id=request.GET.get('id')
        Formname=Formtitle.objects.filter(id=id)
        USerForm = Questions.objects.filter(Form_id=id)
        return render(request,'result.html',{'USerForm':USerForm,'Formname':Formname})
    else:
        return redirect('login')
def Add_Forms(request):
    if request.user.is_authenticated:
        formtitl=request.POST.get('Formname',None)
        user_id=request.user.id
        if Formtitle.objects.filter(Form_name =formtitl,User_id=user_id).exists():
            messages.info(request,"Form Name Already Exist, Enter Different Form Name")
            return redirect('/')
        else:
            return render(request,'Add_Form.html',{'formtitl':formtitl})
    else:
        return redirect('login')
        
def Add(request):
    if request.user.is_authenticated:
        #input from html form
        formtitl=request.POST.get('Formname',None)        
        question=request.POST.getlist('question',None)
        typee=request.POST.getlist('type',None)
        option1=request.POST.getlist('option1',None)
        option2=request.POST.getlist('option2',None)
        option3=request.POST.getlist('option3',None)
        option4=request.POST.getlist('option4',None)
        no=request.POST.getlist('no',None)
        user_id=request.user.id        
        #saving Form name
        queryset1 = Formtitle(Form_name=formtitl,User_id=user_id)
        queryset1.save()     
        #getting form id
        USerForm = Formtitle.objects.filter(Form_name =formtitl,User_id=user_id)
        formid=USerForm[0]
        print(USerForm[0].id)
        
        questions=[]
        #formatting questions
        for i in range(len(question)):
            questionn=[]
            questionn.append(question[i])
            print('Question: '+question[i])
            questionn.append(typee[i])
            print('Type: '+typee[i])
            noo=request.POST.getlist(no[i],None)
            print(noo)
            questionn.append(noo)
            questionn.append(option1[i])
            questionn.append(option2[i])
            questionn.append(option3[i])
            questionn.append(option4[i])
            questions.append(questionn)
            print('option1: '+option1[i])
            print('option2: '+option2[i])
            print('option3: '+option2[i])
            print('option4: '+option4[i])
            
            #saving question to db            
            UserFormQuestion=Questions.objects.create(Form=formid,question=question[i],answer=noo,type=typee[i],option1=option1[i],option2=option2[i],option3=option3[i],option4=option4[i])
            UserFormQuestion.save()       
            #returning to success page        
        messages.info(request,"Form Created Succesfully!")
        return redirect('/',{'questions':questions,'formtitl':formtitl})
    else:
        return redirect('login')
# class HomePageView(TemplateView):
# 	template_name='index'
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username taken")
                return redirect('/register')        
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email taken")
                return redirect('/register')        
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('User Created')
                return redirect('login')
        else:
            messages.info(request,"Password not matching...")
            return redirect('register')        
    else:
        return render(request,'register.html')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credential")
            return redirect('/login')
    else:
        return render(request, 'login.html')    
def registerstd(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username taken")
                return redirect('/registerstd')        
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email taken")
                return redirect('/registerstd')        
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('User Created')
                return redirect('login')
        else:
            messages.info(request,"Password not matching...")
            return redirect('registerstd')        
    else:
        return render(request,'registerstd.html')
def loginstd(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credential")
            return redirect('/login')
    else:
        return render(request, 'loginstd.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
    
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    else:
        return redirect('login')

def about(request):
	return render(request, 'about.html')
