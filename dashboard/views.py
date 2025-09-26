from datetime import timedelta

from django.db.models.aggregates import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from dashboard.mixins import LibrarianTransactionsMixin
from members.models import Member
from transactions.models import Transaction

class DashboardView(LibrarianTransactionsMixin,LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        transactions = Transaction.objects.filter(created_by=user)

        # Umumiy statistikalar
        context.update({
            'today': today,
            'tomorrow': tomorrow,
            'total_members': Member.objects.filter(created_by=user).count(),
            'active_loans': transactions.filter(returned=False).count(),
        })

        # Muddati o'tgan ijaralar (bugungacha)
        context['overdue_loans'] = transactions.filter(
            return_due_date__lt=today,
            returned=False
        ).order_by('return_due_date')

        # Muddati yaqin qolganlar (bugun yoki ertaga) va hali qaytarilmaganlar
        context['upcoming_returns'] = transactions.filter(
            return_due_date__date__range=(today, tomorrow),
            returned=False
        ).order_by('return_due_date')


        # Oxirgi 2 oy ichida kutubxonachi (user) bo‘yicha berilgan kitoblar
        two_months_ago = timezone.now() - timedelta(days=60)

        context['recent_transactions_count'] = (
            transactions.filter(given_at__gte=two_months_ago).count()
        )

        return context

