from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.mixins import LibrarianTransactionsMixin
from django.views.generic import TemplateView
from transactions.models import Transaction
from members.models import Member
from django.utils import timezone
from datetime import timedelta

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        transactions = Transaction.objects.filter(created_by=user)

        # Overdue loans (muddati o'tgan va qaytarilmagan)
        overdue_loans = [t for t in transactions if t.get_status()['status'] == 'overdue']
        overdue_loans = sorted(
            overdue_loans,
            key=lambda x: (x.return_due_date.date(), x.book_title.lower())
        )

        # Faqat Bugun/Ertaga qaytarilishi kerak bo‘lganlar
        upcoming_returns = [t for t in transactions if t.get_status()['status'] in ("today", "tomorrow")]
        upcoming_returns = sorted(
            upcoming_returns,
            key=lambda x: (x.return_due_date.date(), x.book_title.lower())
        )

        context.update({
            'recent_transactions_count': transactions.filter(given_at__gte=timezone.now() - timedelta(days=60)).count(),
            'total_members': Member.objects.filter(created_by=user).count(),
            'active_loans': transactions.filter(returned=False).count(),
            'upcoming_returns': upcoming_returns,
            'overdue_loans': overdue_loans,
        })

        return context

