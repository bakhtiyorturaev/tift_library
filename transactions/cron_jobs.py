
from django.utils import timezone
from datetime import timedelta
from .models import Transaction

def delete_old_transactions():
    cutoff_date = timezone.now() - timedelta(days=90)
    deleted_count, _ = Transaction.objects.filter(
        returned=True,
        return_due_date__lt=cutoff_date
    ).delete()
