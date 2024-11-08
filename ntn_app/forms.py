from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UniversityProfile, CollegeProfile, UniversityUser, CollegeUser
from .models import UniversityProfile

INSTITUTION_TYPE_CHOICES = [
    ('university', 'University'),
    ('college', 'College'),
]

ROLE_CHOICES = [
    ('faculty', 'Faculty'),
    ('ADMIN', 'Admin'),
]


STATE_CHOICES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
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

class InstitutionRegistrationForm(forms.Form):
    # Institution details
    institution_name = forms.CharField(max_length=100, required=True, label="Institution Name")
    institution_type = forms.ChoiceField(choices=INSTITUTION_TYPE_CHOICES, required=True, label="Institution Type")
    
    # Contact person details
    email = forms.EmailField(required=True, label="Email")
    
    # User account details
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="User Role")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, user):
        institution_type = self.cleaned_data['institution_type']
        institution_name = self.cleaned_data['institution_name']
        email = self.cleaned_data['email']
        role = self.cleaned_data['role']

        # Create or get institution profile
        if institution_type == 'university':
            institution, created = UniversityProfile.objects.get_or_create(
                university_name=institution_name,
                defaults={
                    'email': email,
                }
            )
                
            # Link user with University
            UniversityUser.objects.get_or_create(
                user=user,
                university=institution,
                defaults={'role': role}
            )
            
        elif institution_type == 'college':
            institution, created = CollegeProfile.objects.get_or_create(
                college_name=institution_name,
                defaults={
                    'email': email,
                }
            )
            # Link user with College
            CollegeUser.objects.get_or_create(
                user=user,
                college=institution,
                defaults={'role': role}
            )

class InstitutionLoginForm(forms.Form):
    INSTITUTION_TYPE_CHOICES = [
        ('university', 'University'),
        ('college', 'College'),
    ]
    
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    institution_type = forms.ChoiceField(
        choices=INSTITUTION_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
                attrs={'class': "form-control"}
        )
    )
    password = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={
            'class': 'form-control'
            }
        )
    )

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data



# University Profile Forms

# University's basic info form
class Uni_BasicInfoForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = ['university_name', 'state', 'city', 'website']

# University's contact info form
class Uni_ContactInfoForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = ['contact_name', 'contact_title', 'email', 'phone']

# university's academic info form
class Uni_EnrollmentInfoForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = ['UGs', 'number_of_transfers_per_year']

# university's student support services form
class Uni_StudentSupportServicesForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = [
            'housing_availability', 'marriage_or_kids_support', 'vets_support',
            'aids_or_scholarships_for_transfers', 'special_transfer_support'
        ]

# university's transfer and degree pathways form
class Uni_TransferAndDegreePathwaysForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = [
            'contingent_admission', 'online_allowed', 'degree_pathways_for_AAS_student',
            'grad_pathway', 'honor_to_honor_pathway'
        ]

# university's highlights form
class Uni_UniversityHighlightsForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = [
            'institutional_strength_and_highlight', 'graduation_rate', 'retention_rate'
        ]


# College Profile Forms

# College's basic info form
class Col_BasicInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['college_name', 'state', 'city', 'website']

# College's contact info form
class Col_ContactInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['contact_name', 'contact_title', 'email', 'phone']

# College's enrollment form
class Col_EnrollmentInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['total_enrollment', 'full_time_students', 'part_time_students', 'HS_dual_enrollment', 
                  'on_site_HS_available', 'honors_program', 'enrolled_honors_students']

# College's transfer info form
class Col_TransferInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['number_of_transfers_to_universities', 'top1_transfer_partner', 'top2_transfer_partner', 
                  'top3_transfer_partner', 'required_courses_for_transfer', 'head_of_transfer_advising']
        
# College's special 4-year offering form
class Col_Special4YearOfferingForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['statewide_mandated_pathways', 'own_bachelor_degree', 'three_plus_one_program', 'assured_enrollment',
                  'AAS_pathways', 'dual_enrollment_with_university', 'direct_grad_pathways', 'honor_to_honor_pathways']
        
# College's supportive Info form
class Col_SupportiveInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = ['housing_for_international_students', 'sports_teams', 'college_strength']

# class ArticulationAgreementForm(forms.ModelForm):
#     class Meta:
#         model = ArticulationAgreement
#         fields = [
#             'home_institution_name', 'partner_institution_name', 'program_from_institution_one',
#             'program_at_institution_two', 'associate_degree_program', 'institution_offering_associate_degree',
#             'bachelor_degree_program', 'institution_offering_bachelor_degree', 'degree_program',
#             'field_of_study', 'credit_hours', 'university_name', 'gpa_requirement',
#             'final_degree_program', 'final_institution','courses'
#         ]
