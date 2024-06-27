import requests
import time
from bs4 import BeautifulSoup
import string
import os
from unidecode import unidecode


def main():
    # URL of the webpage to scrape
    for letter in string.ascii_uppercase:
        # Avoid overloading server with requests
        time.sleep(3)
        url = f"https://nominis.cef.fr/contenus/prenom/biblique/{letter}.html"

        # Send a GET request to the webpage
        response = requests.get(url)
        print(response.status_code)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all h5 elements with the class 'mb1'
            links = soup.find_all("a", class_="list-group-item list-group-item-action")

            # Extract the text from the 'h5' elements within these 'a' elements
            name_list = []
            for link in links:
                h5_tag = link.find("h5", class_="mb-1")
                if h5_tag:
                    name_list.append(unidecode(h5_tag.get_text(strip=True)).upper())

            # Print the extracted names
            for name in name_list:
                print(name)
                # save the names in a file
                with open(os.path.join("data", "names.txt"), "a") as file:
                    file.write(name + "\n")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)


if __name__ == "__main__":
    main()
