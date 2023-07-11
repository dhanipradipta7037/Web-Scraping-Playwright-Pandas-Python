from playwright.sync_api import sync_playwright
import pandas as pd
import time

def main():
    with sync_playwright() as p:
        data_books = []
        ori_url = 'https://books.toscrape.com'
        base_url = 'https://books.toscrape.com/catalogue'
        for x in range(1, 5):
            url = f'https://books.toscrape.com/catalogue/page-{x}.html'
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            time.sleep(5)
            books = page.locator('//article[@class="product_pod"]').all()
            for book in books:
                name = book.locator('//h3/a').inner_text()
                book_url = base_url + book.locator('//h3/a').get_attribute('href')
                price = book.locator('//p[@class="price_color"]').inner_text()
                img = ori_url + book.locator('//img[@class="thumbnail"]').get_attribute('src').replace('..', '')
                list_book = {'Nama buku':name,
                             'Harga buku':price,
                             'Gambar buku':img,
                             'Link buku':book_url,
                             }
                data_books.append(list_book)

        df = pd.DataFrame(data_books)
        print(df)
        df.to_csv('bookscrape.csv', index=False, encoding='utf-8')

        browser.close()

if __name__ == '__main__':
    main()
