from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.db.models import Q

from dashboard.mixins import LibrarianTransactionsMixin
from members.forms import MemberForm
from members.models import Member
from .models import Transaction
from .forms import TransactionForm


class TransactionListView(LibrarianTransactionsMixin, LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    paginate_by = 20


    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        returned = self.request.GET.get('returned')
        given_from = self.request.GET.get('given_from')
        given_to = self.request.GET.get('given_to')
        due_soon = self.request.GET.get('due_soon')
        overdue = self.request.GET.get('overdue')

        if search_query:
            queryset = queryset.filter(
                Q(book_title__icontains=search_query) |
                Q(member__full_name__icontains=search_query) |
                Q(member__student_id__icontains=search_query) |
                Q(member__phone__icontains=search_query)
            )

        if returned in ['True', 'False']:
            queryset = queryset.filter(returned=returned)
        if given_from:
            queryset = queryset.filter(given_at__gte=given_from)
        if given_to:
            queryset = queryset.filter(given_at__lte=given_to)

        now_date = timezone.now().date()
        tomorrow = now_date + timedelta(days=2)

        # 2 kun ichida qaytarilishi kerak bo'lganlar
        if due_soon == 'true':
            queryset = queryset.filter(
                returned=False,
                return_due_date__gte=now_date,
                return_due_date__lte=tomorrow
            )

        if overdue == 'true':
            queryset = queryset.filter(
                returned=False,
                return_due_date__lt=now_date
            )
        return queryset.order_by('returned','return_due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        context['returned'] = self.request.GET.get('returned', '')
        context['given_from'] = self.request.GET.get('given_from', '')
        context['given_to'] = self.request.GET.get('given_to', '')
        context['due_soon'] = self.request.GET.get('due_soon', '')
        context['overdue'] = self.request.GET.get('overdue', '')



        return context


class TransactionCreateView(LibrarianTransactionsMixin, LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.filter(created_by=self.request.user).order_by('full_name')
        context['member_form'] = kwargs.get('member_form') or MemberForm()
        context['transaction_form'] = kwargs.get('transaction_form') or TransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None

        member_form = MemberForm(request.POST)
        transaction_form = TransactionForm(request.POST)

        # Talaba ID bo'yicha mavjud talabani tekshirish
        student_id = request.POST.get('student_id')
        if student_id:
            try:
                member = Member.objects.get(student_id=student_id)
                member_form = MemberForm(request.POST, instance=member)
            except Member.DoesNotExist:
                pass

        if member_form.is_valid() and transaction_form.is_valid():
            member = member_form.save(commit=False)
            member.created_by = request.user
            member.save()

            transaction = transaction_form.save(commit=False)
            transaction.member = member
            transaction.created_by = request.user
            transaction.save()
            return self.form_valid(transaction_form)
        else:
            return self.form_invalid(transaction_form, member_form)


    def form_invalid(self, transaction_form, member_form):
        """Ikkala formani kontekstga qayta yuboramiz"""
        return self.render_to_response(self.get_context_data(
            transaction_form=transaction_form,
            member_form=member_form
        ))

class TransactionCreateForStudentView(LibrarianTransactionsMixin, FormView):
    template_name = 'transactions/transaction_form_for_student.html'
    form_class = TransactionForm

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('members:detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        member = get_object_or_404(Member, pk=pk)
        member_form = MemberForm(instance=member)
        for field in member_form.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True

        context['member'] = member
        context['member_form'] = member_form
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        member = get_object_or_404(Member, pk=pk)

        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.member = member
            transaction.created_by = request.user
            transaction.save()
            return redirect(self.get_success_url())

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class TransactionReturnView(LibrarianTransactionsMixin, LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['returned']
    template_name = 'transactions/transaction_return.html'

    def get_success_url(self):
        member_id = self.object.member.pk
        return reverse_lazy('members:detail', kwargs={'pk': member_id})


