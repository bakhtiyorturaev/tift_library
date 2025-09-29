from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Username yoki parol xato.",
        'inactive': "Bu hisob faol emas.",
    }