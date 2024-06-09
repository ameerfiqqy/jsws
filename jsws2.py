import requests
from bs4 import BeautifulSoup
import csv
import datetime
from collections import OrderedDict


def get_url(position , location):
    template = 'https://www.jobstreet.com.my/{}jobs/in{}'
    url = template.format(position,location)
    return url

url = 'https://www.jobstreet.com.my'

def get_record(card):
    title_tag = card.h3.div
    job_title = title_tag.text

    url_tag = card.div.a
    job_url = 'https://www.jobstreet.com.my' + url_tag.get('href')

    try:
        companies_tag = card.span.a
        companies = companies_tag.text
    except AttributeError:
        companies = 'Private Advertiser'

    locations_tag = card.find('span' , 'y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w21 _4rkdcp4 _94v4w7')
    locations = locations_tag.text.strip()

    # polah if statement in case xda gaji display
    try:
        salaries_tag = card.find('span', 'y735df0 _153p76c2 _1iz8dgs4y _1iz8dgs0 _1iz8dgsr _153p76c4')
        salaries = salaries_tag.text.strip()
    except AttributeError:
        salaries = ''

    job_categories_tag = card.find('div' , 'y735df0 _1iz8dgsgi _1iz8dgs5a _1iz8dgsg2 _1akoxc52j')
    job_categories = job_categories_tag.text.strip().replace('subClassification: ','').replace('classification: ', ' , ')

    # polah if statement in case xda tulis benefits
    try:
        job_benefits_tag = card.find('ul' , 'y735df0 y735df3 _1akoxc50 _1akoxc54')
        job_benefits = job_benefits_tag.text.strip()
    except AttributeError:
        job_benefits = ''

    # job_summaries_tag = card.find('div', 'y735df0 _1pehz540', 'p')
    # job_summaries = job_summaries_tag

    job_posted_tag = card.find('span' , 'y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w22 _4rkdcp4 _94v4w7')
    job_posted = job_posted_tag.text.strip()

    today = datetime.datetime.now().strftime("%d-%m-%Y")
    
    # record = (job_title , companies , locations , salaries , job_categories , job_benefits , job_summaries , today, job_posted , job_url)
    record = (job_title , companies , locations , salaries , job_categories , job_benefits , today, job_posted , job_url)

    return record

def main(position,location):

    records = []
    url = get_url(position,location)

    # Extract the job data
    while True:

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all('article', 'y735df0 y735df1 _1iz8dgs7i _1iz8dgs6e _1iz8dgs9q _1iz8dgs8m _1iz8dgsh _1iz8dgs66 _1iz8dgs5e _12jtennb _12jtenn9 _12jtenna _94v4w18 _94v4w1b _1iz8dgs32 _1iz8dgs35')

        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = 'https://www.jobstreet.com.my' + soup.find('a',{'aria-label' : 'Next'}).get('href')
        except AttributeError:
            break

    # Save the data
    with open('jobslisting.csv','w', newline='',encoding='utf-8') as f:
        write = csv.writer(f)
        # write.writerow(['Job Title','Company','Location','Salary','Category','Benefits','Summary', 'Extract Date','Posted Date','Job URL'])
        write.writerow(['Job Title','Company','Location','Salary','Category','Benefits','Extract Date','Posted Date','Job URL'])
        write.writerows(records)

# Main Program add "-" at the end of position and begining of location
main('engineer-','-sarawak')

