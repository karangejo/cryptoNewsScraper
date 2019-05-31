#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import socket
import requests

def get_links():
    html_page = urllib2.urlopen("https://www.coindesk.com")
    soup = BeautifulSoup(html_page)
    links= []
    skip_links = ["/wp-json","/wp-content/","/page/","/about","/blog","/press","/employer-details","/events","/editorial-policy","/terms-conditions","/privacy-policy","/advertising","/newsletters"]
    
    # find all the links in the page
    for link in soup.findAll(href=re.compile("http.*")):
        extracted_link = link.get('href')
        # check if the links are not blacklisted
        res = [ele for ele in skip_links if (ele not in extracted_link)]
        if len(res) == len(skip_links) and "www.coindesk.com" in extracted_link and extracted_link != "https://www.coindesk.com/":
            print(" Link: " + extracted_link)
            links.append(extracted_link)
    return links

# get the links
coindesk_article_links = get_links()

article_list = [""] * len(coindesk_article_links)

# for each article link extract the text of the article
for index, article in enumerate(coindesk_article_links):
    response = requests.get(article)
    parsed_html = BeautifulSoup(response.content)
    # extract the div with class entry-content
    articles = parsed_html.findAll("div", {"class":"entry-content"})
    for element in articles:
        # get all the p tags
        ptags = element.findAll("p")
        for tag in ptags:
            tag_string = str(tag)
            # filter some p tags out
            if "<em>" not in tag_string and "href" not in tag_string and "<img" not in tag_string:
                # get the text and filter out the unicode chars
                sentence = re.sub(r'&.*?;','', tag.getText())
                article_list[index] = article_list[index] + sentence.encode("ascii", "ignore")

for complete_article in article_list:
    print("\n\n{****} ARTICLE {****} ")
    print(complete_article)
