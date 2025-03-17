#########################################################
# Engineer: Josh Rendon
# Started: 03/17/2025
# Purpose: Python webscraper that scrapes slashdot.org and creates a summary
# page of articles of interest (than can then be filtered afterwards for
# viewing).
#    
#########################################################
import requests
from bs4 import BeautifulSoup
import csv

debug_mode = 0

from dataclasses import dataclass
@dataclass
class JobListing:
    post_date : str
    title : str
    company : str
    location : str
    apply_url : str
    job_description : str

def extract_job_listing(job_collection):
    i = 0
    for job_card in job_collection:
        #    if i > 1:
        #       break
        job_listing = {}

        title_element = job_card.find("h2", class_="title")
        company_element = job_card.find("h3", class_="company")
        location_element = job_card.find("p", class_="location")
        link_url = job_card.find_all("a")[1]["href"]

        # Once the link_url is found, GET page the request
        # and extract the text
        apply_page = requests.get(link_url)
        soup_job_desc = BeautifulSoup(apply_page.content, "html.parser")
        job_desc_page = soup_job_desc.find(id="ResultsContainer")
        post_date = job_desc_page.find(id="date").text.strip()
        job_description  = job_desc_page.p.text.strip()


        # Remove "Posted:" DATE to get just numerical DATE
        post_date = post_date.replace("Posted:", "").strip()

        jl = JobListing(post_date,
        title_element.text.strip(),
        company_element.text.strip(),
        location_element.text.strip(),
        link_url,
        job_description)


        job_listings.append(jl)

        if debug_mode:
           print(jl.title)
           print(jl.company)
           print(jl.location)
           print(jl.apply_url)
           print(jl.job_description)
           print(jl.post_date)
           print()


URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="ResultsContainer")

# Scrape all job-listings
job_cards = results.find_all("div", class_="card-content")

# Filter out just the python jobs to speed up the scraping
# (although all the job_cards can be stored in a local array
# or hash containing either an collection of (objects, structs or tupples with
# fields (title, company, location). Such that jobs collection can be searched
# against title field for desired job type.

# For now filter out just python jobs

#python_jobs = results.find_all(
#        "h2", string=lambda text: "python" in text.lower()
#        )

#python_job_cards = [
#        #h2_element.parent.parent.parent for h2_element in python_jobs
#        h2_element.parent.parent.parent for h2_element in job_cards
#        ]
python_job_cards = job_cards

#class job_listing():
job_listings = []

# Print number of python_jobs for debug purposes
#print(len(python_jobs))
#print(len(python_job_cards))

extract_job_listing(python_job_cards)

# Now that the job_listings have been scrapped to a dictionary, write the
# contents of that dictionary to a csv file for storage.
with open('job_list.csv', 'w', newline='') as csvfile:
    fieldnames = ['post_date', 'title', 'company', 'location', 'apply_url',
    'job_description']

    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Loop over all the job_listings located and print out the job_listing
    # details to the csv file
    for jl in job_listings:
        writer.writerow({'post_date': jl.post_date, 
                         'title': jl.title,
                         'company': jl.company,
                         'location': jl.location,
                         'apply_url': jl.apply_url,
                         'job_description': jl.job_description
                         }) 

