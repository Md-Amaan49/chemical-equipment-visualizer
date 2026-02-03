from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Dataset(models.Model):
    """Model for storing dataset metadata and summary statistics"""
    filename = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    record_count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Summary statistics
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    
    # Equipment type distribution (JSON field)
    type_distribution = models.JSONField()
    
    class Meta:
        ordering = ['-upload_timestamp']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_timestamp.strftime('%Y-%m-%d %H:%M')}"


class EquipmentRecord(models.Model):
    """Model for storing individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment_records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['equipment_name']
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"