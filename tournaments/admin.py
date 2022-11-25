from django.contrib import admin

from .models import Team, Tournament


class TeamInline(admin.StackedInline):
    model = Team
    extra = 3


class TournamentAdmin(admin.ModelAdmin):
    inlines = [TeamInline]


admin.site.register(Tournament, TournamentAdmin)
