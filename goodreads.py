from bs4 import BeautifulSoup
import requests
from time import sleep
from os import system, name

# introduction
print('This program sorts standalone books or first books in a series over <specify_amount> ratings of any given')
input('list on goodreads.com by average rating across all pages and stores the results in a txt file.')

# taking user input
file = input('What shall be the name of the file?: ') + '.txt'
base_url = input('Return the link of the list you want to sort: ')
url_template = base_url + '?page={}'
pages = int(input('How many pages does the list have?: '))
min_ratings = int(input('Specify the minimum amount of ratings a book should have: '))

sleep(1)

# making place for the book details
print('Making place for book details...')
book_details = []

sleep(1)

# defining headers to use a user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# searching for book details
print(f'Extracting book details and sorting out books not first in a series and under {min_ratings} ratings...')

sleep(1)

for page in range(1, pages + 1):
    current_url = url_template.format(page)
    print(f'Processing page {page}/{pages}...', end='\r')
    # setting up the web scraper with headers
    html_text = requests.get(current_url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    books = soup.find_all('tr')
    # extracting book details
    for book in books:
        title = book.find('span', itemprop="name").text.strip()
        author = book.find('span', itemprop="author").find('span', itemprop="name").text.strip()
        rating = book.find('span', class_="minirating").text.split(' ')
        num_ratings = int(rating[-2].replace(',', ''))
        avg_rating = None
        # searching for the avg rating in rating
        for element in rating:
            try:
                avg_rating = float(element)
                break
            except ValueError:
                continue
        # checking if book is first in series
        first_in_series = not any(char.isdigit() and char != '1' for char in title) and not '11' in title
        # sorting out books under <min_ratings>
        if num_ratings > min_ratings and first_in_series:
            book_details.append({'title': title, 'author': author, 'avg_rating': avg_rating})

sleep(1)

# sorting the books by average rating
print('Sorting books by average rating...')
book_details.sort(key=lambda x: x['avg_rating'], reverse=True)

sleep(1)

# writing results to txt file
print('Writing results to the file...')
with open(file, 'w', encoding='utf-8') as f:
    for book in book_details:
        f.write(f"\n{book['title']} by {book['author']} / {book['avg_rating']}\n")

sleep(1)

print('Done.')