from django.urls import path
from . import views
from .views import UserEditView

#ścieżki
urlpatterns = [
    #logowania
    path('login_user', views.login_user, name="login"),
    #wylogowania
    path('logout_user', views.logout_user, name="logout"),
    #rejestracji
    path('register', views.register_user, name="register"),
    #edycji profilu
    path('edit_profile/', UserEditView.as_view(), name="edit_profile"),
]
