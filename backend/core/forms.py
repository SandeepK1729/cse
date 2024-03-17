from django import forms  
from .models import User  
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = "__all__"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

