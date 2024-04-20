from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to="media/",default='avatar/default.png')
    added_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True,null=True)
    adress= models.CharField(max_length=255,blank=True,null=True)

class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(auto_now_add=True)
    departure_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.arrival_time and not self.departure_time:
            current_time = timezone.now()
            last_attendance = Attendance.objects.filter(staff=self.staff).order_by('-arrival_time').first()
            if last_attendance and last_attendance.departure_time is None:
                last_attendance.departure_time = current_time
                last_attendance.save()
                super(Attendance, self).save(*args, **kwargs)
            else:
                super(Attendance, self).save(*args, **kwargs)
        else:
            super(Attendance, self).save(*args, **kwargs)
