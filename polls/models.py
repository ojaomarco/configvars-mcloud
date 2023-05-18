from django.db import models

# Create your models here.
class Botao(models.Model):
    button_text = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date')

class Botao2(models.Model):
    button_text = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date2')
