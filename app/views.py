from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from forge.views.mixins import HTMLTitleMixin

from forms import SignupForm
from teams.models import Team, TeamMembership, TeamRoles


class BaseLoggedInMixin(LoginRequiredMixin, HTMLTitleMixin):
    html_title_suffix = " | Built with Forge"


class HomeView(BaseLoggedInMixin, TemplateView):
    html_title = "Home"
    template_name = "home.html"


class SignupView(CreateView):
    html_title = "Sign up"
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        # Create a "Personal" team for the new user
        team = Team.objects.create(name=user.username)
        TeamMembership.objects.create(user=user, team=team, role=TeamRoles.ADMIN)

        return super().form_valid(form)
