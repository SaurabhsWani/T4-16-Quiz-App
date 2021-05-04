from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from pymongo import MongoClient
import secrets
import string
from bson.objectid import ObjectId
import datetime

# Mongodb Connection
con="mongodb://127.0.0.1:27017/" 
client = MongoClient(con)
db=client.get_database("ssw")
collection = db.get_collection("ssw_collection")

# Home Page VIew
def HomePageView(request):
    if request.user.is_authenticated:
        forms = Formtitle.objects.filter(User_id =request.user.id) 
        return render(request,'index.html',{'forms':forms})
    else:
        return redirect('login')
# View form from url
def ViewForm(request):
    if request.user.is_authenticated:
        id=request.GET.get('id')
        Formname=Formtitle.objects.filter(Form_Url=id)
        USerForm = Questions.objects.filter(Form_id=Formname[0].id)
        return render(request,'result.html',{'USerForm':USerForm,'Formname':Formname,'url':id})
    else:
        id=request.GET.get('id')
        return render(request,'login.html',{'url':id})
# Checking form exist or not
def Add_Forms(request):
    if request.user.is_authenticated:
        formtitl=request.POST.get('Formname',None)
        if formtitl==None:
            return redirect('/')
        user_id=request.user.id
        if Formtitle.objects.filter(Form_name =formtitl,User_id=user_id).exists():
            messages.info(request,"Form Name Already Exist, Enter Different Form Name")
            return redirect('/')
        else:
            return render(request,'Add_Form.html',{'formtitl':formtitl})
    else:
        return redirect('login')
# inserting form with questions in db        
def Add(request):
    if request.user.is_authenticated:
        #input from html form
        formtitl=request.POST.get('Formname',None)        
        question=request.POST.getlist('question',None)
        typee=request.POST.getlist('type',None)
        # answer=request.POST.getlist('answer',None)
        option1=request.POST.getlist('option1',None)
        option2=request.POST.getlist('option2',None)
        option3=request.POST.getlist('option3',None)
        option4=request.POST.getlist('option4',None)
        no=request.POST.getlist('no',None)
        user_id=request.user.id        
        #saving Form name
        N = 10
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(N))
        queryset1 = Formtitle(Form_name=formtitl,User_id=user_id,Form_Url=res)
        queryset1.save()     
        #getting form id
        USerForm = Formtitle.objects.filter(Form_name =formtitl,User_id=user_id)
        formid=USerForm[0]        
        questions=[]
        #formatting questions
        for i in range(len(question)):
            questionn=[]
            questionn.append(question[i])
            questionn.append(typee[i])
            noo=request.POST.getlist(no[i],None)
            questionn.append(noo)
            questionn.append(option1[i])
            questionn.append(option2[i])
            questionn.append(option3[i])
            questionn.append(option4[i])
            questions.append(questionn)           
            #saving question to mysql db           
            UserFormQuestion=Questions.objects.create(Form=formid,question=question[i],answer=noo,type=typee[i],option1=option1[i],option2=option2[i],option3=option3[i],option4=option4[i])
            UserFormQuestion.save()       
            #returning to success page        
        messages.info(request,"Form Created Succesfully!")
        return redirect('/',{'questions':questions,'formtitl':formtitl})
    else:
        return redirect('login')

# Regiset user view
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
# User login view
def login(request):
    if request.method=='POST':
        url=request.POST['url']
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if url != '' :
                return redirect('/ViewForm?id='+url)
            else:
                return redirect('/')
        else:
            messages.info(request,"Invalid Credential")
            return redirect('/login')
    else:
        return render(request, 'login.html')    
# Logout view 
def logout(request):
    auth.logout(request)
    return redirect('/')
# View profile view    
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    else:
        return redirect('login')
#about us view
def about(request):
	return render(request, 'about.html')
#Saving response to mongodb db
def Save_Response(request):
    if request.user.is_authenticated and request.method=='POST':
        #input from html form
        responsesender=request.POST.get('responsesender',None)
        responsesendername=request.POST.get('responsesendername',None)  
        Formid=request.POST.get('Formid',None) 
        formname=request.POST.get('formname',None) 
        createruserid=request.POST.get('createruserid',None) 
        Questionid=request.POST.getlist('Questionid',None)
        no=request.POST.getlist('no',None)
        typee=request.POST.getlist('type',None)        
        questions=[]
        #formatting response
        for i in range(len(Questionid)):
            questionn=[]
            Qt=Questions.objects.filter(id=Questionid[i])
            questionn.append(Qt[0].question)
            fi=Formtitle.objects.filter(id=Formid)
            noo=request.POST.getlist(no[i],None)
            questionn.append(noo)
            questions.append(questionn) 
        doc={'Form_id':Formid,
             'Submit_Time':datetime.datetime.now(),
             'Form_name':formname,
             'User_id':createruserid,
             'Response_User_id':responsesender,
             'Question':questions,
             }
        #saving response to db     
        docin=collection.insert_one(doc)    #Insert only one data in collection
        messages.info(request,"Response Submitted Successfully")       
        #returning to success page  
        return redirect('/Submited_Response')
    elif request.user.is_authenticated:
        formids=Formtitle.objects.filter(User_id=request.user.id)
        responsecount=[]
        for x in formids:
            print(x.id)
            cursor=collection.find({"User_id":str(request.user.id),"Form_id":str(x.id)})
            responsecount.append(cursor.count())
        myresponse=zip(formids,responsecount)
        print(myresponse)
        return render(request,'Response.html',{'formids':formids,'responsecount':responsecount,'myresponse':myresponse})
    else:
        return redirect('login')
# Viewing all submitted response of form by another user
def Response_Single(request):
    if request.user.is_authenticated :
        formid=request.GET.get('formid')
        cursor=collection.find({"User_id":str(request.user.id),"Form_id":formid})
        if cursor.count() == 0:
            messages.info(request,"No Response Yet")
        else:
            messages.info(request,str(cursor.count())+" Response/s")
        return render(request,'Response_Single.html',{'res':cursor,})
    else:
        return redirect('login')
# getting list of submitted responsed by me
def Submited_Response(request):
    if request.user.is_authenticated:
        cursor=collection.find({"Response_User_id":request.user.first_name+" "+request.user.last_name})
        return render(request,'Submited_response.html',{'cursor':cursor})
    else:
        return redirect('login')
# Viewing all submitted response of form by another user
def Response_Single_sub(request):
    if request.user.is_authenticated :
        formid=request.GET.get('formid')
        cursor=collection.find({"Response_User_id":request.user.first_name+" "+request.user.last_name,"Form_id":formid})
        if cursor.count() == 0:
            messages.info(request,"No Response Yet")
        else:
            messages.info(request,str(cursor.count())+" Response/s")
        return render(request,'Response_Single.html',{'res':cursor,})
    else:
        return redirect('login')