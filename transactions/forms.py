from django import forms
from django.utils import timezone
from .models import Transaction
from datetime import timedelta


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book_title', 'book_id', 'return_due_date']
        widgets = {
            'book_title': forms.TextInput(attrs={'class': 'form-control'}),
            'book_id': forms.TextInput(attrs={'class': 'form-control'}),
            'return_due_date': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker'}
            ),
        }
        labels = {
            'book_title': 'Kitob nomi',
            'book_id': 'Kitob ID',
            'return_due_date': 'Qaytarish muddati',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            default_due = timezone.now() + timedelta(days=7)
            self.initial.setdefault(
                'return_due_date',
                default_due.strftime('%Y-%m-%d %H:%M')
            )

    def clean_return_due_date(self):
        return_due_date = self.cleaned_data.get('return_due_date')
        if not return_due_date:
            raise forms.ValidationError("Qaytarish muddati majburiy")
        if return_due_date <= timezone.now():
            raise forms.ValidationError("Qaytarish muddati hozirgi vaqtdan keyin bo‘lishi kerak")
        return return_due_date


class TransactionReturnForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['returned']
        labels = {
            'returned': 'Kitob qaytarildi',
        }
        widgets = {
            'returned': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'id': 'returned-id'}
            ),
        }

    def clean_returned(self):
        returned = self.cleaned_data.get('returned')
        if self.instance.returned and returned:
            raise forms.ValidationError("Bu kitob allaqachon qaytarilgan")
        return returned

