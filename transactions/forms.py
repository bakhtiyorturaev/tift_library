from django import forms
from django.utils import timezone
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book_title', 'book_id', 'return_due_date']
        widgets = {
            'book_title': forms.TextInput(attrs={'class': 'form-control'}),
            'book_id': forms.TextInput(attrs={'class': 'form-control'}),
            'return_due_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }
        labels = {
            'book_title': 'Kitob nomi',
            'book_id': 'Kitob ID',
            'return_due_date': 'Qaytarish muddati',
        }


    def clean_return_due_date(self):
        return_due_date = self.cleaned_data['return_due_date']
        if return_due_date <= timezone.now():
            raise forms.ValidationError("Qaytarish muddati hozirgi vaqtdan keyin bo'lishi kerak")
        return return_due_date

class TransactionReturnForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['returned']
        labels = {
            'returned': 'Kitob qaytarildi',
        }
        widgets = {
            'returned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }