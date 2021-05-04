from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
path('',HomePageView,name='Home'),
path('Add',Add,name='Add'),
path('login', login, name='login'),
path('register', register, name='register'),
path('Save_Response', Save_Response, name='Save_Response'),
path('Response_Single', Response_Single, name='Response_Single'),
path('Submited_Response', Submited_Response, name='Submited_Response'),
path('Response_Single_sub', Response_Single_sub, name='Response_Single_sub'),
path('logout', logout, name='logout'),
path('about', about, name='about'),
path('profile', profile, name='profile'),
path('Add_Forms', Add_Forms, name='Add_Forms'),
path('ViewForm', ViewForm, name='ViewForm'),
# path('', HomePageView.as_view(), name='Home'),
]
urlpatterns=urlpatterns+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)