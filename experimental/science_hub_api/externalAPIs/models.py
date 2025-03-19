from django.db import models

class ApiKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    service_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    # Права доступа
    can_access_articles = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.service_name} - {self.key}"