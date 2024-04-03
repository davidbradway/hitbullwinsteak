from bs4 import BeautifulSoup
import requests
import pickle
import datetime

# import the old score from the pickle file
try:
    with open('score.pkl', 'rb') as f:
        (old_dt, old_outcome, old_score) = pickle.load(f)
except:
    old_dt = datetime.datetime(2024, 1, 1)
    old_outcome = True
    old_score = [0, 0]

url = 'https://betsapi.com/t/4574/Durham-Bulls'
page = requests.get(url)

# create a beautiful soup object
soup = BeautifulSoup(page.content, 'html.parser')

# find the table
table = soup.find_all('table', class_='table table-sm')[-1]

# find the first row
row = table.find('tr')

# find the date column
date = row.find('td', class_='dt_n')

# get date from the data-dt attribute and convert from ISO-8601 to a datetime
dt = datetime.datetime.fromisoformat(date.attrs['data-dt'])

# find the second to last column in the row
column = row.find_all('td')[-2]

# get the text of the link in that column and strip whitespace
link = column.find('a').text.strip()

# split into a list of strings by the character '-'
score_str = link.split('-')

# convert the list of strings to a list of integers
score = [int(x) for x in score_str]

# find outcome
column = row.find_all('td')[-3]

# Beautilful soup select contents of the td tag
outcome = column.contents[0]
iswin = outcome == 'W'

# if new date posted,
if old_dt != dt:
    # save a list to a pickle file
    with open('score.pkl', 'wb') as f:
        my_tuple = (dt, iswin, score)
        pickle.dump(my_tuple, f)

print('Score:', score, ', is win:', iswin, ', Date:', dt)
