from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget
from django.db.models import Q
import datetime as dt
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,is_staff,is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError("The email address doesn't exist")

        email = self.normalize_email()
        user = self.model(email = email, is_staff= is_staff, is_active=True, is_superuser= is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,email, password=None, **extra_fields):
        return self.create_user(email, password, False, False, **extra_fields)
    
    def create_superuser(self,email, password, **extra_fields):
        return self.create_user(email, is_staff= True,is_superuser= True)
 
class CustomUser(AbstractBaseUser):
    email= models.EmailField(max_length=255, blank = True, unique=True)
    username = models.CharField(max_length=255,unique = True, blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def email_user(self, subject, message, from_email=None):
        send_mail(subject,message,from_email,[self.email])

    def __str__(self):
        return self.email

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hoods/', null=True)
    neighbourhood_count= models.IntegerField(default=0, null=True, blank=True)
   
    def __str__(self):
        return self.neighbourhood

    def save_neighbourhood(self):
        self.save()

    @classmethod
    def delete_neighbourhood(cls,neighbourhood):
        cls.objects.filter(neighbourhood=neighbourhood).delete()


class News(models.Model):
    title = models.CharField(max_length=100)
    notification = HTMLField()
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    neighbourhood_id = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Healthservices(models.Model):
    healthservices = models.CharField(max_length=100)

    def __str__(self):
        return self.healthservices

    def save_healthservices(self):
        self.save()

    @classmethod
    def delete_healthservices(cls,healthservices):
        cls.objects.filter(healthservices=healthservices).delete()


class Business(models.Model):
    business_name = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    description = HTMLField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="business")
    neighbourhood_id = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE,related_name="neighbourhoodbusiness",null=True,blank=True)
    contact = models.IntegerField()
    business_email = models.CharField(max_length=200, null = True)
    
  

    def __str__(self):
        return self.business_name

class Health(models.Model):
    health_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    neighbourhood_id = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE)
    email = models.EmailField()
    contact = models.IntegerField()
    health_email = models.CharField(max_length=200, null = True)
    healthservices = models.ManyToManyField(Healthservices)

    def __str__(self):
        return self.name

class Authorities(models.Model):
    authority_name =models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
   
    neighbourhood_id = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE)
    email = models.EmailField()
    contact = models.IntegerField()
    authority_email = models.CharField(max_length=200, null = True)
   

    def __str__(self):
        return self.name


class Profile(models.Model):
    prof_pic = ImageField(blank=True, manual_crop='')
    bio = HTMLField()
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE)

    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()