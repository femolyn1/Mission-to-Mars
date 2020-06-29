# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)
   #Set new title and paragraph variable
   news_title, news_paragraph = mars_news(browser)

   # Run all scraping functions and store results in dictionary
   data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
   browser.quit()
   return data

def mars_news(browser):
    # Windows users
    executable_path = {'executable_path': 'c:/users/Femi/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    #Parse the HTML
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Add try / except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    #Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    #Find the more info button and click
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #Add try /except for handling error
    try:
        #Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    
    #Use the base URL to create an absolute URL
    
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url
def mars_facts():
    #Add try /except for handling error
    try:
        #Scrape the entire table using pandas
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    #Assign columns and set index of datafarame
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    #Convert dataframe into html format and add bootstrap
    return df.to_html()

def hemispheres(browser):
    # Visit the Astrogoeology site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #parse the html
    html = browser.html
    hemp_soup = BeautifulSoup(html, 'html.parser')
    #Find the title
    title_elem=hemp_soup.find('div', {'id':'product-section'})
    items=title_elem.find('div', {'class':'collapsible results'})

    children =items.findChildren('div',{'class':'item'}, recursive=True)
    
    hemispheres_image_urls=[]
    for child in children:

    
    
        hemp =child.findChildren('a',recursive=False)[0].attrs['href']
    
        url = 'https://astrogeology.usgs.gov'+ hemp
        
        browser.visit(url)
        

        #parse the html
        html = browser.html
        child_soup = BeautifulSoup(html, 'html.parser')
        try:
            title_elem = child_soup.find("h2",class_="title").get_text()
    
            sample_elem = child_soup.find("a", text ="Sample").get("href")
        except AttributeError:
            title_elem = None
            sample_elem = None
        print(sample_elem)
        hemispheres_image_urls.append({'title':title_elem,
                                     'img':sample_elem})

    return hemispheres_image_urls
        
   
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




























































































































































































































































































































