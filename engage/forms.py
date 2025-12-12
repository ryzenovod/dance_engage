from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Дама', 'Дама'),
        ('Кавалер', 'Кавалер'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Роль на балу')
    first_name = forms.CharField(label='Реальное имя')
    last_name = forms.CharField(label='Реальная фамилия')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].help_text = 'Используйте только буквы, цифры и символы @/./+/-/_.'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Например, boston_valzer',
            'class': 'form-control'
        })

        self.fields['first_name'].help_text = 'Это имя увидят только ваши мэтчи.'
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Например, Анна',
            'class': 'form-control'
        })

        self.fields['last_name'].help_text = 'Поможет партнёру узнать вас в реальности после взаимного мэтча.'
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Например, Иванова',
            'class': 'form-control'
        })

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = 'Минимум 8 символов, нельзя использовать простой пароль.'
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Придумайте пароль',
            'class': 'form-control'
        })

        self.fields['password2'].label = 'Повторите пароль'
        self.fields['password2'].help_text = 'Введите тот же пароль ещё раз.'
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль',
            'class': 'form-control'
        })

        self.fields['role'].label = 'Кто вы на балу?'
        self.fields['role'].help_text = 'Выберите подходящую роль, чтобы мы показывали правильных партнёров.'
        self.fields['role'].widget.attrs.update({'class': 'form-select'})

        # Делаем реальные данные обязательными, чтобы они раскрывались при мэтче
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        if commit and not hasattr(user, 'userprofile'):
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

        try:
            UserProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=user, role=self.cleaned_data.get('role', 'Дама'))

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'skills', 'avatar']  # Поле skills обязательно!
