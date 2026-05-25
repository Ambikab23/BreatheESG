from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DataSource(models.Model):
    SOURCE_TYPES = [
        ('SAP', 'SAP Fuel/Procurement'),
        ('UTILITY', 'Utility Electricity'),
        ('TRAVEL', 'Corporate Travel'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type} - {self.file_name}"


class EmissionRecord(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FLAGGED', 'Flagged'),
        ('APPROVED', 'Approved'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)

    scope = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)

    raw_value = models.FloatField()
    raw_unit = models.CharField(max_length=50)

    normalized_value = models.FloatField()
    normalized_unit = models.CharField(max_length=50)

    is_suspicious = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.status}"


class AuditLog(models.Model):
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE)

    action = models.CharField(max_length=100)

    changed_by = models.CharField(
        max_length=100,
        default="analyst"
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action