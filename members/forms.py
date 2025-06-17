from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,  # agar to'ldirish majburiy bo'lsa
        label='Ism Familiya',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Talaba ismi va familiyasini yozing, agar mavjud bo‘lsa bazadan tanlanadi'
    )

    class Meta:
        model = Member
        fields = ['full_name', 'student_id', 'phone']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Ism Familiya',
            'student_id': 'Talaba ID',
            'phone': 'Telefon raqami',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.phone:
            phone = self.instance.phone
            if phone.startswith('+998'):
                self.initial['phone'] = phone[4:]

    # Misol uchun, qo'shimcha validatsiya (majburiy to'ldirish)
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise forms.ValidationError("Ism Familiya maydoni bo‘sh bo‘lishi mumkin emas.")
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError("Telefon raqami majburiy maydon.")
        # Qo'shimcha telefon raqami validatsiyasi kiritilishi mumkin
        return phone
