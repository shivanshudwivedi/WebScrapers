
# eBay Electronics Scraper

This project is a web scraper built to extract product information from eBay's electronics category. The application fetches the product details such as title, price, and image URL from the search results page and writes them into a CSV file named `e_bay_electronics.csv`.

## Tech Stack

1. **Python**: The primary programming language used for writing the scraper.
2. **BeautifulSoup**: A Python library used for parsing HTML and XML documents. It creates parse trees from page source codes that can be used to extract data easily.
3. **Requests**: A simple HTTP library for Python, used for making GET requests to fetch the HTML content of web pages.
4. **CSV**: Python's built-in CSV library is used to write the extracted data into a CSV file.

## Methodology

### 1. Fetching HTML Content

The `get_page(url)` function takes a URL as input and makes a GET request to fetch the HTML content of the page. If the response is successful, it parses the HTML using BeautifulSoup with the `lxml` parser and returns the soup object.

```python
def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print("Server Responded: ", response.status_code)
    else:
        soup = BeautifulSoup(response.text, "lxml")
    return soup
```

### 2. Extracting Product Details

The `get_detail_data(soup)` function takes a BeautifulSoup object as input and extracts the product title, price, and image URL using specific HTML tags and class names. It returns these details as a dictionary.

```python
def get_detail_data(soup):
    try:
        title = soup.find("h1", class_="x-item-title__mainTitle").find("span").get_text().strip()
    except:
        title = ""

    try:
        price = soup.find("div", class_="x-price-primary").find("span").get_text().strip()
    except:
        price = ""

    try:
        image_url = soup.find("div", class_="ux-image-carousel-item image-treatment active image").find("img").get("src").strip()
    except:
        image_url = ""

    data = {
        'Title': title,
        'Price': price,
        'Image URL': image_url
    }
    return data
```

### 3. Extracting Product Links

The `get_index_data(soup)` function takes a BeautifulSoup object of the search results page and extracts the URLs of individual product pages. It returns a list of these URLs.

```python
def get_index_data(soup):
    try:
        links = soup.find_all("a", class_="s-item__link")
    except:
        links = []
    urls = [item.get("href") for item in links]
    return urls
```

### 4. Writing Data to CSV

The `write_to_csv(data)` function appends the extracted product details to the `e_bay_electronics.csv` file.

```python
def write_to_csv(data):
    with open('e_bay_electronics.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Image URL'])
        writer.writerow(data)
```

### 5. Main Function

The `main()` function orchestrates the entire scraping process. It initializes the CSV file with headers, fetches the search results page, extracts product URLs, and then iterates through each URL to fetch and write product details to the CSV file.

```python
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
```

## Usage

1. Ensure you have Python installed on your machine.
2. Install the required libraries using the following commands:
   ```bash
   pip install requests
   pip install beautifulsoup4
   ```
3. Run the script:
   ```bash
   python ebay_scraper.py
   ```
4. The scraped data will be saved in a file named `e_bay_electronics.csv`.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
