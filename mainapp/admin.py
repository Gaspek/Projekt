from django.contrib import admin
from .models import Exercise, Challenge, UserProfile, ChallengeGoal, PersonalHighscore, ExerciseHighscore, ExerciseLog, Workout, WorkoutExercise
from django.utils.html import format_html

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.image.url))
        return '-'
    image_tag.short_description = 'Image'

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercise)
admin.site.register(Challenge)
admin.site.register(UserProfile)
admin.site.register(ChallengeGoal)
admin.site.register(PersonalHighscore)
admin.site.register(ExerciseHighscore)
admin.site.register(ExerciseLog)
admin.site.register(WorkoutExercise)

