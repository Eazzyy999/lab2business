import json
import csv
from playwright.sync_api import sync_playwright

URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)

        products_data = []
        page_num = 1

        while True:
            print(f"\nОбробка сторінки {page_num}")

            page.wait_for_selector(".thumbnail")

            cards = page.locator(".thumbnail").all()
            for card in cards:
                title = card.locator(".title").inner_text()
                price = card.locator(".price").inner_text()
                description = card.locator(".description").inner_text()

                products_data.append({
                    "title": title,
                    "price": price,
                    "description": description
                })

            print(f"Зібрано товарів на сторінці: {len(cards)}. Загалом: {len(products_data)}")

            next_button = page.locator("a.page-link:has-text('›')")

            if next_button.is_visible():
                print("Натискаємо кнопку 'Далі'...")
                next_button.click()
                page.wait_for_timeout(2000)
                page_num += 1
            else:
                print("Кнопки 'Далі' більше немає. Досягнуто останньої сторінки.")
                break
        browser.close()
    print("\nЗбереження даних у файли...")
    with open("laptops_data.json", "w", encoding="utf-8") as json_file:
        json.dump(products_data, json_file, ensure_ascii=False, indent=4)

    with open("laptops_data.csv", "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "price", "description"])
        writer.writeheader()
        writer.writerows(products_data)
    print("Готово!")

if __name__ == "__main__":
    main()