from django.db import models
from users.models import User, BusinessProfile
from offers.models import Service
# Create your models here.


class Reservation(models.Model):
    fkClient = models.ForeignKey(User, on_delete=models.CASCADE)
    fkService = models.ForeignKey(Service, on_delete=models.CASCADE)
    fkBusiness = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    def __str__(self):
        return f"Reservation for {self.fkClient.email} - {self.fkService.name} from {self.time_start} to {self.time_end}"