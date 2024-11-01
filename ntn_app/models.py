from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

# Create your models here.

# INSTITUTION_TYPE = [
#     ('college', 'Two Year College'),
#     ('university', 'Four Year University'),
# ]

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
class UniversityProfile(models.Model):
    university_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    website = models.URLField()
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    contact_title = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo_image = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='institution_banners/', blank=True, null=True)
    UGs = models.IntegerField(blank=True, null=True)
    number_of_transfers_per_year = models.IntegerField(blank=True, null=True)
    housing_availability = models.BooleanField(default=False)
    marriage_or_kids_support = models.TextField(blank=True, null=True)
    vets_support = models.TextField(blank=True, null=True)
    aids_or_scholarships_for_transfers = models.TextField(blank=True, null=True)
    special_transfer_program = models.TextField(blank=True, null=True)
    contigent_admission = models.TextField(blank=True, null=True)
    online_allowed = models.BooleanField(default=False)
    degree_pathways_for_AAS_student = models.TextField(blank=True, null=True)
    grad_pathway = models.TextField(blank=True, null=True)
    honor_to_honor_pathway = models.TextField(blank=True, null=True)
    institutional_strength_and_highlight = models.TextField(blank=True, null=True)
    graduation_rate = models.FloatField(blank=True, null=True)
    rentation_rate = models.FloatField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.institution_name} ({self.get_institution_type_display()})"
    
class CollegeProfile(models.Model):
    college_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    website = models.URLField()
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    contact_title = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo_image = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='institution_banners/', blank=True, null=True)
    total_enrollment = models.IntegerField(blank=True, null=True)
    full_time_students = models.IntegerField(blank=True, null=True)
    part_time_students = models.IntegerField(blank=True, null=True)
    HS_dual_enrollment = models.BooleanField(default=False)
    on_site_HS_available = models.BooleanField(default=False)
    number_of_transfers_to_univerisities = models.IntegerField(blank=True, null=True)
    honors_program = models.BooleanField(default=False)
    enrolled_honors_students = models.IntegerField(blank=True, null=True)
    top1_transfer_partner = models.CharField(max_length=100, blank=True, null=True)
    top2_transfer_partner = models.CharField(max_length=100, blank=True, null=True)
    top3_transfer_partner = models.CharField(max_length=100, blank=True, null=True)
    required_courses_for_transfer = models.TextField(blank=True, null=True)
    head_of_transfer_advising = models.CharField(max_length=50, blank=True, null=True)
    statewide_mandated_pathways = models.TextField(blank=True, null=True)
    own_bachelor_degree = models.TextField(blank=True, null=True)
    three_plus_one_program = models.TextField(blank=True, null=True)
    assured_enrollment = models.TextField(blank=True, null=True)
    AAS_pathways = models.TextField(blank=True, null=True)
    dual_enrollment_with_university = models.TextField(blank=True, null=True)
    direct_grad_pathways = models.TextField(blank=True, null=True)
    honor_to_honor_pathways = models.TextField(blank=True, null=True)
    college_strength = models.TextField(blank=True, null=True)
    housing_for_international_students = models.BooleanField(default=False)
    sports_teams = models.TextField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.institution_name} ({self.get_institution_type_display()})"

# Represents a user belonging to an institution
class UniversityUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=INSTITUTION_USER_ROLE)
    created_on = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only belong to an institution once
    class Meta:
        unique_together = ('user', 'university') 

    def __str__(self):
        return f"{self.user.username} at {self.university}"
    

class CollegeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=INSTITUTION_USER_ROLE)
    created_on = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only belong to an institution once
    class Meta:
        unique_together = ('user', 'college') 

    def __str__(self):
        return f"{self.user.username} at {self.college}"

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
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    prefered_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_TYPE)
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.CASCADE)
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