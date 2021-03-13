from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save









class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# This signal creates a UserProfile instance when a User is created
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)



class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey('UserProfile', on_delete=models.CASCADE, default=1)
    category = models.ForeignKey("Category", related_name="leads",on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'



class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


