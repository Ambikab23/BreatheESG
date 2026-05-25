from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Company, DataSource, EmissionRecord, AuditLog
import pandas as pd


def dashboard(request):
    data = {
        "total_records": EmissionRecord.objects.count(),
        "approved": EmissionRecord.objects.filter(status='APPROVED').count(),
        "flagged": EmissionRecord.objects.filter(status='FLAGGED').count()
    }
    return JsonResponse(data)


def records(request):
    all_records = EmissionRecord.objects.all().order_by('-id')

    data = []
    for r in all_records:
        data.append({
            "id": r.id,
            "scope": r.scope,
            "category": r.category,
            "activity_type": r.activity_type,
            "raw_value": r.raw_value,
            "raw_unit": r.raw_unit,
            "normalized_value": r.normalized_value,
            "normalized_unit": r.normalized_unit,
            "is_suspicious": r.is_suspicious,
            "status": r.status,
            "source_type": r.source.source_type
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['file']
        source_type = request.POST.get('source_type', 'SAP')

        df = pd.read_csv(file)

        company, created = Company.objects.get_or_create(name="Demo Company")

        source = DataSource.objects.create(
            company=company,
            source_type=source_type,
            file_name=file.name
        )

        for index, row in df.iterrows():
            value = float(row['value'])

            if source_type == 'SAP':
                suspicious = value > 1000
                scope = 'Scope 1'
            elif source_type == 'UTILITY':
                suspicious = value > 5000
                scope = 'Scope 2'
            elif source_type == 'TRAVEL':
                suspicious = value > 10000
                scope = 'Scope 3'
            else:
                suspicious = False
                scope = 'Unknown'

            status = 'FLAGGED' if suspicious else 'PENDING'

            EmissionRecord.objects.create(
                company=company,
                source=source,
                scope=scope,
                category=row['category'],
                activity_type=row['activity_type'],
                raw_value=value,
                raw_unit=row['unit'],
                normalized_value=value,
                normalized_unit=row['unit'],
                is_suspicious=suspicious,
                status=status
            )

        return JsonResponse({"message": "CSV Uploaded Successfully"})

    return JsonResponse({"error": "Invalid request"})


@csrf_exempt
def approve_record(request, record_id):
    if request.method == 'POST':
        record = EmissionRecord.objects.get(id=record_id)
        record.status = 'APPROVED'
        record.save()

        AuditLog.objects.create(
            record=record,
            action="Record approved",
            changed_by="analyst"
        )

        return JsonResponse({"message": "Record approved successfully"})

    return JsonResponse({"error": "Invalid request"})