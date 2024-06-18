from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import RegisterUserForm, ModifySuccessForm
from django.views import generic
from django.urls import reverse_lazy
from mainapp.models import UserProfile

#Edytowanie profilu użytkownika
class UserEditView(generic.UpdateView):
  form_class = ModifySuccessForm
  template_name = 'authentication/edit_profile.html'
  success_url = reverse_lazy('profile')

  #zwrócenie aktualnie zalogowanego użytkownika
  def get_object(self):
    return self.request.user

#Obsługa logowania
def login_user(request):
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    #uwierzytelnienie użytkownika przy pomocy jego nazwy i hasła
    user = authenticate(request, username=username, password=password)
    if user is not None:
      #jeśli użytkoownik zalogowany, to zaloguj
      login(request, user)
      #powrót do strony głównej
      return redirect('home')

    else:
    #w przypadku błędu wyświetlenie komunikatu o błędzie
      messages.success(request,
                       ("There was an error logging in. Please try again."))
      return redirect('login')

  else:
    #jeśli metoda nie jest POST, to zwraca stronę logowania
    return render(request, 'authentication/login.html', {})

#obsługa wylogowywania
def logout_user(request):
  #wylogowanie
  logout(request)
  #wyświetlenie komunikat o sukcesie
  messages.success(request, ("You were logged out successfully!"))
  return redirect('home')

#obsługa rejestracji
def register_user(request):
  if request.method == "POST":
    form = RegisterUserForm(request.POST)
    #jeśli formularz poprawny - zapisanie użytkownika
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      #zalogowanie go
      login(request, user)
      messages.success(request, "You were registered successfully!")
      return redirect('home')
  else:
    form = RegisterUserForm()

  return render(request, 'authentication/register.html', {'form': form})
