# Quick and dirty script to gather data from NewsBank using a GVSU student
# account.
#
# Very WIP.
#
# Note: desperately needs some error checks. Right now if anything goes wrong
# the script will just sit down and cry.

import getpass
from robobrowser import RoboBrowser
import re
from bs4 import BeautifulSoup

login_url = 'http://ezproxy.gvsu.edu/login?url=http://infoweb.newsbank.com'

# Entry point
def main():
    display_welcome()
    username, password = get_user_and_pass()
    browser = login_to_gvsu(username, password, login_url)
    topic_strings = display_topics(browser)
    selection = get_topic_selection(topic_strings)
    process_topic_selection(selection, browser)

# Display the welcome message
def display_welcome():
    print("Welcome to the GVSU NewsBank Scanner\n"
            "Note: This program requires a valid GVSU student login")

# Prompt the user for their login information
def get_user_and_pass():
    username = input('Enter your GVSU username: ')
    password = getpass.getpass('Enter you GVSU password: ')
    return username, password

# Login to the site and return the browser object
def login_to_gvsu(username, password, url):
    browser = RoboBrowser()
    browser.open(url)
    form = browser.get_form()
    form['username'].value = username
    form['password'].value = password
    browser.submit_form(form)
    return browser

# Display the available topics and prompt for selection
def display_topics(browser):
    link_view_all = browser.get_link(text='View All Special Reports')
    browser.follow_link(link_view_all)
    links = browser.find_all('a')
    link_text = []
    for i in range(0, len(links) - 1):
        link_text.append(strip_html_and_whitespace(str(links[i])))
        print(i, link_text[i])
    return link_text

# Remove all HTML tags, leading, and trailing whitespace from a string
def strip_html_and_whitespace(string):
    string = re.sub('<.*?>', '', string)
    string = re.sub('\n', '', string)
    string = re.sub('^\s+', '', string)
    string = re.sub('\s+$', '', string)
    return string

# Ask the user which topic to download and get their response
def get_topic_selection(topic_strings):
    print("Please enter the number of the topic you would like to download:")
    selection = int(input())
    return topic_strings[selection]

# Loop through the articles in the selected topic and download each
def process_topic_selection(selected_topic, browser):
    link_topic = browser.get_link(text=selected_topic)
    browser.follow_link(link_topic)
    sub_topics_list = browser.find_all(attrs={'class':'heading'})
    for i in range(0, len(sub_topics_list)):
        sub_topics_list[i] = strip_html_and_whitespace(str(sub_topics_list[i]))
    print(sub_topics_list)
    topic = re.sub(' ', '', sub_topics_list[0])
    topic = 'list'+(topic)
    ol_data = browser.find(id=topic)
    soup = BeautifulSoup(str(ol_data), 'html.parser')
    link = soup.find('a')
    browser.follow_link(link)
    print(strip_html_and_whitespace(str(browser.find('body'))))
#    for topic in sub_topics_list:
#        topic = re.sub(' ', '', topic)
#        topic = 'list'+(topic)
#        ol_data = browser.find(id=topic)
#        soup = BeautifulSoup(ol_data, 'html.parser')
#        link = soup.find('a')
#        browser.follow_link(link)
#        print(browser.find('body'))




# Download an article
#def download_article(article, browser):

# Run main if this file was opened directly
if __name__ == "__main__":
    main()
