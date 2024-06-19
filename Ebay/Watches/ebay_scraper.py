import time
from bs4 import BeautifulSoup
import requests
import csv

def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print("Server Responded: ", response.status_code)
    else:
        soup = BeautifulSoup(response.text, "lxml")

    return soup
    
def get_detail_data(soup):

    #title
    #price
    #imageURL

    try:
        title = soup.find("h1", class_="x-item-title__mainTitle").find("span").get_text().strip()
        print(title)

    except:
        title = ""

    try:
        price = soup.find("div", class_="x-price-primary").find("span").get_text().strip()
        print(price)

    except:
        price = ""

    try:
        image_url = soup.find("div", class_="ux-image-carousel-item image-treatment active image").find("img").get("src").strip()
        print(image_url)

    except:
        image_url = ""

    data = {
        'Title': title,
        'Price': price,
        'Image URL': image_url
    }

    return data

def get_index_data(soup):
    try:
        links = soup.find_all("a", class_="s-item__link")

    except:
        links = []
    
    urls = [item.get("href") for item in links]

    return urls

def write_to_csv(data):
    with open('e_bay_electronics.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Image URL'])
        writer.writerow(data)

def main():

    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=watch+men&_sacat=260324&_pgn=1"
 
    products = get_index_data(get_page(url))
   
    for i in range(2, len(products)):
        print(products[i])
        data = get_detail_data(get_page(products[i]))
        print(data)
        write_to_csv(data)

if __name__ == "__main__":
    with open('e_bay_electronics.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Image URL'])
        writer.writeheader()
    main()
