from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
path('',HomePageView,name='Home'),
path('add',Add,name='add'),
path('login', login, name='login'),
path('register', register, name='register'),
path('registerstd', registerstd, name='registerstd'),
path('loginstd', loginstd, name='loginstd'),
path('logout', logout, name='logout'),
path('about', about, name='about'),
path('profile', profile, name='profile'),
path('Add_Forms', Add_Forms, name='Add_Forms'),
path('ViewForm', ViewForm, name='ViewForm'),
# path('', HomePageView.as_view(), name='Home'),
]
urlpatterns=urlpatterns+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)