from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from members.models import Member

class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Talaba')
    book_title = models.CharField(max_length=200, verbose_name='Kitob nomi')
    book_id = models.CharField(max_length=50, verbose_name='Kitob ID')
    given_at = models.DateTimeField(auto_now_add=True, verbose_name='Berilgan vaqt')
    return_due_date = models.DateTimeField(verbose_name='Qaytarish muddati')
    returned = models.BooleanField(default=False, verbose_name='Qaytarilganmi')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transactions',
        verbose_name='kim tomonidan'
    )

    class Meta:
        ordering = ['-given_at']
        verbose_name = 'Ijara'
        verbose_name_plural = 'Ijaralar'

    def __str__(self):
        return f"{self.book_title} - {self.book_id} - {self.member}"

    def is_overdue(self):
        return not self.returned and timezone.now() > self.return_due_date

    def days_remaining(self):
        if self.returned:
            return 0
        remaining = self.return_due_date - timezone.now()
        return remaining.days

    def is_due_soon(self):
        if self.returned:
            return False
        now = timezone.now()
        return now <= self.return_due_date <= now + timedelta(days=2)
