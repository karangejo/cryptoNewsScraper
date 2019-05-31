#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import socket
import requests

def get_links(search_term):
    html_page = urllib2.urlopen("https://www.bbc.co.uk/search?q=" + search_term)
    soup = BeautifulSoup(html_page)
    links= []
    #skip_links = ["/wp-json","/wp-content/","/page/","/about","/blog","/press","/employer-details","/events","/editorial-policy","/terms-conditions","/privacy-policy","/advertising","/newsletters"]
    
    # find all the links in the page
    for link in soup.findAll(href=re.compile("http.*")):
        extracted_link = link.get('href')
        if "www.bbc.co.uk/news/" in extracted_link and "localnews" not in extracted_link:
            links.append(extracted_link)
    return links

# get the links
bbc_article_links = get_links("bitcoin")

for art_link in bbc_article_links:
    print(art_link)

article_list = [""] * len(bbc_article_links)

# for each article link extract the text of the article
for index, article in enumerate(bbc_article_links):
    response = requests.get(article)
    parsed_html = BeautifulSoup(response.content)
    #print(parsed_html)
    # extract the div with class 
    articles = parsed_html.findAll("div", {"class":"story-body__inner"})
    for element in articles:
        # get all the p tags
        ptags = element.findAll("p")
        for tag in ptags:
            tag_string = str(tag)
            print(tag_string)
            """
            # filter some p tags out
            #if "<em>" not in tag_string and "href" not in tag_string and "<img" not in tag_string:
                # get the text and filter out the unicode chars
                sentence = re.sub(r'&.*?;','', tag.getText())
                article_list[index] = article_list[index] + sentence.encode("ascii", "ignore")

for complete_article in article_list:
    print("\n\n{****} ARTICLE {****} ")
    print(complete_article)

"""
