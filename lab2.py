import json
import csv
from playwright.sync_api import sync_playwright

URL = "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"


def main():
    print("Запуск браузера та відкриття сторінки...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        print("Очікування відпрацювання JavaScript (завантаження товарів)...")
        page.wait_for_selector(".thumbnail")
        print("JavaScript успішно відпрацював, картки товарів з'явилися.")
        products_data = []
        cards = page.locator(".thumbnail").all()

        for card in cards:
            title = card.locator(".title").inner_text()
            price = card.locator(".price").inner_text()
            description = card.locator(".description").inner_text()
            reviews = card.locator(".ratings > p.pull-right").inner_text()
            products_data.append({
                "title": title,
                "price": price,
                "description": description,
                "reviews": reviews
            })
        print(f"Успішно зібрано даних про товари: {len(products_data)}")
        browser.close()
    print("\nЗбереження даних у структуровані формати...")

    with open("laptops_data.json", "w", encoding="utf-8") as json_file:
        json.dump(products_data, json_file, ensure_ascii=False, indent=4)

    with open("laptops_data.csv", "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "price", "description", "reviews"])
        writer.writeheader()
        writer.writerows(products_data)

    print("Готово! Дані збережено у файли 'laptops_data.json' та 'laptops_data.csv'.")


if __name__ == "__main__":
    main()