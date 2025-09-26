from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django import forms

from .models import Transaction
from users.models import User


class TransferTransactionsForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    new_user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_librarian=True),
        label="Kutubxonchi"
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'member', 'given_at', 'created_by', 'returned')
    list_filter = ('returned', 'created_by')
    search_fields = ('book_title', 'book_id', 'member__ful_name',)
    raw_id_fields = ('member',)
    actions = ['transfer_transactions_action']
    list_per_page = 20

    def transfer_transactions_action(self, request, queryset):
        """
        Action orqali ijaralarni yangi kutubxonchiga topshirish formini ko‘rsatish.
        """
        selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
        return redirect(f'./transfer_transactions/?_selected_action={",".join(selected)}')

    transfer_transactions_action.short_description = "Tanlangan ijaralarni boshqa kutubxonchiga topshirish"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'transfer_transactions/',
                self.admin_site.admin_view(self.transfer_transactions_view),
                name='transactions_transaction_transfer',
            )
        ]
        return custom_urls + urls

    def transfer_transactions_view(self, request):
        selected_ids = request.GET.get('_selected_action') or request.POST.get('_selected_action')
        if selected_ids:
            selected_ids = selected_ids.split(',')
            queryset = Transaction.objects.filter(pk__in=selected_ids)
        else:
            self.message_user(request, "Hech qanday element tanlanmagan.", level=messages.WARNING)
            return redirect('admin:transactions_transaction_changelist')

        from members.models import Member
        members = Member.objects.filter(transaction__in=queryset).distinct()
        member_count = members.count()

        if request.method == 'POST':
            form = TransferTransactionsForm(request.POST)
            if form.is_valid():
                new_user = form.cleaned_data['new_user']
                count = queryset.update(created_by=new_user)
                updated_members = members.update(created_by=new_user)

                self.message_user(
                    request,
                    f"{count} ta ijara va {updated_members} ta talaba muvaffaqiyatli yangi kutubxonchiga o'tkazildi.",
                    level=messages.SUCCESS
                )
                return redirect('admin:transactions_transaction_changelist')
        else:
            form = TransferTransactionsForm(initial={'_selected_action': ",".join(selected_ids)})

        return render(request, 'admin/transfer_transactions.html', {
            'form': form,
            'transactions': queryset,
            'member_count': member_count,
            'total_count': queryset.count(),
            'title': 'Tanlangan ijaralarni boshqa kutubxonchiga o‘tkazish',
        })

