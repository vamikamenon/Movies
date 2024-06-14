from django import forms
from django.contrib.auth.models import User

from . models import Movies,Details


class MovieForm(forms.ModelForm):
    class Meta:
        model=Movies
        fields=['title','category','desc','actors','release_date','poster','utube_link']


class DetailsForm(forms.ModelForm):
    class Meta:
        model=Details
        fields=['review','rating']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']
