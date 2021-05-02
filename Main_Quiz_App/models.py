from django.db import models
from jsonfield import JSONField

class Formtitle(models.Model):
    Form_name =models.CharField(max_length=100)
    User_id=models.IntegerField()
    def __str__(self):
        return self.id
class Questions(models.Model):
    Form = models.ForeignKey(Formtitle, on_delete=models.CASCADE)
    question=models.CharField(max_length=100)
    answer=JSONField(max_length=200)
    type=models.CharField(max_length=100)
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100,blank=True)
    option4=models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return self.question