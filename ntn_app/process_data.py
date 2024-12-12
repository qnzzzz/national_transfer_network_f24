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

# Step 3: Remove rows with invalid "College Digit" or "WVU Digit"
# Allow only letters and digits (no special characters)
filtered_data = filtered_data[
    filtered_data['College Digit'].str.match(r'^[A-Za-z0-9]+$', na=False) &
    filtered_data['WVU Digit'].str.match(r'^[A-Za-z0-9]+$', na=False)
]

# Step 4: Fill empty cells with 'NA' as a placeholder
filtered_data = filtered_data.fillna('NA')

# Save the cleaned data to a new .txt file with tab separation for verification
output_path = '../files/cleaned_WVU_Transfer_Credit_Database.txt'
filtered_data.to_csv(output_path, sep='\t', index=False)

print(f"Cleaned data saved to {output_path}")


# def find_longest_digit_code(file_path):
#     longest_length = 0
#     longest_code = ""

#     with open(file_path, 'r') as file:
#         # Skip the header line
#         header = file.readline().strip().split('\t')
#         # Ensure "College Digit" is in the header
#         if 'College Digit' not in header:
#             raise ValueError("Column 'College Digit' not found in the file header")
#         digit_code_index = header.index('College Digit')

#         for line in file:
#             columns = line.strip().split('\t')  # Split line into columns
#             digit_code = columns[digit_code_index].strip()  # Access the 'College Digit' column
#             if len(digit_code) > longest_length:
#                 longest_length = len(digit_code)
#                 longest_code = digit_code

#     print(f"Longest digit code: {longest_code}")
#     print(f"Length: {longest_length}")

# # Replace with the actual path to your cleaned .txt file
# find_longest_digit_code('../files/cleaned_WVU_Transfer_Credit_Database.txt')
