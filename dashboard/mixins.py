class LibrarianTransactionsMixin:
    """
    Faqat hozirgi foydalanuvchining yozuvlarini ko'rsatish uchun mixin.
    Faqat kutubxonachi (is_librarian=True) uchun amal qiladi,
    aks holda bo'sh queryset qaytaradi.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated and user.is_librarian:
            return qs.filter(created_by=user)
        return qs.none()

