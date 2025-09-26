from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Member(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Ism Familiyasi')
    student_id = models.CharField(max_length=12, unique=True, verbose_name='Talaba ID')
    phone = models.CharField(
        max_length=9,
        unique=True,
        verbose_name='Telefon raqami',
        validators=[RegexValidator(
            regex=r'^(20|36|33|50|55|61|62|65|66|67|69|70|71|72|73|74|75|76|77|78|79|88|90|91|93|94|95|97|98|99|)\d{7}$',
            message='Telefon raqami 9 xonali bo‘lishi kerak. Masalan: 91 1234567'
        )]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='members'
    )

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def formatted_phone(self):
        if self.phone and len(self.phone) == 9:
            return f"{self.phone[:2]} {self.phone[2:]}"
        return self.phone

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'

    def __str__(self):
        return f"{self.full_name} - {self.formatted_phone}"
