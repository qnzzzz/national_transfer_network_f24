import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from ntn_app.models import UniversityProfile, CollegeProfile, Agreement, UniversityCourse, CollegeCourse, AgreementCourse

class Command(BaseCommand):
    help = 'Load courses and agreements from a tab-separated file'

    def handle(self, *args, **options):
        # Step 1: Load the data from the .txt file
        file_path = './files/cleaned_WVU_Transfer_Credit_Database.txt'
        data = pd.read_csv(file_path, sep='\t')
        
        # Step 2: Create the university profile for WVU
        wvu, _ = UniversityProfile.objects.get_or_create(university_name="West Virginia University", is_partner=True)
        
        # Step 3: Process each row in the data
        for _, row in data.iterrows():
            college_name = row['College Name']
            city = row['City']
            state = row['State']
            # effective_term = row['Effective Term']
            college_subject_code = row['College Subject']
            college_digit_code = str(row['College Digit'])
            wvu_subject_code = row['WVU Subject']
            wvu_digit_code = str(row['WVU Digit'])
            credits = float(row['Credits']) if not pd.isna(row['Credits']) else 0.0

            # Step 4: Create or get the college profile
            college, _ = CollegeProfile.objects.get_or_create(
                college_name=college_name,
                city=city,
                state=state,
                is_partner=True
            )
            
            # Step 5: Create or get the agreement
            agreement, _ = Agreement.objects.get_or_create(
                university=wvu,
                college=college,
            )

            # Step 6: Create or get the university course
            university_course, _ = UniversityCourse.objects.get_or_create(
                institution=wvu,
                subject_code=wvu_subject_code,
                digit_code=wvu_digit_code,
                # defaults={'credits': credits}
            )

            # Step 7: Create or get the college course
            college_course, _ = CollegeCourse.objects.get_or_create(
                institution=college,
                subject_code=college_subject_code,
                digit_code=college_digit_code,
                # defaults={'credits': credits}
            )

            # Step 8: Create the AgreementCourse linking the college and university courses
            AgreementCourse.objects.create(
                agreement=agreement,
                college_course=college_course,
                university_course=university_course,
                credits=credits
            )

        self.stdout.write(self.style.SUCCESS("Data successfully loaded into the database"))
