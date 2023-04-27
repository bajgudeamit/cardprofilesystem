from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from CMS.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
# Create your models here.


class Custom_user(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=250)
    phone_no=models.CharField(max_length=20,unique=True)
    url=models.URLField(unique=True)
    profile_pic=models.ImageField(upload_to='images/',null=True,blank=True)

    def __str__(self):
        return f'{self.user}'
    

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message= "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        "Password Reset request for {title}".format(title="www.cardprofilesys.com"),
        email_plaintext_message,
        EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
