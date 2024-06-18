import logging
from django import forms
from .models import UserChallengeProgress, UserProfile, Workout, ExerciseLog, Challenge, PersonalHighscore

# Configure logger
logger = logging.getLogger(__name__)

# formularz dodawania szczegółów ćwiczenia
class AddEntryExercise(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['duration', 'weight', 'reps', 'distance', 'sets']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("AddEntryExercise form initialized")

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"AddEntryExercise form cleaned: {cleaned_data}")
        return cleaned_data

# formularz uczestnictwa w wyzwaniu
class ParticipateInChallengeForm(forms.ModelForm):
    challenge = forms.ModelChoiceField(
        queryset=Challenge.objects.all(),
        label="Challenge",
        widget=forms.Select(attrs={'style': 'font-weight: bold;'})
    )

    class Meta:
        model = UserChallengeProgress
        fields = ['challenge', 'progress_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("ParticipateInChallengeForm form initialized")

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"ParticipateInChallengeForm form cleaned: {cleaned_data}")
        return cleaned_data

# formularz śledzenia postępów użytkownika w wyzwaniu
class TrackProgressForm(forms.ModelForm):
    class Meta:
        model = UserChallengeProgress
        fields = ['progress_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("TrackProgressForm form initialized")

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"TrackProgressForm form cleaned: {cleaned_data}")
        return cleaned_data

# formularz danych użytkownika
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'gender', 'height', 'weight']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'height': forms.NumberInput(attrs={'min': 0}),
            'weight': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("UserProfileForm form initialized")

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"UserProfileForm form cleaned: {cleaned_data}")
        return cleaned_data

# formularz dodawania treningu
class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("WorkoutForm form initialized")

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"WorkoutForm form cleaned: {cleaned_data}")
        return cleaned_data

# formularz dodawania własnego rekordu użytkownika
class PersonalHighscoreForm(forms.ModelForm):
    class Meta:
        model = PersonalHighscore
        fields = ['highscore']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("PersonalHighscoreForm form initialized")

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"PersonalHighscoreForm form cleaned: {cleaned_data}")
        return cleaned_data
