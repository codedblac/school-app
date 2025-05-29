from django.db import models
from accounts.models import CustomUser as User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    subject_specialization = models.CharField(max_length=100)
    classes = models.ManyToManyField('classes.SchoolClass', related_name='teachers')  # Lazy reference
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()
