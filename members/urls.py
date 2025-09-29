from django.urls import path
from .views import MemberListView, MemberDetailView, MemberUpdateView, ReturnMultipleView

app_name = 'members'

urlpatterns = [
    path('', MemberListView.as_view(), name='list'),
    path('<int:pk>/', MemberDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MemberUpdateView.as_view(), name='edit'),
    path("return-multiple/", ReturnMultipleView.as_view(), name="return_multiple"),

]
