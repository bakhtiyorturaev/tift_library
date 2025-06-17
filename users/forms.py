from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class LibrarianCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_librarian = True
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Noto'g'ri foydalanuvchi nomi yoki parol kiritildi.",
        'inactive': "Bu hisob faol emas.",
    }