from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField # pip install django-multiselectfield

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

MILITARY_STATUS_CHOICES = [
    ('VET', 'Veteran'),
    ('ACTIVE', 'Active Military'),
    ('NONE', 'None')
]

MARITAL_STATUS_CHOICES = [
    ('Single', 'Single'),
    ('Married', 'Married'),
]
CITIZENSHIP_CHOICES = [
    ('US', 'US Citizen'),
    ('International', 'International'),
]

STATE_CHOICES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'Washington, D.C.'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]

LOCATION_PREFERENCE_CHOICES = [
    ('Current', 'Within 50 miles of current location'),
    ('Regional', 'Regional'),
    ('National', 'National'),
    ('International', 'International'),
]

SIZE_PREFERENCE_CHOICES = [
    ('<1500', 'Under 1500 undergraduates'),
    ('1500-5000', '1500-5000 undergraduates'),
    ('>5000', 'More than 5000 undergraduates'),
]

DEGREE_CHOICES = [
    ("B.Arch.", "Bachelor of Architecture (B.Arch.)"),
    ("B.A.", "Bachelor of Arts (B.A.)"),
    ("B.B.", "Bachelor of Business (B.B.)"),
    ("B.B.A.", "Bachelor of Business Administration (B.B.A.)"),
    ("B.S.B.", "Bachelor of Science in Business (B.S.B.)"),
    ("B.C.L.", "Bachelor of Canon Law (B.C.L.)"),
    ("B.C.S.", "Bachelor of Computer Science (B.C.S.)"),
    ("B.S.C.S.", "Bachelor of Science in Computer Science (B.S.C.S.)"),
    ("B.C.J.", "Bachelor of Criminal Justice (B.C.J.)"),
    ("B.S.C.J.", "Bachelor of Science in Criminal Justice (B.S.C.J.)"),
    ("B.D.", "Bachelor of Divinity (B.D.)"),
    ("B.Ed.", "Bachelor of Education (B.Ed.)"),
    ("B.S.Ed.", "Bachelor of Science in Education (B.S.Ed.)"),
    ("B.W.E.", "Bachelor of Wireless Engineering (B.W.E.)"),
    ("B.E.", "Bachelor of Engineering (B.E./B.Eng.)"),
    ("B.S.E.", "Bachelor of Science in Engineering (B.S.E./B.S.EN.)"),
    ("B.S.A.E.", "Bachelor of Science in Aerospace Engineering (B.S.A.E.)"),
    ("B.S.Ag.E.", "Bachelor of Science in Agricultural Engineering (B.S.Ag.E.)"),
    ("B.S.B.S.", "Bachelor of Science in Biological Systems (B.S.B.S.)"),
    ("B.S.B.A.E.", "Bachelor of Science in Biosystems and Agricultural Engineering (B.S.B.A.E.)"),
    ("B.S.B.E.", "Bachelor of Science in Biological Engineering (B.S.B.E.)"),
    ("B.B.m.E.", "Bachelor of Biomedical Engineering (B.B.m.E.)"),
    ("B.S.B.M.E.", "Bachelor of Science in Biomedical Engineering (B.S.B.E./B.S.B.M.E.)"),
    ("B.S.Ch.E.", "Bachelor of Science in Chemical Engineering (B.S.Ch.E.)"),
    ("B.S.Ch.B.E.", "Bachelor of Science in Chemical and Biomolecular Engineering (B.S.Ch.B.E.)"),
    ("B.S.C.M.E.", "Bachelor of Science in Chemical and Materials Engineering (B.S.C.M.E.)"),
    ("B.C.E.", "Bachelor of Civil Engineering (B.C.E.)"),
    ("B.S.C.E.", "Bachelor of Science in Civil Engineering (B.S.C.E.)"),
    ("B.S.-C.I.E.", "Bachelor of Science in Civil and Infrastructure Engineering (B.S.-C.I.E.)"),
    ("B.Comp.E.", "Bachelor of Computer Engineering (B.Comp.E.)"),
    ("B.S.Cmp.E.", "Bachelor of Science in Computer Engineering (B.S.C.E./B.S.Cmp.E.)"),
    ("B.S.C.S.E.", "Bachelor of Science in Computer Science and Engineering (B.S.C.S.E.)"),
    ("B.S.E.C.E.", "Bachelor of Science in Electrical and Computer Engineering (B.S.E.C.E.)"),
    ("B.E.E.", "Bachelor of Electrical Engineering (B.E.E.)"),
    ("B.S.E.E.", "Bachelor of Science in Electrical Engineering (B.S.E.E.)"),
    ("B.S.E.Mgt.", "Bachelor of Science in Engineering Management (B.S.E.Mgt.)"),
    ("B.S.En.E.", "Bachelor of Science in Environmental Engineering (B.S.En.E./B.S.Env.E.)"),
    ("B.F.E.", "Bachelor of Fiber Engineering (B.F.E.)"),
    ("B.S.I.E.", "Bachelor of Science in Industrial Engineering (B.S.I.E.)"),
    ("B.S.Mfg.E.", "Bachelor of Science in Manufacturing Engineering (B.S.Mfg.E.)"),
    ("B.S.M.S.E.", "Bachelor of Science in Manufacturing Systems Engineering (B.S.M.S.E.)"),
    ("B.S.M.S.E.", "Bachelor of Science in Materials Science and Engineering (B.S.M.S.E.)"),
    ("B.S.MA.E.", "Bachelor of Science in Materials Engineering (B.S.MA.E.)"),
    ("B.M.E.", "Bachelor of Mechanical Engineering (B.M.E.)"),
    ("B.S.M.E.", "Bachelor of Science in Mechanical Engineering (B.S.M.E.)"),
    ("B.S.Mt.E.", "Bachelor of Science in Metallurgical Engineering (B.S.Mt.E.)"),
    ("B.S.MI.E.", "Bachelor of Science in Mining Engineering (B.S.MI.E.)"),
    ("B.S.-SYST.", "Bachelor of Science in Systems (B.S.-SYST.)"),
    ("B.S.W.E.", "Bachelor of Software Engineering (B.S.W.E.)"),
    ("B.S.S.E.", "Bachelor of Science in Software Engineering (B.S.S.E.)"),
    ("B.S.E.", "Bachelor of Systems Engineering (B.S.E.)"),
    ("B.S.S.E.", "Bachelor of Science in Systems Engineering (B.S.S.E.)"),
    ("B.E.T.", "Bachelor of Engineering Technology (B.E.T.)"),
    ("B.S.E.T.", "Bachelor of Science in Engineering Technology (B.S.E.T.)"),
    ("B.S.C.E.T.", "Bachelor of Science in Civil Engineering Technology (B.S.C.E.T./B.S.Civ.E.T.)"),
    ("B.S.C.E.T.", "Bachelor of Science in Computer Engineering Technology (B.S.C.E.T.)"),
    ("B.S.Con.E.T.", "Bachelor of Science in Construction Engineering Technology (B.S.Con.E.T.)"),
    ("B.S.D.D.T.", "Bachelor of Science in Drafting Design Technology (B.S.D.D.T.)"),
    ("B.S.E.T.", "Bachelor of Science in Electrical/Electronics Technology (B.S.E.T.)"),
    ("B.S.E.E.T.", "Bachelor of Science in Electrical Engineering Technology (B.S.E.E.T.)"),
    ("B.S.E.M.E.T.", "Bachelor of Science in Electro-Mechanical Engineering Technology (B.S.E.M.E.T.)"),
    ("B.S.M.E.T.", "Bachelor of Science in Mechanical Engineering Technology (B.S.M.E.T.)"),
    ("B.F.A.", "Bachelor of Fine Arts (B.F.A.)"),
    ("B.F.", "Bachelor of Forestry (B.F.)"),
    ("B.S.For.Res.", "Bachelor of Science in Forest Research (B.S.For.Res.)"),
    ("B.H.L.", "Bachelor of Hebrew Letters (B.H.L.)"),
    ("B.J.", "Bachelor of Journalism (B.J.)"),
    ("LL.B.", "Bachelor of Laws (LL.B.)"),
    ("B.L.S.", "Bachelor of Liberal Studies (B.L.S.)"),
    ("B.Lit.", "Bachelor of Literature (B.Lit.)"),
    ("B.M.S.", "Bachelor of Marine Science (B.M.S.)"),
    ("B.M.", "Bachelor of Music (B.M.)"),
    ("B.N.", "Bachelor of Nursing (B.N.)"),
    ("B.S.N.", "Bachelor of Science in Nursing (B.S.N.)"),
    ("B.Pharm.", "Bachelor of Pharmacy (B.Pharm.)"),
    ("B.Phil.", "Bachelor of Philosophy (B.Phil.)"),
    ("B.R.E.", "Bachelor of Religious Education (B.R.E.)"),
    ("B.S.", "Bachelor of Science (B.S.)"),
    ("B.S.Ch.", "Bachelor of Science in Chemistry (B.S.Ch.)"),
    ("B.T.", "Bachelor of Technology (B.T./B.Tech.)"),
    ("unknown", "Unknown"),
]

