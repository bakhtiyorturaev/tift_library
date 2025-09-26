from django.urls import path
from .views import MemberListView, MemberDetailView, MemberUpdateView

app_name = 'members'

urlpatterns = [
    path('', MemberListView.as_view(), name='list'),
    path('<int:pk>/', MemberDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MemberUpdateView.as_view(), name='edit'),
]
