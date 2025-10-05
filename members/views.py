from django.db.models import Q, F, ExpressionWrapper, IntegerField, Case, When, Value
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.mixins import LibrarianTransactionsMixin
from django.db.models.functions import Now, TruncDate, ExtractDay
from django.core.paginator import Paginator
from django.views.generic.base import View
from transactions.models import Transaction
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .forms import MemberForm
from .models import Member
from django.utils import timezone
from datetime import timedelta

class MemberListView(LibrarianTransactionsMixin, LoginRequiredMixin, ListView):
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
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.object

        # Annotatsiya: qoldiq kun va muddati o'tganmi
        # loans = (
        #     Transaction.objects.filter(member=member)
        #     .annotate(
        #         days_left=ExpressionWrapper(
        #             ExtractDay(F("return_due_date")) - TruncDate(Now())+ Value(1),
        #             output_field=IntegerField(),
        #         ),
        #         is_overdue_db=Case(
        #             When(returned=False, return_due_date__lt=Now(), then=True),
        #             default=False,
        #             output_field=IntegerField(),
        #         ),
        #     )
        #     .order_by("returned", "return_due_date")
        # )

        loans = Transaction.objects.filter(member=member).order_by("returned", "return_due_date")

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)
        # Paginator
        paginator = Paginator(loans, self.paginate_by)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        context.update({
            "loans": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "paginator": paginator,
            "today": today,
            "tomorrow": tomorrow,
        })
        return context

class MemberUpdateView(LibrarianTransactionsMixin, LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/member_update_form.html'
    context_object_name = 'member'

    def get_success_url(self):
        return reverse('members:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if not form.has_changed():
            messages.info(self.request, "Hech qanday o‘zgarish kiritilmadi ❗")
            return redirect(self.get_success_url())
        messages.success(self.request, "Talaba ma’lumotlari muvaffaqiyatli yangilandi ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ma\'lumotlarni saqlashda xatolik yuz berdi! ❌')
        return super().form_invalid(form)

class ReturnMultipleView(LoginRequiredMixin, LibrarianTransactionsMixin, View):
    """
    Bir yoki bir nechta kitobni qaytarilgan deb belgilash uchun view.
    """
    def post(self, request, *args, **kwargs):
        loan_ids = request.POST.getlist("loans")

        if not loan_ids:
            messages.warning(request, "❌ Kitob tanlanmadi")
            return redirect(request.META.get("HTTP_REFERER", "members:list"))

        loans = Transaction.objects.filter(pk__in=loan_ids, returned=False)
        updated_count = loans.update(returned=True)

        if updated_count:
            messages.success(request, f"✅ {updated_count} ta kitob qaytarildi")
        else:
            messages.info(request, "⚠️ Tanlangan kitoblarning hammasi allaqachon qaytarilgan")

        return redirect(request.META.get("HTTP_REFERER", "members:list"))