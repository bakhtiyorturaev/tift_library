
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from dashboard.mixins import LibrarianTransactionsMixin
from transactions.models import Transaction
from django.db.models import Q
from .models import Member
from .forms import MemberForm


class MemberListView(LibrarianTransactionsMixin ,LoginRequiredMixin, ListView):
    model = Member
    template_name = 'members/member_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        created_from = self.request.GET.get('created_from')

        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(phone__icontains=search_query)
            )

        if created_from:
            queryset = queryset.filter(created_at__gte=created_from)

        return queryset.order_by('full_name')


class MemberDetailView(LibrarianTransactionsMixin, LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'members/member_detail.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.object

        active_loans = Transaction.objects.filter(
            member=member,
            returned=False
        ).order_by('return_due_date')

        # har bir loan uchun extra atributlar: is_overdue, days_remaining
        for loan in active_loans:
            now = timezone.now().date()
            loan.days_remaining = (loan.return_due_date.date() - now).days

        context['active_loans'] = active_loans
        return context


class MemberCreateView(LibrarianTransactionsMixin, LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/member_form.html'
    success_url = reverse_lazy('members:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Yangi talaba qo\'shish'
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MemberUpdateView(LibrarianTransactionsMixin, LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/forms.html'
    context_object_name = 'member'

    def get_success_url(self):
        return reverse('members:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Talaba ma\'lumotlarini tahrirlash'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Talaba ma\'lumotlari muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Ma\'lumotlarni saqlashda xatolik yuz berdi. Iltimos, tekshirib qaytadan urunib ko\'ring.')
        return super().form_invalid(form)