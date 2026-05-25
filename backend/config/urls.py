from django.contrib import admin
from django.urls import path
from emissions.views import dashboard, upload_csv, records, approve_record

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dashboard/', dashboard),
    path('api/upload/', upload_csv),
    path('api/records/', records),
    path('api/approve/<int:record_id>/', approve_record),
]