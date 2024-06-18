from django import forms
from .models import UserChallengeProgress, UserProfile, Workout, ExerciseLog, Challenge,PersonalHighscore

class AddEntryExercise(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['duration', 'weight', 'reps', 'distance', 'sets']

class ParticipateInChallengeForm(forms.ModelForm):
    challenge = forms.ModelChoiceField(
        queryset=Challenge.objects.all(),
        label="Challenge",
        widget=forms.Select(attrs={'style': 'font-weight: bold;'})
    )

    class Meta:
        model = UserChallengeProgress
        fields = ['challenge', 'progress_value']

class TrackProgressForm(forms.ModelForm):
    class Meta:
        model = UserChallengeProgress
        fields = ['progress_value']

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

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'image']

class PersonalHighscoreForm(forms.ModelForm):
    class Meta:
        model = PersonalHighscore
        fields = ['highscore']
