from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from account.managers import CustomUserManager

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    role = models.CharField(choices=ROLE,  max_length=10)
    gender = models.CharField(choices=JOB_TYPE, max_length=1)
    location = models.CharField( max_length=100)
    skills = models.CharField( max_length=100)
    MobileNumber = models.CharField( max_length=100)
    Primary_school = models.CharField( max_length=200)
    High_school = models.CharField( max_length=200)
    Under_graduate = models.CharField( max_length=200)
    Post_graduate = models.CharField( max_length=200)
    Experience = models.CharField( max_length=200)
    AcademicProjects = models.CharField( max_length=200) 
    cv = models.FileField(upload_to='cv_uploads/', 
                          null=True, blank=True,
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()
