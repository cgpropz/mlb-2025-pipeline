from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&qual=y&type=0&season=2025&month=0&season1=2025&ind=0&team=0%2Cts&pageitems=200"

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

table = soup.find('table')


headers = [th.text.strip() for th in table.find('thead').find_all('th')]

data = []
for tr in table.find('tbody').find_all('tr'):
    row = [td.text.strip() for td in tr.find_all('td')]
    if row:
        data.append(row)

df = pd.DataFrame(data, columns=headers)
print(df)

