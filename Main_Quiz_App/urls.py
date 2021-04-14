from django.urls import path
from .views import *

urlpatterns=[
path('',HomePageView,name='Home'),
# path('', HomePageView.as_view(), name='Home'),
]