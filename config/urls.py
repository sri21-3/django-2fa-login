"""
URL configuration for 2fa_email_login project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('', RedirectView.as_view(pattern_name='authentication:login', permanent=False)),
]
