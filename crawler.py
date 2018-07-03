from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


import time
import pandas as pd
import numpy as np
import re

start_url = 'https://steamcommunity.com/app/255710/reviews'
options = Options()
# options.add_argument('--headless')

print('initializing driver...')

driver = webdriver.Firefox(firefox_options = options)
driver.get(start_url)
driver.find_element_by_class_name('filterselect_arrow').click()
driver.find_element_by_id('filterselect_option_0').click()
comments = []
dates = []
titles = []
helpfuls = []
products = []
hours = []
# names = []

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

# match=False
# while(match==False):
# for _ in range(1000):
while len(driver.find_elements_by_class_name('title')) <= 2900:
	print('obs retrieved: '+str(len(driver.find_elements_by_class_name('title'))))
	lastCount = lenOfPage
	time.sleep(2)
	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	# if lastCount==lenOfPage:
		# match=True

print('parsing...')
dateComment = driver.find_elements_by_class_name('apphub_CardTextContent')
title = driver.find_elements_by_class_name('title')
hour = driver.find_elements_by_class_name('hours')
helpful = driver.find_elements_by_class_name('found_helpful')
product = driver.find_elements_by_class_name('apphub_CardContentMoreLink.ellipsis')
# name = driver.find_elements_by_class_name('apphub_CardContentAuthorName.online.ellipsis')

print('parsing dates and comments..')
for d in dateComment:
	dates.append(re.findall('\:.*[0-9]+', d.text)[0][1:])
	comments.append(''.join(re.split('\n', d.text)[1:]))

print('parsing titles..')
for t in title:
	titles.append(t.text)

print('parsing number of helpfuls..')
for h in helpful:
	if len(re.findall('^[0-9]+', h.text)) > 0:
		helpfuls.append(re.findall('^[0-9]+', h.text)[0])
	else:
		helpfuls.append(0)

print('parsing played hours..')
for h in hour:
	if len(re.findall('[0-9]+.*[0-9]', h.text)) > 0:
		hours.append(re.findall('[0-9]+.*[0-9]', h.text)[0])
	else:
		hours.append(0)

print('parsing number of products..')
for p in product:
	if len(re.findall('[0-9]+', p.text)) > 0:
		products.append(re.findall('[0-9]+', p.text)[0])
	else:
		products.append(0)
# for n in name:
	# names.append(n.text)

dat = pd.DataFrame()
# dat['name'] = pd.Series(names)
dat['product'] = pd.Series(products)
dat['hour'] = pd.Series(hours)
dat['title'] = pd.Series(titles)
dat['date'] = pd.Series(dates)
dat['helpful'] = pd.Series(helpfuls)
dat['comment'] = pd.Series(comments)

print('writing file...')

dat.to_csv('Cities_skylines.csv', encoding='utf-8', sep=',', index=False)
driver.close()
print('done')