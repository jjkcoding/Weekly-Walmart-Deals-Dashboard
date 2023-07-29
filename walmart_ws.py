# Import Necessary Libraries From Selenium, Pandas, and Time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from selenium_stealth import stealth

import random
import pandas as pd
import time
import os
import tqdm
import gspread


cred_path = "D:/Projects/web scraping/google sheets scrape/credentials.json"
token_path = "D:/Projects/web scraping/google sheets scrape/tokens.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1BbQbzkmTUUvvSN_lDANqyjx_28B5qNMLKTlxxzsSWF0"
auth_path = "D:/Projects/web scraping/google sheets scrape/auth.json"


fold_path = "D:/Projects/walmart dashboard/"
ex_path = fold_path + "wm_sale.csv"
s_categories = ["Electronics", "Health and Medicine", "Beauty", "Home Improvement", "Personal Care"]


user_agent_path = "D:/Projects/web scraping/user-agents.txt"
with open(user_agent_path, 'r') as file:
    user_agents = file.readlines()


def rand_user(options):
    options.add_argument("--user-agent={}".format(random.choice(user_agents).strip()))
    return options


# Initialize Driver
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--incognito')
options.add_argument('--disable-blink-features=AutomationControlled')
# options = rand_user(options)
# options.add_argument("--headless=new")


options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)



driver1 = webdriver.Chrome(service = Service(ChromeDriverManager().install()),
                          options = options)

stealth(driver1,
        languages = ["en-US", "en"],
        vendor = "Google Inc.",
        platform = "Win32",
        webgl_vendor = "Intel Inc.",
        renderer = "Intel Iris OpenGL Engine")


driver2 = webdriver.Chrome(service = Service(ChromeDriverManager().install()),
                          options = options)

stealth(driver2,
        languages = ["en-US", "en"],
        vendor = "Google Inc.",
        platform = "Win32",
        webgl_vendor = "Intel Inc.",
        renderer = "Intel Iris OpenGL Engine")



def get_prod_info(cur_driver, site):
    cur_driver.get(site)

    cur_name = cur_driver.find_element("xpath", "//h1[contains(@itemprop, 'name')]").get_attribute("innerText")
    cur_price = cur_driver.find_elements("xpath", "//span[contains(@itemprop, 'price') and contains(@aria-hidden, 'false')]")
    if len(cur_price) > 0:
        cur_price = cur_price[0].get_attribute("innerText")
        if "Now " in cur_price:
            cur_price = cur_price.replace("Now ", "")
        else:
            cur_price = None
    else:
        cur_price = None
    
    cur_old_price = cur_driver.find_elements("xpath", "//span[contains(@aria-hidden, 'true') and contains(@class, 'gray')]")
    if len(cur_old_price) > 0:
        cur_old_price = cur_old_price[0].get_attribute("innerText")
    else:
        cur_old_price = None
    return cur_name, cur_price, cur_old_price



driver1.get("https://www.walmart.com/shop/deals/flash-picks?sort=best_seller")
driver1.find_element("xpath", "//button[contains(@aria-label, 'All filters')]").click()
time.sleep(1)
driver1.find_element("xpath", "//div[text()[contains(., 'Departments')]]").click()
time.sleep(1)
driver1.find_element("xpath", "//button[text()[contains(., 'Show More')]]").click()
time.sleep(1)

all_sections = driver1.find_elements("xpath", "//div[contains(@aria-label, 'All departments')]//div")
str_sections = []
all_index = []
for sec_i in range(len(all_sections)):
    str_sections.append(all_sections[sec_i].find_element("xpath", ".//span[contains(@aria-hidden, 'true') and text()[string-length(.) > 0]]").get_attribute("innerText").strip())
    if str_sections[-1] in s_categories:
        all_index.append(sec_i)

time.sleep(1)

for i in all_index:
    cur_section = all_sections[i].find_element("xpath", ".//span[contains(@aria-hidden, 'true') and text()[string-length(.) > 0]]").get_attribute("innerText").strip()
    print(cur_section)

    all_sections[i].click()
    time.sleep(1)
    driver1.find_element("xpath", "//button[text()[contains(., 'View results')]]").click()
    time.sleep(1)


    all_links = []

    cur_next = [1, 2, 3]
    while len(cur_next) > 0:
        time.sleep(random.randint(1, 3))
        all_link_xpaths = driver1.find_elements("xpath", "//a[contains(@class, 'absolute') and string-length(@href) > 0 and not(contains(@href, '/shop/'))]")
        for cur_x in all_link_xpaths:
            all_links.append(cur_x.get_attribute("href"))
        cur_next = driver1.find_elements("xpath", "//a[contains(@link-identifier, 'Generic Name') and contains(@aria-label, 'Next Page')]")
        if len(cur_next) > 0:
            next_href = cur_next[0].get_attribute("href")
            driver1.get(next_href)

    for cur_link in tqdm.tqdm(all_links):
        time.sleep(random.randint(2, 4))
        cur_name, cur_price, cur_old_price = get_prod_info(driver2, cur_link)
        if cur_price != None:
            cur_price_diff = float(cur_old_price.replace("$", "").replace(",", "")) - float(cur_price.replace("$", "").replace(",", ""))
            cur_perc_diff = cur_price_diff / float(cur_old_price.replace("$", "").replace(",", "")) * 100

            temp_df = pd.DataFrame({
                "Name": [cur_name],
                "Section": [cur_section],
                "URL": [cur_link],
                "Current Price": [cur_price],
                "Old Price": [cur_old_price],
                "Price Difference": ["${:.2f}".format(cur_price_diff)],
                "Percent Difference": ["{:.2f}%".format(cur_perc_diff)]
            })
            if os.path.exists(ex_path):
                temp_df.to_csv(ex_path, index = False, header = False, mode = 'a')
            else:
                temp_df.to_csv(ex_path, index = False)
    
    if i + 1 < len(all_sections):
        driver1.get("https://www.walmart.com/shop/deals/flash-picks?sort=best_seller")
        driver1.find_element("xpath", "//button[contains(@aria-label, 'All filters')]").click()
        time.sleep(1)
        driver1.find_element("xpath", "//div[text()[contains(., 'Departments')]]").click()
        time.sleep(1)
        driver1.find_element("xpath", "//button[text()[contains(., 'Show More')]]").click()
        time.sleep(1)

    all_sections = driver1.find_elements("xpath", "//div[contains(@aria-label, 'All departments')]//div")

driver1.close()
driver2.close()



# transfering csv to google sheets
wm_df = pd.read_csv(ex_path)

# Authenticate with Google Sheets API
gc = gspread.oauth(
    credentials_filename=cred_path,
    authorized_user_filename=auth_path
)

# Open the Google Sheet by name
sh = gc.open('Weekly Walmart Deals')

# Select the worksheet by name
worksheet = sh.worksheet('Sheet1')
worksheet.clear()

# Print Dataframe On Google Sheet
worksheet.update([wm_df.columns.values.tolist()] + wm_df.values.tolist())

