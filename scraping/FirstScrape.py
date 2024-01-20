# Import necessary libraries
from requests import get
import pandas as pd
from tqdm import tqdm
from json import loads

try:
    # Read URLs from file and format them to Trendyol URLs
    print("Reading URLs from file...")
    with open("electronics.txt", "r") as file:
        urls = [f"https://www.trendyol.com/{line.strip()}" for line in file]

    # Set a limit on the number of products to fetch per URL
    limit = 50
    products = []

    # Iterate through each URL and fetch product information
    for url_idx, url in enumerate(tqdm(urls)):
        # Initialize variables for each URL
        page_count = 1
        products = []

        # Extract keyword from URL to use in API request
        keyword = url.split("com/")[-1].split("?")[0]
        api_url = f'https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/{keyword}?pi={page_count}'

        # Continue fetching products until the limit is reached or maximum page count is reached
        while not (len(products) >= limit and limit != 0 or page_count > 208):
            data = loads(get(api_url).text)
            products.extend(data["result"]["products"])

        products = products[:limit]

        # Extract product information into separate lists
        names, links, prices = [], [], []
        for item in products:
            names.append(item["name"])
            links.append("https://trendyol.com" + item["url"])
            prices.append(item["price"]["sellingPrice"])

        # Combine lists into a list of lists
        products.extend(list(zip(names, links, prices)))    

    # Create a DataFrame from the product list and save it to a TSV file
    dataframe = pd.DataFrame(products, columns=(["Name", "Link", "Price"]))
    dataframe.to_csv("products.tsv", sep="\t", index=False)

except Exception as e:
    # Print any exception that occurs during the process
    print(str(e))
