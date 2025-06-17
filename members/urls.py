from django.urls import path
from .views import MemberListView, MemberDetailView, MemberCreateView, MemberUpdateView

app_name = 'members'

urlpatterns = [
    path('', MemberListView.as_view(), name='list'),
    path('create/', MemberCreateView.as_view(), name='create'),
    path('<int:pk>/', MemberDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MemberUpdateView.as_view(), name='edit'),

]
