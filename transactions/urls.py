from django.urls import path
from .views import TransactionListView, TransactionCreateView, TransactionCreateForStudentView, \
                   BulkConfirmView

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListView.as_view(), name='list'),
    path('create/', TransactionCreateView.as_view(), name='create'),
    path('create/<int:pk>/', TransactionCreateForStudentView.as_view(), name='create_for_student'),
    # path('<int:pk>/return', TransactionReturnView.as_view(), name='return'),
    path("bulk-confirm/", BulkConfirmView.as_view(), name="bulk_confirm"),

]