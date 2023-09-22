import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Define the city and niche to scrape
city = "San Francisco"
niche = "Home Decor"

url = "https://www.google.com/search?q={}+{}".format(city, niche)
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

businesses = []
for business in soup.findAll("div", class_="cX8d1e"):
    name = business.find("span", class_="BNeawe").text
    address = business.find("span", class_="BNeawe tA6K1").text
    phone_number = business.find("span", class_="phoneNumber").text
    email_address = business.find("span", class_="email").text

    social_media_links = []
    for link in business.findAll("a", class_="BNeawe"):
        href = link.get("href")
        if "facebook" in href:
            social_media_links.append({"platform": "Facebook", "url": href})
        elif "instagram" in href:
            social_media_links.append({"platform": "Instagram", "url": href})
        elif "tiktok" in href:
            social_media_links.append({"platform": "TikTok", "url": href})


    businesses.append({
        "name": name,
        "address": address,
        "phone_number": phone_number,
        "email_address": email_address,
        "social_media_links": social_media_links
    })

# Scrape additional data, such as reviews, website, operating since, and employee number
def scrape_additional_data(business):
    website = None
    for link in business["social_media_links"]:
        if "website" in link["platform"]:
            website = link["url"]
            break

    
    reviews = []
    if website:
        
        pass

    
    operating_since = None
    

    
    employee_number = None
    

    
    business["website"] = website
    business["reviews"] = reviews
    business["operating_since"] = operating_since
    business["employee_number"] = employee_number

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_additional_data, businesses)

import csv
with open("businesses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "address", "phone_number", "email_address", "social_media_links", "website", "reviews", "operating_since", "employee_number"])
    for business in businesses:
        writer.writerow([business["name"], business["address"], business["phone_number"], business["email_address"], ",".join([link["url"] for link in business["social_media_links"]]), business["website"], ",".join(business["reviews"]), business["operating_since"], business["employee_number"]])
