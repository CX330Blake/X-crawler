import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--user-agent={my_user_agent}")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

email = "AN4126068@gs.ncku.edu.tw"
username = "ccep_an4126068"
password = "an4126068"
url = "https://twitter.com/search-advanced"

driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
        )
    )
)
email_input = driver.find_element(
    By.CSS_SELECTOR,
    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
)
email_input.send_keys(email)
email_input.send_keys(Keys.ENTER)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
        )
    )
)

check_user = driver.find_element(
    By.CSS_SELECTOR,
    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
)

check_user.send_keys(username)
check_user.send_keys(Keys.ENTER)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
        )
    )
)
password_input = driver.find_element(
    By.CSS_SELECTOR,
    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
)
password_input.send_keys(password)
password_input.send_keys(Keys.ENTER)

# keyword = input("搜尋關鍵字: ")
# start_date = input("起始日期(yyyy/mm/dd): ").replace("/", "")
# end_date = input("終止日期(yyyy/mm/dd): ").replace("/", "")
keyword = "tsla"
start_date = "20200101"
end_date = "20220101"
start_year = start_date[:4]
start_month = int(start_date[4:6].replace("0", ""))
start_day = int(start_date[6:].replace("0", ""))
end_year = end_date[:4]
end_month = int(end_date[4:6].replace("0", ""))
end_day = int(end_date[6:].replace("0", ""))
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='allOfTheseWords']"))
)
search_box = driver.find_element(By.XPATH, '//input[@name="allOfTheseWords"]')
search_box.send_keys(keyword)
start_month_selector = Select(driver.find_element("id", "SELECTOR_2"))
start_day_selector = Select(driver.find_element("id", "SELECTOR_3"))
start_year_selector = Select(driver.find_element("id", "SELECTOR_4"))
end_month_selector = Select(driver.find_element("id", "SELECTOR_5"))
end_day_selector = Select(driver.find_element("id", "SELECTOR_6"))
end_year_selector = Select(driver.find_element("id", "SELECTOR_7"))

start_month_selector.select_by_index(start_month)
start_day_selector.select_by_index(start_day)
start_year_selector.select_by_value(start_year)
end_month_selector.select_by_index(end_month)
end_day_selector.select_by_index(end_day)
end_year_selector.select_by_value(end_year)
time.sleep(30)
