from django.db import models
from users.models import BusinessProfile, User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Service(models.Model):
    fkBusiness = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.FloatField(validators=[MinValueValidator(5)])
    description = models.TextField(max_length=300, null=False)
    duration = models.DurationField()
    
    def __str__(self):
        return f"{self.name} - {self.fkBusiness.business_name}"

class CommentsOnService(models.Model):
    fkClient = models.ForeignKey(User, on_delete=models.CASCADE)
    fkService = models.ForeignKey(Service, on_delete=models.CASCADE)
    desc = models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"Comment by {self.fkClient.email} on {self.fkService.name}"