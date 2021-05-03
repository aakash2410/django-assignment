from django.db import models
from django.contrib.auth.models import User

class Advisor(models.Model):
    advisor_name = models.CharField(max_length = 32, blank = False)
    advisor_photo_url = models.URLField(max_length=200, blank = False)

    def __str__(self):
        return "{}".format(self.advisor_name)

class AdvisorUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    advisor_id = models.ForeignKey(Advisor, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.advisor_id.advisor_name)

class Bookings(models.Model):
    advisor_user_id = models.ForeignKey(AdvisorUser, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return "{}".format(self.date_and_time)


# Create your models here.
