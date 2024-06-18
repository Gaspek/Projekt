from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import UserProfileCreateView, UserProfileUpdateView

# ścieżki URL
urlpatterns = [
    path("", views.home, name="home"),
    path("workouts/pdf/", views.save_workouts_to_pdf, name="save_workouts_to_pdf"),  # Ensure this is before the workout detail pattern
    path("workouts/", views.workouts, name="workouts"),
    path("workouts/<str:workout_name>/", views.w_e, name="w_e"),
    path("workouts/add_entry_workout/<str:workout_name>/", views.add_entry_workout, name="add_entry_workout"),
    path('user_logs/', views.user_logs, name='user_logs'),
    path("exercises/", views.exercises, name="exercises"),
    path('challenges/', views.challenges, name='challenges'),
    path('challenges/participate/<int:challenge_id>/', views.participate_in_challenge,name='participate_in_challenge'),
    path('challenges/track/<int:challenge_id>/', views.track_progress, name='track_progress'),
    path('hall_of_fame/', views.hall_of_fame, name='hall_of_fame'),
    path("about_us/", views.about_us, name="about_us"),
    path("contact/", views.contact, name="contact"),
    path("members/", include('django.contrib.auth.urls')),
    path("members/", include('members.urls')),
    path("profile/", views.profile, name="profile"),
    path("profile/edit_extra/", UserProfileUpdateView.as_view(), name="profile_edit"),
    path('personal_records/', views.personal_records, name='personal_records'),
    path('update_record/<int:exercise_id>/', views.update_record, name='update_record')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
