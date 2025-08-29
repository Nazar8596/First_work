import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.olx.ua/uk/transport/legkovye-avtomobili/"
HOST = "https://www.olx.ua"
CSV_FILE = "cars.csv"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0"
}

def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status() 
    return response

def get_car_details(url):
    response = get_html(url)
    soup = BeautifulSoup(response.text, "html.parser")

    transmission = None
    mileage = None
    fuel_type = None
    photo = None

    details_list = soup.find_all('li', class_='css-1ux7d92')
    for detail in details_list:
        label = detail.find('span', recursive=False)
        value = detail.find('strong')
        if label and value:
            label_text = label.get_text(strip=True).lower()
            if "трансмісія" in label_text:
                transmission = value.get_text(strip=True)
            elif "пробіг" in label_text:
                mileage = value.get_text(strip=True)
            elif "паливо" in label_text:
                fuel_type = value.get_text(strip=True)

    photo_div = soup.find('div', class_='css-1jjevk8')
    img = photo_div.find('img')
    photo = img.get('src') or img.get('data-src')

    return {
        "transmission": transmission,
        "mileage": mileage,
        "fuel_type": fuel_type,
        "photo": photo
    }

def parse_list_page(html):
    soup = BeautifulSoup(html, "html.parser")
    cars = []
    items = soup.find_all('div', class_="css-1r93q13")
    for item in items:
        title = item.find('h4', class_="css-1g61gc2").get_text(strip=True)
        price = item.find('p', class_="css-uj7mm0").get_text(strip=True)
        link_tag = item.find('a', class_="css-1tqlkj0")
        link = HOST + link_tag.get('href')

        details = get_car_details(link)
        cars.append([
            title, price, link, 
            details["transmission"], details["mileage"], details["fuel_type"], details["photo"]
        ])
    return cars

def save_to_csv(cars, filename):
    with open(filename, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Назва", "Ціна", "Посилання", "Трансмісія", "Пробіг", "Тип палива", "Фото"])
        writer.writerows(cars)

def main():
    pages = int(input("Введіть кількість сторінок для парсингу: "))
    all_cars = []
    for page in range(1, pages + 1):
        print(f"Парсимо сторінку {page}...")
        response = get_html(URL, params={"page": page})
        cars = parse_list_page(response.text)
        all_cars.extend(cars)
    save_to_csv(all_cars, CSV_FILE)
    print(f"Збережено {len(all_cars)} оголошень у {CSV_FILE}")

if name == "main":
    main()