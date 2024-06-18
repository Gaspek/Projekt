import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Exercise, Workout, ExerciseLog, Challenge, ChallengeGoal, UserProfile, WorkoutExercise, UserChallengeProgress, PersonalHighscore
from .forms import AddEntryExercise, ParticipateInChallengeForm, UserProfileForm, TrackProgressForm, PersonalHighscoreForm
from django.views import generic
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)

def home(request):
    logger.info("Home page requested")
    return render(request, 'home.html')

def workouts(request):
    workouts = Workout.objects.all()
    logger.debug(f"Retrieved {len(workouts)} workouts")
    return render(request, 'workouts.html', {'workouts': workouts})

def add_entry_workout(request, workout_name):
    workout = get_object_or_404(Workout, name=workout_name)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)
    exercise_logs = ExerciseLog.objects.filter(workout_exercise__workout=workout, user=request.user)
    logger.debug(f"Workout '{workout_name}' requested by user '{request.user.username}'")

    if request.method == 'POST':
        form = AddEntryExercise(request.POST)
        if form.is_valid():
            exercise_log = form.save(commit=False)
            exercise_log.workout_exercise_id = request.POST.get('exercise_id')
            exercise_log.user = request.user
            exercise_log.save()
            logger.info(f"New entry added to workout '{workout_name}' by user '{request.user.username}'")
            return redirect('workouts')
        else:
            logger.error(f"Error in add_entry_workout form: {form.errors}")
    else:
        form = AddEntryExercise()
        logger.debug("Add entry form initialized")

    context = {
        'add_entry_form': form,
        'workout': workout,
        'exercise_logs': exercise_logs,
        'workout_exercises': workout_exercises
    }
    return render(request, 'add_entry_workout.html', context)

def user_logs(request):
    exercise_logs = ExerciseLog.objects.filter(user=request.user)
    logger.debug(f"User logs retrieved for user '{request.user.username}'")
    context = {'exercise_logs': exercise_logs}
    return render(request, 'user_logs.html', context)

def exercises(request):
    exercises = Exercise.objects.all()
    logger.debug(f"Retrieved {len(exercises)} exercises")
    return render(request, 'exercises.html', {'exercises': exercises})

def challenges(request):
    challenges = Challenge.objects.all()
    logger.debug(f"Retrieved {len(challenges)} challenges")
    return render(request, 'challenges.html', {'challenges': challenges})

@login_required
def participate_in_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user_progress = UserChallengeProgress.objects.filter(user=request.user, challenge=challenge).first()
    goal = get_object_or_404(ChallengeGoal, id=challenge_id)
    logger.debug(f"Challenge '{challenge_id}' participation requested by user '{request.user.username}'")

    if request.method == 'POST':
        form = ParticipateInChallengeForm(request.POST, instance=user_progress)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.user = request.user
            participation.challenge = challenge
            participation.save()
            logger.info(f"User '{request.user.username}' participated in challenge '{challenge.name}'")
            return redirect('challenges')
        else:
            logger.error(f"Error in participate_in_challenge form: {form.errors}")
    else:
        form = ParticipateInChallengeForm(initial={'challenge': challenge}, instance=user_progress)
        logger.debug("Participate in challenge form initialized")

    return render(request, 'participate_in_challenge.html', {
        'form': form,
        'challenge': challenge,
        'user_progress': user_progress,
        'goal': goal
    })

@login_required
def track_progress(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    goals = ChallengeGoal.objects.filter(challenge=challenge)
    logger.debug(f"Track progress for challenge '{challenge_id}' requested by user '{request.user.username}'")

    if request.method == 'POST':
        form = TrackProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.challenge = challenge
            progress.save()
            logger.info(f"User '{request.user.username}' tracked progress in challenge '{challenge.name}'")
            return redirect('challenges')
        else:
            logger.error(f"Error in track_progress form: {form.errors}")
    else:
        form = TrackProgressForm()
        logger.debug("Track progress form initialized")

    return render(request, 'track_progress.html', {
        'form': form,
        'challenge': challenge,
        'goals': goals
    })

@login_required
def personal_records(request):
    records = PersonalHighscore.objects.filter(user=request.user).select_related('exercise')
    logger.debug(f"Personal records retrieved for user '{request.user.username}'")
    return render(request, 'personal_records.html', {'records': records})

@login_required
def update_record(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    record, created = PersonalHighscore.objects.get_or_create(user=request.user, exercise=exercise)
    logger.debug(f"Update record for exercise '{exercise_id}' requested by user '{request.user.username}'")

    if request.method == 'POST':
        form = PersonalHighscoreForm(request.POST, instance=record)
        if form.is_valid():
            new_record = form.cleaned_data['highscore']
            logger.debug(f"Current highscore: {record.highscore}, New record: {new_record}")
            if new_record > record.highscore:
                record.highscore = new_record
                record.date_got = timezone.now()
                record.save()
                logger.info(f"User '{request.user.username}' updated record for exercise '{exercise.name}' to '{new_record}'")
                messages.success(request, "Record updated successfully.")
                return redirect('personal_records')
            else:
                messages.error(request, "New record must be greater than the current highscore.")
                logger.warning(f"User '{request.user.username}' attempted to set new record ({new_record}) lower than or equal to current highscore ({record.highscore})")
        else:
            logger.error(f"Error in update_record form: {form.errors}")
            messages.error(request, "Invalid form submission.")
    else:
        form = PersonalHighscoreForm(instance=record)
        logger.debug("Update record form initialized")

    return render(request, 'update_record.html', {
        'form': form,
        'exercise': exercise,
        'record': record
    })

def hall_of_fame(request):
    exercises = Exercise.objects.all()
    hall_of_fame_records = []
    logger.debug("Hall of Fame page requested")

    for exercise in exercises:
        top_record = PersonalHighscore.objects.filter(exercise=exercise).order_by('-highscore').first()
        if top_record:
            hall_of_fame_records.append({
                'exercise': exercise,
                'user': top_record.user,
                'highscore': top_record.highscore,
                'date_got': top_record.date_got,
            })
    logger.debug(f"Retrieved {len(hall_of_fame_records)} records for Hall of Fame")
    return render(request, 'hall_of_fame.html', {'hall_of_fame_records': hall_of_fame_records})

def about_us(request):
    logger.info("About Us page requested")
    return render(request, 'about_us.html')

def contact(request):
    logger.info("Contact page requested")
    return render(request, 'contact.html')

def profile(request):
    logger.info("Profile page requested")
    return render(request, 'profile.html')

def w_e(request, workout_name):
    workout = get_object_or_404(Workout, name=workout_name)
    w_e = WorkoutExercise.objects.filter(workout=workout)
    logger.debug(f"Workout exercises for '{workout_name}' retrieved")
    return render(request, 'work_info.html', {'w_e': w_e, 'workout': workout})

class UserProfileCreateView(generic.CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'authentication/edit_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        logger.info(f"User profile created for '{self.request.user.username}'")
        return super().form_valid(form)

class UserProfileUpdateView(generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'authentication/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        logger.error(f"Error updating user profile for '{self.request.user.username}': {form.errors}")
        messages.error(self.request, "There was an error updating your profile. Please check the form.")
        return self.render_to_response(self.get_context_data(form=form))

def save_workouts_to_pdf(request):
    workouts = Workout.objects.all()
    html_string = render_to_string('workouts_pdf.html', {'workouts': workouts})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="workouts.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        logger.error("Error creating PDF for workouts")
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    logger.info("PDF for workouts created successfully")
    return response
