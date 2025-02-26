from django.db import models
from accounts.models import CustomUser

# Create your models here.
class New(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=10000)
    publication_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(CustomUser, null= True, on_delete= models.SET_NULL)

    def __str__(self):
        return self.title

