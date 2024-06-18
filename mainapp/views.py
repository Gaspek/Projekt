from .models import Exercise, Workout, Exercise, ExerciseLog, Challenge, ChallengeGoal, UserProfile, WorkoutExercise, UserChallengeProgress, PersonalHighscore
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddEntryExercise, ParticipateInChallengeForm, UserProfileForm, TrackProgressForm, PersonalHighscoreForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home(request):
    return render(request, 'home.html')


def workouts(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts.html', {'workouts': workouts})


def workouts(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts.html', {'workouts': workouts})


def add_entry_workout(request, workout_name):
    workout = get_object_or_404(Workout, name=workout_name)
    workout_exercises = WorkoutExercise.objects.all()
    exercise_logs = ExerciseLog.objects.filter(
        workout_exercise__workout=workout, user=request.user)

    if request.method == 'POST':
        form = AddEntryExercise(request.POST)
        if form.is_valid():
            exercise_log = form.save(commit=False)
            exercise_log.workout_exercise_id = request.POST.get('exercise_id')
            exercise_log.user = request.user
            exercise_log.save()
            return redirect('workouts')
    else:
        form = AddEntryExercise()

    context = {
        'add_entry_form': form,
        'workout': workout,
        'exercise_logs': exercise_logs,
        'workout_exercises': workout_exercises
    }
    return render(request, 'add_entry_workout.html', context)


def user_logs(request):
    exercise_logs = ExerciseLog.objects.filter(user=request.user)
    context = {'exercise_logs': exercise_logs}
    return render(request, 'user_logs.html', context)


def exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercises.html', {'exercises': exercises})


def challenges(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges.html', {'challenges': challenges})


@login_required
def participate_in_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user_progress = UserChallengeProgress.objects.filter(
        user=request.user, challenge=challenge).first()
    goal = get_object_or_404(ChallengeGoal, id=challenge_id)

    if request.method == 'POST':
        form = ParticipateInChallengeForm(request.POST, instance=user_progress)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.user = request.user
            participation.challenge = challenge
            participation.save()

            return redirect('challenges')
        else:
            print(
                form.errors)  # Print form errors to the console for debugging
    else:
        form = ParticipateInChallengeForm(initial={'challenge': challenge},
                                          instance=user_progress)

    return render(
        request, 'participate_in_challenge.html', {
            'form': form,
            'challenge': challenge,
            'user_progress': user_progress,
            'goal': goal
        })


@login_required
def track_progress(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    goals = ChallengeGoal.objects.filter(challenge=challenge)
    if request.method == 'POST':
        form = TrackProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.challenge = challenge
            progress.save()
            return redirect('challenges')
    else:
        form = TrackProgressForm()
    return render(request, 'track_progress.html', {
        'form': form,
        'challenge': challenge,
        'goals': goals
    })


@login_required
def personal_records(request):
    records = PersonalHighscore.objects.filter(
        user=request.user).select_related('exercise')
    return render(request, 'personal_records.html', {'records': records})


@login_required
def update_record(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    record, created = PersonalHighscore.objects.get_or_create(
        user=request.user, exercise=exercise)

    if request.method == 'POST':
        form = PersonalHighscoreForm(request.POST, instance=record)
        if form.is_valid():
            new_record = form.cleaned_data['highscore']
            print(
                f"Current highscore: {record.highscore}, New record: {new_record}"
            )  # Debugging statement
            if new_record > record.highscore:
                record.highscore = new_record
                record.date_got = timezone.now()
                record.save()
                messages.success(request, "Record updated successfully.")
                return redirect('personal_records')
            else:
                messages.error(
                    request,
                    "New record must be greater than the current highscore.")
        else:
            print(form.errors)  # Debugging: Print form errors to the console
            messages.error(request, "Invalid form submission.")
    else:
        form = PersonalHighscoreForm(instance=record)

    return render(request, 'update_record.html', {
        'form': form,
        'exercise': exercise,
        'record': record
    })


def hall_of_fame(request):
    exercises = Exercise.objects.all()
    hall_of_fame_records = []

    for exercise in exercises:
        top_record = PersonalHighscore.objects.filter(
            exercise=exercise).order_by('-highscore').first()
        if top_record:
            hall_of_fame_records.append({
                'exercise': exercise,
                'user': top_record.user,
                'highscore': top_record.highscore,
                'date_got': top_record.date_got,
            })

    return render(request, 'hall_of_fame.html',
                  {'hall_of_fame_records': hall_of_fame_records})


def about_us(request):
    return render(request, 'about_us.html')


def contact(request):
    return render(request, 'contact.html')


def profile(request):
    return render(request, 'profile.html')


def w_e(request, workout_name):
    workout = get_object_or_404(Workout, name=workout_name)
    w_e = WorkoutExercise.objects.all()
    template_name = 'work_info.html'
    context = {'w_e': w_e, 'workout': workout}
    return render(request, 'work_info.html', context)


class UserProfileCreateView(generic.CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'authentication/edit_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserProfileUpdateView(generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'authentication/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(
            self.request,
            "There was an error updating your profile. Please check the form.")
        return self.render_to_response(self.get_context_data(form=form))


def save_workouts_to_pdf(request):
    workouts = Workout.objects.all()
    html_string = render_to_string('workouts_pdf.html', {'workouts': workouts})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="workouts.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string +
                            '</pre>')
    return response
