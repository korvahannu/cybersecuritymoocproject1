from django.contrib import admin
from django.urls import path, include

# A05:2021 – Security Misconfiguration
# Suppose this is a production application. Suppose this app uses default admin account of admin:admin.
# Two things that one should fix: remove the admin application, remove insecure admin credentials
# It is debatable whether admin app should exist on production level
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('brokensite.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]