TERM_CHOICES = [
    ('spring', 'Spring'),
    ('summer', 'Summer'),
    ('fall', 'Fall'),
    ('winter', 'Winter'),
]


# Represents an institution profile
class UniversityProfile(models.Model):
    university_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
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
    special_transfer_support = models.TextField(blank=True, null=True)
    contingent_admission = models.TextField(blank=True, null=True)
    online_allowed = models.BooleanField(default=False)
    degree_pathways_for_AAS_student = models.TextField(blank=True, null=True)
    grad_pathway = models.TextField(blank=True, null=True)
    honor_to_honor_pathway = models.TextField(blank=True, null=True)
    institutional_strength_and_highlight = models.TextField(blank=True, null=True)
    graduation_rate = models.FloatField(blank=True, null=True)
    retention_rate = models.FloatField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_partner = models.BooleanField(default=False)

    def __str__(self):
        return self.university_name

  
class CollegeProfile(models.Model):
    college_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
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
    on_site_HS_available = models.BooleanField(default=False, blank=True)
    number_of_transfers_to_universities = models.IntegerField(blank=True, null=True)
    honors_program = models.BooleanField(default=False, blank=True)
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
    housing_for_international_students = models.BooleanField(default=False, blank=True)
    sports_teams = models.TextField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_partner = models.BooleanField(default=False)

    def __str__(self):
        return self.college_name
    
