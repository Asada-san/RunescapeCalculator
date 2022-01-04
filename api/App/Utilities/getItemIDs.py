import requests
from bs4 import BeautifulSoup
import json
import time
import random


def get_tradeable_itemIDs():
    item_list = {}
    number_of_categories = 42
    max_amount_of_pages = 20

    # For every category on the Grand Exchange catalogue page starting at 0
    for i in range(0, number_of_categories):
        end_loop = False
        time.sleep(10)

        # For every page in a given category (make sure the pages don't go over 20 offline) starting at 1
        for j in range(1, max_amount_of_pages + 1):
            # The url of category i and page j
            url = f"http://services.runescape.com/m=itemdb_rs/catalogue?cat={i}&page={j}"
            # Get the html code of the page

            # custom header cause Jagex... (noindex/nofollow)
            UAS = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
            "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            )

            ua = UAS[random.randrange(len(UAS))]

            r = requests.get(url, headers={'user-agent': ua})

            # Clean that shit up
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find all the table rows
            rows = soup.find('table').find('tbody').find_all('tr')

            for row in rows:
                # The item name and id are both in a img element within a table row
                img_element = row.find('td').find('a').find('img')
                item = img_element['title']
                # The id is buried a bit deeper within the source link of the image
                link = img_element['src']
                id = link.split('=')[-1]

                # Verify if all items in the category are checked
                if id in item_list:
                    end_loop = True
                    break
                else:
                    item_list.update({id: item})

            print(i, j)

            if end_loop:
                break
            else:
                time.sleep(10)

    # Save the list
    with open('../itemIDs.json', 'w') as file:
        json.dump(item_list, file)

    return None


if __name__ == "__main__":
    get_tradeable_itemIDs()
