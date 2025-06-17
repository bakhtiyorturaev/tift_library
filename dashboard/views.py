from datetime import timedelta

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from dashboard.mixins import LibrarianTransactionsMixin
from members.models import Member
from transactions.models import Transaction


class DashboardView(LibrarianTransactionsMixin,LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Umumiy statistikalar
        context['total_members'] = Member.objects.count()
        context['active_loans'] = Transaction.objects.filter(returned=False).count()

        # Muddati o'tgan ijaralar
        today = timezone.localdate()
        context['overdue_loans'] = Transaction.objects.filter(
            return_due_date__lt=today,
            returned=False).order_by('return_due_date')[:10]

        # Hozirgi sana va ertangi sana

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        context['today'] = today
        context['tomorrow'] = tomorrow

        # Muddati yaqin qolgan (bugun va ertaga) va qaytarilmaganlar
        context['upcoming_returns'] = Transaction.objects.filter(
            return_due_date__date__gte=today,
            return_due_date__date__lte=tomorrow,
            returned=False
        ).order_by('return_due_date')[:10]


        return context
