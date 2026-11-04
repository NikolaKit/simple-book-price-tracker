import csv
import requests
from bs4 import BeautifulSoup

def get_max_budget():
    while True:
        try:
            budget = float(input("Enter your maximum budget (GBP): "))
            if budget > 0:
                return budget
            print("Please enter a price greater than 0.")
        except ValueError:
            print("Invalid input! Please enter a valid number (e.g., 20 or 15.5).")

def scrape_books():
    url = "http://books.toscrape.com/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve data from website: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    max_budget = get_max_budget()

    books = soup.find_all("article", class_="product_pod")
    books_data = []

    print(f"\n--- Books Found Within Budget (GBP {max_budget}) ---")

    for book in books:
        try:
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text
            
            # Ciscenje cene i konverzija
            clean_price = price_text.replace("£", "").replace("Â", "").strip()
            price = float(clean_price)

            if price <= max_budget:
                print(f"{title} - GBP {price}")
                books_data.append([title, price])
        except (AttributeError, KeyError, ValueError):
            continue

    if books_data:
        csv_filename = "books.csv"
        with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as file:
            file.write("sep=;\n")
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Book Title", "Price (GBP)"])
            writer.writerows(books_data)
        print(f"\nSuccessfully saved {len(books_data)} books to '{csv_filename}'.")
    else:
        print("\nNo books found within your budget.")

if __name__ == "__main__":
    scrape_books()
