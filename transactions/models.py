from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from members.models import Member
from django.db import models

class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Talaba')
    book_title = models.CharField(max_length=200, verbose_name='Kitob nomi')
    book_id = models.CharField(max_length=50, verbose_name='Kitob ID')
    given_at = models.DateTimeField(auto_now_add=True, verbose_name='Berilgan vaqt')
    return_due_date = models.DateTimeField(verbose_name='Qaytarish muddati')
    returned = models.BooleanField(default=False, verbose_name='Qaytarilgan')
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

    def get_status(self):
        """
        Ijara holatini aniqlaydi va qaytaradi:
        - status: 'returned', 'today', 'tomorrow', 'overdue', 'future'
        - is_overdue: True/False
        """
        now = timezone.now()
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        # Lokal vaqt
        local_due = timezone.localtime(self.return_due_date)

        # Status aniqlash
        if self.returned:
            status = "returned"
        elif local_due.date() < today:
            status = "overdue"
        elif local_due.date() == today:
            status = "today"
        elif local_due.date() == tomorrow:
            status = "tomorrow"
        else:
            status = "future"

        # is_overdue flag
        is_overdue = (status == "overdue")

        return {
            "status": status,
            "is_overdue": is_overdue
        }

    @property
    def overdue_days(self):
        """Agar ijaraning muddati o'tgan bo'lsa, necha kun o'tganini qaytaradi"""
        if self.returned or self.return_due_date >= timezone.now():
            return 0
        delta = timezone.now() - self.return_due_date
        return delta.days

    @property
    def days_remaining_display(self):
        """Inson o‘qiydigan shaklda"""
        status = self.get_status()['status']  # <-- shu yer
        if self.returned:
            return "Topshirilgan"
        elif status == "today":
            return "Bugun"
        elif status == "tomorrow":
            return "Ertaga"
        elif status == "overdue":
            days_overdue = (timezone.localdate() - timezone.localtime(self.return_due_date).date()).days
            return f"{days_overdue} kun o'tgan"
        else:
            days_remaining = (timezone.localtime(self.return_due_date).date() - timezone.localdate()).days
            return f"{days_remaining} kun qoldi"


