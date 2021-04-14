from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def HomePageView(request):
	return render(request,'index.html')
# class HomePageView(TemplateView):
# 	template_name='index.html'