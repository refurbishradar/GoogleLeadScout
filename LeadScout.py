import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Get the niche and location from the user
niche = input("Enter a niche: ")
location = input("Enter a location: ")

# Generate a list of keywords related to the niche
keywords = [
    niche,
    niche + " " + location,
    niche + " services near me",
    niche + " companies near me",
    niche + " businesses near me",
    niche + " contractors near me",
    niche + " professionals near me",
    niche + " experts near me",
    niche + " reviews",
    niche + " ratings",
    niche + " directory",
    niche + " listings"
]

# Scrape data for each keyword in parallel
def scrape_data(keyword):
    # Get the list of businesses from Google
    url = "https://www.google.com/search?q={}+{}".format(keyword, location)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the business name, address, phone number, email address, and social media links
    businesses = []
    for business in soup.findAll("div", class_="cX8d1e"):
        name = business.find("span", class_="BNeawe").text
        address = business.find("span", class_="BNeawe tA6K1").text
        phone_number = business.find("span", class_="phoneNumber").text
        email_address = business.find("span", class_="email").text

        # Extract social media links
        social_media_links = []
        for link in business.findAll("a", class_="BNeawe"):
            href = link.get("href")
            if "facebook" in href:
                social_media_links.append({"platform": "Facebook", "url": href})
            elif "instagram" in href:
                social_media_links.append({"platform": "Instagram", "url": href})
            elif "tiktok" in href:
                social_media_links.append({"platform": "TikTok", "url": href})

        # Extract the business's website
        website = business.find("a", class_="BNeawe tA6K1")
        website = website.get("href")

        # Scrape reviews from the business's website
        # (This code will vary depending on the website)
        reviews = []
        # ...

        # Add the business to the list of businesses
        businesses.append({
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email_address": email_address,
            "social_media_links": social_media_links,
            "website": website,
            "reviews": reviews
        })

    return businesses

# Scrape data for each keyword in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_data, keywords)

# Export the data to CSV
import csv
with open("businesses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "address", "phone_number", "email_address", "social_media_links", "website", "reviews"])
    for businesses in results:
        for business in businesses:
            writer.writerow([business["name"], business["address"], business["phone_number"], business["email_address"], ",".join([link["url"] for link in business["social_media_links"]]), business["website"], ",".join(business["reviews"])])
