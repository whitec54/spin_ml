# Quick and dirty script to gather data from NewsBank using a GVSU student
# account.
#
# Very WIP.

import getpass
from robobrowser import RoboBrowser

login_url = 'http://ezproxy.gvsu.edu/login?url=http://infoweb.newsbank.com'

# Entry point
def __main__():
	display_welcome()
	username, password = get_user_and_pass()
	browser = login_to_gvsu(username, password)
	selection = display_topics(browser)

# Display the welcome message
def display_welcome():
	print("""
			Welcome to the GVSU NewsBank Scanner
			Note: This program requires a valid GVSU student login
	""")

# Prompt the user for their login information
def get_user_and_pass():
	username = input('Enter your GVSU username: ')
	password = getpass.getpass('Enter you GVSU password: ')
	return username, password

# Login to the site and return the browser object
def login_to_gvsu(username, password):
	browser = RoboBrowser()
	browser.open(login_url)
	form = browser.get_form()
	form['username'].value = username
	form['password'].value = password
	browser.submit_form(form)
	return browser

# Display the available topics and prompt for selection
def display_topics(browser):
	view_all_link = browser.get_link(text='View All Special Reports')
	browser.follow_link(view_all_link)
	links = browser.find_all('a')
	print(links)

__main__()
