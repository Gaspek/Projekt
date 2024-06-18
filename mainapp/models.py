from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# model bazowy
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

# model ćwiczenia
class Exercise(BaseModel):
    name = models.CharField(max_length=100)
    muscles = models.CharField(max_length=100)
    instructions = models.TextField()
    difficulty = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} - Difficulty: {self.difficulty}, Instructions: {self.instructions}"

# model wyzwania
class Challenge(BaseModel):
    name = models.CharField(max_length=100)
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - Start Date: {self.date_start}, End Date: {self.date_end}"

# profil użytkownika
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    birthday = models.DateField()
    gender = models.CharField(max_length=10)
    height = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return str(self.user)

# cele wyzwania
class ChallengeGoal(BaseModel):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    goal = models.IntegerField()

    def __str__(self):
        return f"{self.goal}"

# rekordy osobiste
class PersonalHighscore(BaseModel):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    highscore = models.IntegerField(default=0)
    date_got = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} - {self.highscore}"

# rekordy ćwiczeń
class ExerciseHighscore(BaseModel):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    highscore = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_got = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.highscore}"

# model treningu
class Workout(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='workout_images/',
                              blank=True,
                              null=True)

    def __str__(self):
        return self.name

# model ćwiczeń w treningu
class WorkoutExercise(BaseModel):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

# logi treningu
class ExerciseLog(BaseModel):
    workout_exercise = models.ForeignKey(WorkoutExercise,
                                         on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)

# postęp użytkownika w wyzwaniach
class UserChallengeProgress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    progress_value = models.IntegerField(default=0)
    goal = models.ForeignKey(ChallengeGoal,
                             on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return f'{self.user.username} - {self.challenge.name} - {self.progress_value}'
