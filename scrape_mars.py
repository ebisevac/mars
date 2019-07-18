from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests as req



def scrape_all():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph=mars_news(browser)

    data={
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "mars_weather":mars_weather(browser),
        "pandas_html":pandas_html(browser),
        "hemispere_image":hemispere_image(browser)
    }
    
    browser.quit()
    return data    

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
        new_elem=soup.select_one("ul.item_list li.slide")
        news_title=new_elem.find('div',class_="content_title").a.text
        news_p=new_elem.find('div',class_="article_teaser_body").text
    except AttributeError:
        return None, None
    
    return news_title, news_p

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather_div = soup.find_all('div', class_="js-tweet-text-container")
    mars_weather=""
    for m_w in mars_weather_div:
        mw1=m_w.text
        print(mw1)
        if mw1[0]=="InSight":
            mars_weather=mw1
        break
    print('MARS WEATHER')
    print(mars_weather)
    return mars_weather

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem=browser.find_by_id('full_image')
    full_image_elem.click()
    browser.is_element_present_by_text('more info      ', wait_time=2)
    more_info_elem=browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    html=browser.html
    try:
        img_soup=BeautifulSoup(html,'html.parser')
        img_url_rel=img_soup.select_one('figure.lede a img').get("src")
        img_url=f'https://www.jpl.nasa.gov{img_url_rel}'
    except AttributeError:
        return None, None
    
    return img_url

def pandas_html(browser):
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Mars Facts', 'Values','Earth']
    dfa=df[['Mars Facts', 'Values']]
    dfa = dfa.set_index('Mars Facts')
    dfa.columns.name = dfa.index.name
    dfa.index.name = None
    pds_html = dfa.to_html()

    return pds_html

def hemispere_image(browser):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    hemisphere_image_urls=[]
    for i in range(4):
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        full_image_elem=browser.find_by_tag('h3')[i]
        full_image_elem.click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_class=soup.find('div',class_="downloads")
        img_url=img_class.ul.li.a["href"]
        title_div=soup.find('div',class_='content')
        title=title_div.h2.text
        hemisphere_image_urls.append({"title":title,"img_url":img_url})
    
    return hemisphere_image_urls

