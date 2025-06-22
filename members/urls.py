from django.urls import path
from .views import MemberListView, MemberDetailView, MemberCreateView, MemberUpdateView, MemberTransactionHistoryView

app_name = 'members'

urlpatterns = [
    path('', MemberListView.as_view(), name='list'),
    path('create/', MemberCreateView.as_view(), name='create'),
    path('<int:pk>/', MemberDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MemberUpdateView.as_view(), name='edit'),
    path('<int:pk>/transactions/',MemberTransactionHistoryView.as_view(),name='member_transactions'),

]
