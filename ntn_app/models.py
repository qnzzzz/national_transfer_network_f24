from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class TwoYearCollege(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    website = models.URLField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_title = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    hashed_password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class FourYearUniversity(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    website = models.URLField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_title = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    hashed_password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Agreement relationship
class Agreement(models.Model):
    university = models.ForeignKey(FourYearUniversity, on_delete=models.CASCADE)
    college = models.ForeignKey(TwoYearCollege, on_delete=models.CASCADE)
    effective_term = models.DateField()

    def __str__(self):
        return f"Agreement between {self.university} and {self.college}"

class Course(models.Model):
    # ContentType and Object ID for the generic relation
    school_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    school_object_id = models.PositiveIntegerField()
    school = GenericForeignKey('school_content_type', 'school_object_id')
    
    subject_code = models.CharField(max_length=10)
    digit_code = models.CharField(max_length=10)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.subject_code} {self.digit_code}"
    
# Course conversion relationship
class AgreementCourse(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    course_1 = models.ForeignKey(Course, related_name='agreement_course_1', on_delete=models.CASCADE)
    course_2 = models.ForeignKey(Course, related_name='agreement_course_2', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_1} ↔ {self.course_2} in {self.agreement}"

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    preferred_city = models.CharField(max_length=255)
    preferred_major = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

