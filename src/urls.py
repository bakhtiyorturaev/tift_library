from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('users.urls')),
    path('members/', include('members.urls')),
    path('transactions/', include('transactions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', RedirectView.as_view(url='dashboard/'), name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)