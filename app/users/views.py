from django.views.generic import UpdateView

from views import BaseLoggedInView

from .models import User


class MyAccountView(BaseLoggedInView, UpdateView):
    html_title = "My account"
    model = User
    fields = ("username", "email", "first_name", "last_name")
    success_url = "."

    def get_object(self, queryset=None):
        return self.request.user
