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

def debug():
    with open("test.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

def get_tweets(path):
    flag = 0
    tweet_count = 0
    id_set = []
    timeout = 3
    last_write_time = time.time()
    while True:
        print(f"Found {tweet_count} tweet(s) currently.")
        current_time = time.time()
        # 提取推文
        tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
        # 寫入推文到文件
        with open(path, "a", encoding="utf-8") as file:
            for tweet in tweets:
                id = tweet.get_attribute("id")
                if id not in id_set:
                    id_set.append(id)
                    tweet_count += 1
                    spans = tweet.find_elements(By.TAG_NAME, "span")
                    file.write(f"{tweet_count}. ")
                    for span in spans:
                        if "r-qvk6io" not in span.get_attribute(
                            "class"
                        ) and "r-lrvibr" not in span.get_attribute("class"):
                            file.write(span.text.replace("\n", ""))

                    for i in range(2):
                        file.write("\n")
                    last_write_time = time.time()

        if flag == 1:
            print(f"Found {tweet_count} tweet(s) FINALLY.")
            break
        # 等待新推文加載
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="tweetText"]')
            )
        )

        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # 等待新的推文加載

        if current_time - last_write_time > timeout:
            flag = 1


my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--user-agent={my_user_agent}")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

email = "AN4126068@gs.ncku.edu.tw"
username = "ccep_an4126068"
password = "an4126068"

keyword = "tsla elon musk"
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
# https://twitter.com/search?q=tsla%20elon%20musk%20since%3A2020-01-01%20until%3A2022-01-01

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

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]'))
)


# for i in range(10):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')

# print(f"捕獲的推文數量：{len(tweets)}")


# with open("./Data/tweets.txt", "w", encoding="utf-8") as file:
#     count = 1
#     for tweet in tweets:
#         spans = tweet.find_elements(By.TAG_NAME, "span")
#         file.write(f"{count}. ")
#         for span in spans:
#             file.write(span.text.replace("\n", ""))
#         count += 1
#         for i in range(2):
#             file.write("\n")

while True:
    try:
        get_tweets(
            f"./Data/{keyword.replace(" ", " - ")}_{start_date}_{end_date}.txt".replace(" ", "")
        )
        break
    except Exception as e:
        print(f"{e}")
