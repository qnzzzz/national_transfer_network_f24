import pandas as pd

# Load the Excel file
file_path = '../files/WVU Transfer Credit Database.xlsx'
excel_data = pd.read_excel(file_path)

# Step 1: Filter out all rows in "College Name" column with "university"
filtered_data = excel_data[~excel_data['College Name'].str.contains("university", case=False, na=False)].copy()

# Step 2: Split "College Location" column by comma, create "City" and "State" columns
location_split = filtered_data['College Location'].str.split(',', expand=True)
filtered_data['City'] = location_split[0].str.strip()
filtered_data['State'] = location_split[1].str.strip() if location_split.shape[1] > 1 else None

# Drop the original "College Location" column
filtered_data = filtered_data.drop(columns=['College Location'])

# Save the cleaned data to a new .txt file with tab separation for verification
output_path = '../files/cleaned_WVU_Transfer_Credit_Database.txt'
filtered_data.to_csv(output_path, sep='\t', index=False)

print(f"Cleaned data saved to {output_path}")
