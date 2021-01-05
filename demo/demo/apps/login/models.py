from django.db import models

# Create your models here.
class Yonghu(models.Model):
    yonghu_id = models.CharField(max_length=32, unique=True)
    yonghu_secret = models.CharField(max_length=32)

class svn_asset(models.Model):
    svn_name=models.CharField(max_length=128)
    path=models.CharField(max_length=128)
    last_change_person=models.CharField(max_length=128)
    last_change_date=models.CharField(max_length=128)
# Create your models here.
