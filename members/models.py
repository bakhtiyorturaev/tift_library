from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

class Member(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Ism Familiyasi')
    student_id = models.CharField(max_length=12, unique=True, verbose_name='Talaba ID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='members'
    )
    phone = models.CharField(
        unique=True,
        max_length=13,
        verbose_name='Telefon raqami',
        validators=[RegexValidator(
            regex='^[0-9]{9}$',
            message='Faqat 9 xonali raqam kiriting, masalan: 901234567'
        )]
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+998'):
            phone = '+998'+phone
        return phone

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'

    def __str__(self):
        return f"{self.full_name} - {self.phone}"