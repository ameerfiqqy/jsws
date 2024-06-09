import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.jobstreet.com.my/jobs/in-Kuching-Sarawak'

# Send a GET request to the URL
response = requests.get(url)

# Parse HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract job titles
results_jawatan = soup.find_all('a', class_='y735df0 y735dff y735df0 y735dff _12jtenne _12jtenng')

# Extract Salary
results_gaji = soup.find_all('span', class_='y735df0 _153p76c2 _1iz8dgs4y _1iz8dgs0 _1iz8dgsr _153p76c4')

# Extract company names
results_opis = soup.find_all('a', class_='y735df0 y735dff y735df0 y735dff _5nhsu10 _5nhsu11')

# Extract job locations
location_elements = soup.find_all('a', {'data-automation': 'jobLocation'})
results_banda =  [element.text.strip() for element in location_elements]

combined_banda = []

for i in range(0, len(results_banda), 2):
    combined_banda.append(results_banda[i] + ', ' + results_banda[i+1])


# Extract lists of benefits
results_ben = soup.find_all('ul', class_='y735df0 y735df3 _1akoxc50 _1akoxc54')


# # Open a CSV file for writing
# with open('jobs.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
    
#     # Write the header
#     writer.writerow(['Job Title', 'Salary Range','Company Name', 'Location', 'Benefits'])
    
#     # Iterate through the extracted data and write to the CSV file

#     for i in range(max(len(results_jawatan), len(results_gaji), len(results_opis), len(results_ben))):
#         job_title = results_jawatan[i].text.strip() if i < len(results_jawatan) else ''
#         saalry_range = results_gaji[i].text.strip() if i < len(results_gaji) else ''
#         company_name = results_opis[i].text.strip() if i < len(results_opis) else ''
#         location = combined_banda[i] if i < len(results_banda) else ''
#         benefits = results_ben[i].text.strip() if i < len(results_ben) else ''

#         # Write the row to the CSV file
#         writer.writerow([job_title, saalry_range, company_name, location, benefits])

# print('Data has been written to jobs.csv')

# Combine 'Kuching' and 'Sarawak' into one location
combined_banda = []
for i in range(0, len(results_banda), 2):
    combined_banda.append(results_banda[i] + ', ' + results_banda[i + 1])

# Collect data and write to CSV
with open('jobs.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Salary Range', 'Company Name', 'Location', 'Benefits'])

    # Iterate through the extracted data and write to the CSV file
    for i in range(max(len(results_jawatan), len(results_gaji), len(results_opis), len(combined_banda))):
        job_title = results_jawatan[i].text.strip() if i < len(results_jawatan) else ''
        salary_range = results_gaji[i].text.strip() if i < len(results_gaji) else ''
        company_name = results_opis[i].text.strip() if i < len(results_opis) else ''
        location = combined_banda[i] if i < len(combined_banda) else ''
        
        # Extract job titles
        results_jawatan = soup.find_all('a', class_='y735df0 y735dff y735df0 y735dff _12jtenne _12jtenng')

        # Extract salary ranges
        results_gaji = soup.find_all('span', class_='y735df0 _153p76c2 _1iz8dgs4y _1iz8dgs0 _1iz8dgsr _153p76c4')

        # Extract company names
        results_opis = soup.find_all('a', class_='y735df0 y735dff y735df0 y735dff _5nhsu10 _5nhsu11')

        # Extract job locations
        location_elements = soup.find_all('a', {'data-automation': 'jobLocation'})
        results_banda = [element.text.strip() for element in location_elements]
        
        # Extract lists of benefits
        results_ben = soup.find_all('ul', class_='y735df0 y735df3 _1akoxc50 _1akoxc54')
        benefits = results_ben[i].text.strip() if i < len(results_ben) else ''

        # Write the row to the CSV file
        writer.writerow([job_title, salary_range, company_name, location, benefits])

print('Data has been written to jobs.csv')