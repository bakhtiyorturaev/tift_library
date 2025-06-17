from django.urls import path
from .views import CustomLoginView, CustomLogoutView, LibrarianCreateView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('create-librarian/', LibrarianCreateView.as_view(), name='create_librarian'),
]