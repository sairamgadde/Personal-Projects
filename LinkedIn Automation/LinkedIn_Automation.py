import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
username = "ogadde1@student.gsu.edu"
password = "yogI5_li"
search_for = "Technical Recruiter"
g_URL = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
chromeDriver = "/Users/gadde/Downloads/chromedriver"
g_nTimeSecToWait = 30 * 24 * 60 * 60  # 30 days


def Login(aBrowserDriver):
    aBrowserDriver.get(g_URL)
    aBrowserDriver.maximize_window()
    aWaitNextPage = WebDriverWait(aBrowserDriver, g_nTimeSecToWait)  # Wait up to x seconds (30 days).
    aWaitNextPage.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/signup/cold-join')]")))
    # fill the username and password
    aInputElementUsername = aBrowserDriver.find_element_by_xpath("//input[contains(@id,'username')]")
    aInputElementUsername.send_keys(username)
    aInputElementPassword = aBrowserDriver.find_element_by_xpath("//input[contains(@id,'password')]")
    aInputElementPassword.send_keys(password)
    time.sleep(1)
    aLogin = aBrowserDriver.find_element_by_xpath("//button[contains(@aria-label,'Sign in')]")
    aLogin.click()


def NavigateToOnePage(aBrowserDriver, sPageLink):
    time.sleep(2)
    aBrowserDriver.get(sPageLink)


aBrowserDriver = webdriver.Chrome(chromeDriver)
Login(aBrowserDriver)
print("Login Successful")

aSearch = aBrowserDriver.find_element_by_xpath("//input[contains(@placeholder, search)]")
aSearch.send_keys(search_for)
aSearch.send_keys(Keys.ENTER)

search_keyword = search_for.split()
visit_link = "https://www.linkedin.com/search/results/all/?keywords="
for i in range(len(search_keyword)):
    if i == len(search_keyword) - 1:
        visit_link += search_keyword[i]
    else:
        visit_link += search_keyword[i] + "%20"
visit_link += "&origin=GLOBAL_SEARCH_HEADER"

for i in range(10):
    print("page", i+1)
    visit_page = visit_link + "&page=" + str(i+1)
    print(visit_page)
    NavigateToOnePage(aBrowserDriver, visit_page)
    time.sleep(30)
    aBrowserDriver.execute_script("window.scrollTo(350, 700)")
    time.sleep(3)
    aBrowserDriver.execute_script("window.scrollTo(700, document.body.scrollHeight)")
    time.sleep(2)
    source_code = BeautifulSoup(aBrowserDriver.page_source, features="html.parser")
    profiles_block = source_code.find('div', {'class': 'search-results-page core-rail'})
    each_profile_block = profiles_block.find_all('div', {'class': 'search-result__wrapper'})

    for one_pro_block in each_profile_block:
        link_info = one_pro_block.find('div', {'class': 'search-result__info pt3 pb4 ph0'})
        link = link_info.find('a', {'class': 'search-result__result-link ember-view'})
        profile_name = link.find('span', {'class': 'name actor-name'}).text.split(' ')
        profile_name = profile_name[0]
        link = link['href']
        print(link)
        NavigateToOnePage(aBrowserDriver, "https://www.linkedin.com" + link)
        time.sleep(2)
        aConnect = aBrowserDriver.find_element_by_xpath("//button[contains(@class,'pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 "
                                                        "artdeco-button--primary ember-view')]")
        aConnect.click()
        time.sleep(2)
        message = "Hello " + profile_name + ',\n'
        text = aBrowserDriver.find_element_by_xpath("//textarea[contains(@name,'message')]")
        text.send_keys(message)
