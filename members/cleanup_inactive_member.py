from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from members.models import Member
from transactions.cron_jobs import delete_old_transactions
from transactions.models import Transaction

class Command(BaseCommand):
    help = "Eski transactionlarni va faol bo‘lmagan talabalarni tozalash"

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=90)

        #  Avval eski transactionlarni o‘chiramiz
        deleted_tx = delete_old_transactions()
        self.stdout.write(f"Deleted {deleted_tx} old transactions.")

        #  Faol bo‘lmagan talabalarni o‘chiramiz
        for member in Member.objects.all():
            has_unreturned_books = Transaction.objects.filter(
                member=member,
                returned=False
            ).exists()
            if has_unreturned_books:
                continue

            recent_transaction = Transaction.objects.filter(
                member=member,
                given_at__gte=cutoff_date
            ).exists()
            if not recent_transaction:
                self.stdout.write(f"Deleting {member.full_name}")
                member.delete()
