import requests
from bs4 import BeautifulSoup

# Define the URL of the website you want to scrape
url = "https://www.datascienceglossary.org/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the elements containing glossary terms (you may need to inspect the page's HTML structure)
    glossary_elements = soup.find_all("dt") #the headers are contained inside the dt tags , dt tags are used to define a term

    # Create a set to store unique glossary terms
    glossary_set = set()

    # Extract and store glossary terms in the set
    for element in glossary_elements:
        term = element.find("dfn").get_text().strip() #extract text within dfn tags, the headers are contained inside the dfn tags
        glossary_set.add(term)

    # Convert the set to a list
    glossary_list = list(glossary_set)

else:
    print("Failed to retrieve the web page. Status code:", response.status_code)

print(glossary_list)
