from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_name', 'student_id', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '901234567',
                    'maxlength': '9',
                }
            ),
        }
        labels = {
            'full_name': 'Ism Familiya',
            'student_id': 'Talaba ID',
            'phone': 'Telefon raqami',
        }


    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').replace(' ', '')
        if not phone.isdigit() or len(phone) != 9:
            raise forms.ValidationError(
                "Telefon raqami faqat 9 xonali bo‘lishi kerak va O‘zbekiston operatorlaridan biri bilan boshlanishi kerak. Masalan: 90 1234567"
            )

        valid_prefixes = ['20', '36', '33', '50', '55', '61', '62', '65', '66', '67', '69', '70', '71', '72', '73',
                          '74', '75', '76', '77', '78', '79', '88', '90', '91', '93', '94', '95', '97', '98', '99']
        if phone[:2] not in valid_prefixes:
            raise forms.ValidationError(
                "Telefon raqami O‘zbekiston operatorlaridan biri bilan boshlanishi kerak. Masalan: 90 1234567"
            )

        return phone


