from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from mainapp.models import UserProfile

#Formularz do modyfikacji danych użytkownika
class ModifySuccessForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        #Pola, które będą wyświetlane w formularzu modyfikacji
        fields = ('username', 'first_name', 'last_name', 'email')

#Formularz do zarejestrowania użytkownika
class RegisterUserForm(UserCreationForm):
    #dodatkowe pola
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male',
                                         'Male'), ('Female',
                                                   'Female'), ('Other',
                                                               'Other')])
    height = forms.IntegerField(min_value=0)
    weight = forms.IntegerField(min_value=0)

    class Meta:
        model = User
        #pola wyświetlone w formularzu rejestracji    
        fields = [
            'username', 'email', 'password1', 'password2', 'birthday',
            'gender', 'height', 'weight'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            #zapisanie
            user.save()
            #utworzenie modelu UserProfile na podstawie danych z formularza
            UserProfile.objects.create(user=user,
                                       birthday=self.cleaned_data['birthday'],
                                       gender=self.cleaned_data['gender'],
                                       height=self.cleaned_data['height'],
                                       weight=self.cleaned_data['weight'])

        return user
