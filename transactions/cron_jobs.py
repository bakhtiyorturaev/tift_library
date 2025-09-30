
from django.utils import timezone
from datetime import timedelta
from .models import Transaction

def delete_old_transactions():
    """90 kundan eski va qaytarilgan transactionlarni o‘chirish"""
    cutoff_date = timezone.now() - timedelta(days=90)
    deleted_count, _ = Transaction.objects.filter(
        returned=True,
        return_due_date__lt=cutoff_date
    ).delete()
