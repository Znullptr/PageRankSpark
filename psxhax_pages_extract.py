import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

psxhax_pages_info = {
    'page_title': [],
    'page_url': [],
    'links': [],
}


def get_articles(response):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')
    articles = soup.findAll('a', class_='porta-article-header')
    articles_urls = [link['href'] for link in articles]

    for url in articles_urls:
        article_url = 'https://www.psxhax.com' + url
        while True:
            try:
                # Send a GET request to the URL
                response = requests.get(article_url)
                # Check if the request was successful
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'lxml')
                    # Find all <a> tags with href starting with "https://www.psxhax.com/threads/"
                    wiki_box = soup.find('div', class_='bbWrapper')
                    threads = wiki_box.find_all("a", href=lambda href: href and href.startswith(
                        "https://www.psxhax.com/threads/"))
                    # Extract the links, page link and page title from the page
                    threads_links = set([link['href'] for link in threads])
                    article_title = soup.find('h1', class_="p-title-value").text.strip()
                    article_links = ','.join(str(link) for link in threads_links)
                    psxhax_pages_info['page_title'].append(article_title)
                    psxhax_pages_info['page_url'].append(article_url)
                    psxhax_pages_info['links'].append(article_links)
                    break
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                print("Connection error or timeout occurred. Retrying in 30 seconds...")
                time.sleep(30)
                continue


def main():
    # Iterate over the URLs and scrape psxhax page information
    url = 'https://www.psxhax.com/articles/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    nb_page = soup.find('ul', class_="pageNav-main").find_all('li')[-1].text.strip()
    i = 1
    while True:
        try:
            if i == int(nb_page) + 1:
                break
            url = f'https://www.psxhax.com/articles/page-{i}'
            response = requests.get(url)
            if response.status_code == 200:
                # Get articles of the page
                print(f'processing psxhax page {i}/{nb_page} ...')  # numbers of pages in psxhax in the meantime is 414
                get_articles(response)
                i += 1
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            print("Connection error or timeout occurred. Retrying in 30 seconds...")
            time.sleep(30)
            continue

    # Create a DataFrame from the psxhax pages information
    pages_df = pd.DataFrame(psxhax_pages_info)
    # Save the dataframe to a CSV file with index column and named 'page_id'
    pages_df.to_csv('psxhax_pages_info.csv', index_label='page_id')
    print('==========================================================')
    print('\nwiki pages information saved to psxhax_pages_info.csv successfully.')


if __name__ == '__main__':
    main()
