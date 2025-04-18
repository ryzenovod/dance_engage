from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


# forms.py
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Дама', 'Дама'),
        ('Кавалер', 'Кавалер'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Ваша роль')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=commit)

        # Создаем профиль, только если его нет
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user

class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Можно добавить дополнительные проверки, если нужно
        pass

    def save(self, commit=True):
        user = super().save(commit=False)

        # Проверяем, существует ли уже профиль для этого пользователя
        try:
            UserProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            # Профиль не найден, создаём новый
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])

        if commit:
            user.save()
        return user

from django import forms
from .models import UserProfile

# forms.py
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'skills', 'avatar']  # Поле skills обязательно!
