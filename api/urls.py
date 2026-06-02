from django.urls import path, include
from api.views import csrf_init

urlpatterns = [
    path('csrf-init/', csrf_init, name='csrf_init'),
    path('auth/', include('accounts.urls')),
]
