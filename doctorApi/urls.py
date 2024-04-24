from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('doctorUser.urls')),
    path('api/', include('slotbook.urls')),
    path('api/', include('slotEntry.urls')),
    path('api/', include('report.urls')),


]
