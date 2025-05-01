from django.db import models

# Create your models here.

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    month_name = models.CharField(max_length=255, default='January')
    year_name = models.CharField(max_length=4, default='2023')

    def __str__(self):
        return f"{self.name} - {self.month_name} {self.year_name}"


