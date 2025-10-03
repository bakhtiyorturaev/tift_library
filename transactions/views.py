from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from dashboard.mixins import LibrarianTransactionsMixin
from django.urls import reverse_lazy, reverse
from members.forms import MemberForm
from django.contrib import messages
from .forms import TransactionForm
from django.utils import timezone
from members.models import Member
from .models import Transaction
from django.views import View
from django.db.models import Q


class TransactionListView(LibrarianTransactionsMixin, LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request.GET

        search_query = request.get('search_query')
        returned = request.get('returned')
        given_from = request.get('given_from')
        given_to = request.get('given_to')

        # Qidiruv
        if search_query:
            queryset = queryset.filter(
                Q(book_title__icontains=search_query) |
                Q(member__full_name__icontains=search_query) |
                Q(member__student_id__icontains=search_query) |
                Q(member__phone__icontains=search_query)
            )

        # Holat bo‘yicha filter
        now = timezone.now()

        if returned == 'True':  # Qaytarilgan
            queryset = queryset.filter(returned=True)
        elif returned == 'False':  # Faol
            queryset = queryset.filter(returned=False)
        elif returned == 'overdue':  # Muddati o'tgan
            queryset = queryset.filter(returned=False, return_due_date__lt=now)

        # Sana filterlari
        if given_from:
            queryset = queryset.filter(given_at__date__gte=given_from)
        if given_to:
            queryset = queryset.filter(given_at__date__lte=given_to)

        return queryset.order_by('returned', 'return_due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request.GET
        context.update({
            'search_query': request.get('search_query', ''),
            'returned': request.get('returned', ''),
            'given_from': request.get('given_from', ''),
            'given_to': request.get('given_to', ''),
        })
        return context



class TransactionCreateView(LibrarianTransactionsMixin, LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('member_form', kwargs.get('member_form') or MemberForm())
        context['members'] = Member.objects.all()[:10]
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        member_form = MemberForm(request.POST)
        transaction_form = TransactionForm(request.POST)

        # Talabani ID bo‘yicha olish yoki yaratish
        student_id = request.POST.get('student_id')
        member = None
        if student_id:
            member = Member.objects.filter(student_id=student_id).first()
            if member:
                member_form = MemberForm(request.POST, instance=member)

        if member_form.is_valid() and transaction_form.is_valid():
            # Talabani saqlash
            member = member_form.save(commit=False)
            member.created_by = request.user
            member.save()

            # Ijarani saqlash
            transaction = transaction_form.save(commit=False)
            transaction.member = member
            transaction.created_by = request.user
            transaction.save()

            messages.success(request, "Ijara muvaffaqiyatli qo‘shildi ✅")
            return self.form_valid(transaction_form)

        messages.error(request, "Ma‘lumotlarni tekshiring ❌")
        return self.form_invalid(transaction_form, member_form)

    def form_invalid(self, transaction_form, member_form):
        """Ikkala formani qayta render qilish"""
        return self.render_to_response(
            self.get_context_data(
                form=transaction_form,
                member_form=member_form
            )
        )

class TransactionCreateForStudentView(LibrarianTransactionsMixin, LoginRequiredMixin, FormView):
    template_name = 'transactions/transaction_form_for_student.html'
    form_class = TransactionForm

    def get_success_url(self):
        return reverse('members:detail', kwargs={'pk': self.kwargs['pk']})

    def get_member(self):
        return get_object_or_404(Member, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_member()
        member_form = MemberForm(instance=member)

        # readonly / disabled qo‘shib qo‘yish
        for name, field in member_form.fields.items():
            field.widget.attrs.update({
                'readonly': True,
                'disabled': True
            })

        context.update({
            'member': member,
            'member_form': member_form,
        })
        return context

    def form_valid(self, form):
        member = self.get_member()
        transaction = form.save(commit=False)
        transaction.member = member
        transaction.created_by = self.request.user
        transaction.save()

        messages.success(self.request, "Ijara muvaffaqiyatli qo‘shildi ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Xatolik ❌ Ma‘lumotlarni tekshiring.")
        return super().form_invalid(form)


class BulkConfirmView(View):
    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist("loans")
        redirect_to = request.POST.get("redirect_to")

        if not selected_ids:
            messages.warning(request, "❌ Hech qanday kitob tanlanmadi")
            if redirect_to == "overdue":
                return redirect(reverse("dashboard:dashboard") + "?overdue=true")
            elif redirect_to == "due_soon":
                return redirect(reverse("dashboard:dashboard") + "?due_soon=true")
            return redirect(reverse("transactions:list"))

        # Tanlangan transactionlarni qaytarilgan qilib belgilash
        Transaction.objects.filter(pk__in=selected_ids).update(returned=True)

        messages.success(request, f"✅ {len(selected_ids)} ta kitob qaytarildi")
        if redirect_to == "overdue":
            return redirect(reverse("dashboard:dashboard") + "?overdue=true")

        elif redirect_to == "due_soon":
            return redirect(reverse("dashboard:dashboard") + "?due_soon=true")

        return redirect(reverse("transactions:list"))
