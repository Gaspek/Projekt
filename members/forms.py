from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from mainapp.models import UserProfile
from django.core.mail import send_mail


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')


class ModifySuccessForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class RegisterUserForm(UserCreationForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male',
                                         'Male'), ('Female',
                                                   'Female'), ('Other',
                                                               'Other')])
    height = forms.IntegerField(min_value=0)
    weight = forms.IntegerField(min_value=0)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'birthday',
            'gender', 'height', 'weight'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user,
                                       birthday=self.cleaned_data['birthday'],
                                       gender=self.cleaned_data['gender'],
                                       height=self.cleaned_data['height'],
                                       weight=self.cleaned_data['weight'])

        return user
