from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from dashboard.mixins import LibrarianTransactionsMixin
from .forms import CustomAuthenticationForm


class CustomLoginView(LibrarianTransactionsMixin, LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.session.flush()
        return response
