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

        print("File open successfully")
        
        # Step 2: Create the university profile for WVU
        wvu, _ = UniversityProfile.objects.get_or_create(university_name="West Virginia University", is_partner=True)
        print("West Virginia University profile created successfully")

        # Step 3: Process each row in the data
        for _, row in data.iterrows():
            college_name = row['College Name'].strip() if pd.notna(row['College Name']) else None
            city = row['City'].strip() if pd.notna(row['City']) else None
            state = row['State'].strip() if pd.notna(row['State']) else None
            college_subject_code = row['College Subject'].strip() if pd.notna(row['College Subject']) else None
            college_digit_code = str(row['College Digit']).strip() if pd.notna(row['College Digit']) else None
            wvu_subject_code = row['WVU Subject'].strip() if pd.notna(row['WVU Subject']) else None
            wvu_digit_code = str(row['WVU Digit']).strip() if pd.notna(row['WVU Digit']) else None
            credits = float(row['Credits']) if pd.notna(row['Credits']) else None


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
            )

            # Step 7: Create or get the college course
            college_course, _ = CollegeCourse.objects.get_or_create(
                institution=college,
                subject_code=college_subject_code,
                digit_code=college_digit_code,
            )

            # Step 8: Create the AgreementCourse linking the college and university courses
            AgreementCourse.objects.create(
                agreement=agreement,
                college_course=college_course,
                university_course=university_course,
                credits=credits
            )

        self.stdout.write(self.style.SUCCESS("WVU Data successfully loaded into the database"))
