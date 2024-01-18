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

keyword = "tsla"
start_date = "2020-01-01"
end_date = "2022-01-01"
# keyword = input("請輸入關鍵字(以空格分隔): ")
# start_date = input("請輸入起始日期(yyyy-mm-dd): ")
# end_date = input("請輸入終止日期(yyyy-mm-dd): ")
since = "since:" + start_date
until = "until:" + end_date
search = f"{keyword} {since} {until}".replace(" ", "%20").replace(":", "%3A")
url = f"https://twitter.com/search?q={search}"
# https://twitter.com/search?q=tsla%20since%3A2020-01-01%20until%3A2022-01-01

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
tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')

print(tweets)
with open("./Data/tweets.txt", "w", encoding="utf-8") as file:
    for tweet in tweets:
        spans = tweet.find_elements(By.TAG_NAME, "span")
        for span in spans:
            file.write(span.text)
            file.write("\n")