# Represents a user belonging to an institution
class UniversityUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=INSTITUTION_USER_ROLE)
    created_on = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only belong to an institution once
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'university'], name='unique_university_user')
        ]

    def __str__(self):
        return f"{self.user.username} at {self.university}"
    

class CollegeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=INSTITUTION_USER_ROLE)
    created_on = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only belong to an institution once
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'college'], name='unique_college_user')
        ]

    def __str__(self):
        return f"{self.user.username} at {self.college}"

# Represents an agreement between two institutions
class Agreement(models.Model):
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    university_program = models.CharField(max_length=100, blank=True, null=True)
    college_program = models.CharField(max_length=100, blank=True, null=True)
    credits = models.FloatField(blank=True, null=True)
    gpa_required = models.CharField(max_length=10, blank=True, null=True)
    effective_term = models.DateField(blank=True, null=True)

    # An agreement is unique between two programs
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['university', 'college', 'university_program', 'college_program'],
                name='unique_agreement'
            )
        ]
   
    def __str__(self):
        return f"Agreement between {self.university} and {self.college}"

# Represents a course 
class UniversityCourse(models.Model):
    institution = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=10)
    digit_code = models.CharField(max_length=10)
    credits = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject_code} {self.digit_code}"
    
class CollegeCourse(models.Model):
    institution = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=10)
    digit_code = models.CharField(max_length=10)
    credits = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject_code} {self.digit_code}"
    
# Represents a course equivalency between two institutions
class AgreementCourse(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, null=True)
    college_course = models.ForeignKey(CollegeCourse, on_delete=models.CASCADE, null=True)
    university_course = models.ForeignKey(UniversityCourse, on_delete=models.CASCADE, null=True)
    credits = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.college_course} ↔ {self.university_course} in {self.agreement}"
 


   
# Represents a student profile
class StudentProfile(models.Model):
    # required info for registration
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    preferred_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_TYPE)
    # institution = models.CharField(max_length=50, blank=True, null=True)
    institution = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
   
    # student demographic information
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    military_status = models.CharField(max_length=20, choices=MILITARY_STATUS_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    dependent_children_num = models.IntegerField(blank=True, null=True)
    race = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    citizenship_status = models.CharField(max_length=20, choices=CITIZENSHIP_CHOICES, blank=True, null=True)
    is_enrolled_in_college = models.BooleanField(default=False, blank=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.CharField(max_length=10, blank=True, null=True)
    college_credits_num = models.IntegerField(blank=True, null=True)
    target_transfer_date = models.DateField(blank=True, null=True)
    
    # student preferences
    location_preference = models.CharField(max_length=20, choices=LOCATION_PREFERENCE_CHOICES, blank=True, null=True)
    size_preference = models.CharField(max_length=20, choices=SIZE_PREFERENCE_CHOICES, blank=True, null=True)
    degree_preference = MultiSelectField(choices=DEGREE_CHOICES, blank=True)
    graduate_pathway_preference = models.BooleanField(default=False, blank=True)
    career_objective = models.TextField(blank=True, null=True)
    is_fafsa_completed = models.BooleanField(default=False, blank=True)
    expected_family_contribution = models.IntegerField(blank=True, null=True)
    estimated_affordable_amount = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.institution}"
    
# Represents the courses a student has taken
class StudentCourse(models.Model):

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(CollegeCourse, on_delete=models.CASCADE, null=True, blank=True)
    course_code = models.CharField(max_length=20, null=True)
    grade = models.CharField(max_length=5)
    taken_year = models.IntegerField(null=True) 
    taken_term = models.CharField(max_length=10, choices=TERM_CHOICES, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student} - {self.course} ({self.taken_year}, {self.taken_term})"