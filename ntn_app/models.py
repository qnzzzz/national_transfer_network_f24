from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

# Create your models here.

INSTITUTION_TYPE = [
    ('college', 'Two Year College'),
    ('university', 'Four Year University'),
]

INSTITUTION_USER_ROLE = [
    ('admin', 'Administrator'),
    ('faculty', 'Faculty'),
]

GENDER_TYPE = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


# Represents an institution profile
class InstitutionProfile(models.Model):
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPE) # two-year college or four-year university
    institution_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    website = models.URLField()
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    contact_title = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=Tru)
    logo_image = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='institution_banners/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.institution_name} ({self.get_institution_type_display()})"

# Represents a user belonging to an institution
class InstitutionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=INSTITUTION_USER_ROLE)
    created_on = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only belong to an institution once
    class Meta:
        unique_together = ('user', 'institution') 

    def __str__(self):
        return f"{self.user.username} at {self.institution}"

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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    prefered_name = models.CharField(max_length=50, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=GENDER_TYPE)
    preferred_city = models.CharField(max_length=255, blank=True, null=True)
    preferred_major = models.CharField(max_length=255, blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.institution}"
    
# Represents the courses a student has taken
class StudentCourse(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student} - {self.course}"