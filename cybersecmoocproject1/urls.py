from django.contrib import admin
from django.urls import path, include

# A05:2021 – Security Misconfiguration
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('brokensite.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]
