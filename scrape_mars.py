from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # news scrape
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all('div',class_='content_title')[0].text
    paragraph = soup.find_all('div',class_='article_teaser_body')[0].text

    # img scrape
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    relative_image_path = soup.find_all('img',class_='headerimage fade-in')[0]["src"]
    
    featured_image_url = img_url + relative_image_path

    # fact scrape
    facts_url = 'https://galaxyfacts-mars.com/'

    facts_table = pd.read_html(facts_url)

    df = facts_table[0]
    df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    df = df.drop(0)

    html_table = df.to_html(index=False)

    # hems scrape
    hem_url = "https://marshemispheres.com/"
    browser.visit(hem_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    main_urls = soup.find_all('div', class_='item')

    hem_img_urls=[]

    for x in main_urls:
        title = x.find('h3').text
        url = x.find('a')['href']
        hem_img_url = hem_url + url

        browser.visit(hem_img_url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        hem_img_original = soup.find('div',class_='downloads')
        hem_img_url = hem_img_original.find('a')['href']
        
        img_data = dict({'title':title, 'img_url': hem_url + hem_img_url})
        hem_img_urls.append(img_data)
        
    # dictionary storage
    mars_data= {
            'title': title,
            'paragraph': paragraph,
            'image_url': featured_image_url,
            'facts': html_table,
            'hem_img_urls': hem_img_urls
    }
    
    browser.quit()
    
    return mars_data
        
        