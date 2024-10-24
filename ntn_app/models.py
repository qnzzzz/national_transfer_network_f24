from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

# Create your models here.

INSTITUTION_TYPE = [
    ('college', 'Two Year College'),
    ('university', 'Four Year University'),
]

# Represents an institution profile
class InstitutionProfile(models.Model):
    # use django built-in User model to store user credentials
    # user has a one-to-one relationship with InstitutionProfile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution_profile')
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPE) # two-year college or four-year university
    institution_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    website = models.URLField()
    contact_name = models.CharField(max_length=50)
    contact_title = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.institution_name} ({self.get_institution_type_display()})"

# Represents an agreement between two institutions
class Agreement(models.Model):
    university = models.ForeignKey(InstitutionProfile, limit_choices_to={'institution_type': 'university'}, on_delete=models.CASCADE)
    college = models.ForeignKey(InstitutionProfile, limit_choices_to={'institution_type': 'college'}, on_delete=models.CASCADE)
    effective_term = models.DateField()

    def __str__(self):
        return f"Agreement between {self.university} and {self.college}"

# Represents a course 
class Course(models.Model):
    school = models.ForeignKey(InstitutionProfile, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=10)
    digit_code = models.CharField(max_length=10)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.subject_code} {self.digit_code}"
    
# Represents a course equivalency between two institutions
class AgreementCourse(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    course_1 = models.ForeignKey(Course, related_name='agreement_course_1', on_delete=models.CASCADE)
    course_2 = models.ForeignKey(Course, related_name='agreement_course_2', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_1} ↔ {self.course_2} in {self.agreement}"
    
# Represents a student profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    major = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    preferred_city = models.CharField(max_length=255)
    preferred_major = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.institution}"