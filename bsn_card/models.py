from django.db import models
from django.contrib.auth.models import User

#

class master(models.Model):
    img = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title

    class Meta:
        app_label = 'bsn_card'






# Create your models here.
class details(models.Model):
    img_bsn = models.ImageField()
    com_name=models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100)
    desi = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='')
    email_id = models.CharField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=100)
    fax_no = models.CharField(max_length=100, default='')
    desc = models.TextField()
    category= models.CharField(max_length=50,default='')
    comment = models.CharField(max_length=10000, default='' )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'bsn_card'


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'bsn_card'
