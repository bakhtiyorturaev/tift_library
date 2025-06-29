from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from dashboard.mixins import LibrarianTransactionsMixin
from .models import User
from .forms import LibrarianCreationForm, CustomAuthenticationForm


class CustomLoginView(LibrarianTransactionsMixin, LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')


class CustomLogoutView(LibrarianTransactionsMixin, LogoutView):
    template_name = 'users/logout.html'


class LibrarianCreateView(LibrarianTransactionsMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = LibrarianCreationForm
    template_name = 'users/create_librarian.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.is_librarian = True
        return super().form_valid(form)
