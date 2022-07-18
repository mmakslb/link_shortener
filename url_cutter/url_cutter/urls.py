from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_panel/', admin.site.urls),
    path('', include('cutter_app.urls')),
]
