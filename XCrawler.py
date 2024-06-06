import warnings

warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import sys
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import json
import os
from rich import print

class crawler:    
       
    def __init__(self, keyword, start_date, end_date, email, username, password, path, debug) -> None:
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.email = email
        self.username = username
        self.password = password
        self.path = path
        self.chrome_options = webdriver.ChromeOptions()
        my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        service = Service(executable_path=ChromeDriverManager().install())
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument(f"--user-agent={my_user_agent}")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        if not debug:
            self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.tweets_data_list = []
        self.error_count = 0


    # def debug(self):
    #     with open("test.html", "w", encoding="utf-8") as file:
    #         file.write(self.driver.page_source)

    def parse_count_string(self, count_str) -> int:
        multipliers = 1
        if "K" in count_str:
            multipliers = 1000
        elif "M" in count_str:
            multipliers = 1000000
        count_str = count_str.replace("K", "").replace("M", "")

        try:
            count = int(float(count_str) * multipliers)
            return count
        except ValueError:
            return None

    def get_articles(self,  timeout: int, target_count: int):
        
        flag = 0
        id_set = []
        timeout = timeout
        last_write_time = time.time()
        current_count = 0
        while True:
            # print(f"Found {len(tweets_data_list)} tweet(s) currently.", end="\r")
            current_time = time.time()
            articles = self.driver.find_elements(By.TAG_NAME, "article")

            for article in articles:
                data = {
                    "text": "",
                    "likes": 0,
                    "replies": 0,
                    "retweets": 0,
                    "publish_time": "",
                }
                try:
                    publish_time = article.find_element(
                        By.TAG_NAME, "time"
                    ).get_attribute("datetime")
                except Exception:
                    pass
                if publish_time:
                    data["publish_time"] = publish_time.split("T")[0]
                try:
                    tweet = article.find_element(
                        By.CSS_SELECTOR, '[data-testid="tweetText"]'
                    )
                except:
                    continue
                spans = tweet.find_elements(By.TAG_NAME, "span")
                id = tweet.get_attribute("id")

                for span in spans:
                    if "r-qvk6io" not in span.get_attribute(
                        "class"
                    ) and "r-lrvibr" not in span.get_attribute("class"):
                        data["text"] += span.text.replace("\n", "")

                likes = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="like"]'
                ).text
                replies = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="reply"]'
                ).text
                retweets = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="retweet"]'
                ).text
                if likes:
                    data["likes"] = self.parse_count_string(likes)
                else:
                    data["likes"] = 0
                if replies:
                    data["replies"] = self.parse_count_string(replies)
                else:
                    data["replies"] = 0
                if retweets:
                    data["retweets"] = self.parse_count_string(retweets)
                else:
                    data["retweets"] = 0

                if id not in id_set:
                    id_set.append(id)
                    self.tweets_data_list.append(data)
                    last_write_time = time.time()
                    current_count += 1
            
            if current_count >= target_count:
                break
            
            if current_time - last_write_time > timeout:
                flag = 1
            if flag == 1:
                break

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )

            body = self.driver.find_element(By.TAG_NAME, "body")
            if body:
                try:
                    # body.send_keys(Keys.PAGE_DOWN)
                    self.driver.execute_script(
                        "window.scrollTo(0,  document.body.scrollHeight);"
                    )
                    time.sleep(4)
                    
                except Exception as e:
                    # body.send_keys(Keys.PAGE_DOWN)
                    self.driver.execute_script(
                        "window.scrollTo(0,  document.body.scrollHeight);"
                    )
                    time.sleep(4)
            time.sleep(0.5)  

        """
        TODO : Solve the repeat of the tweet sequence 
        
        Use the tweets_dict and tweets_data_list to do this.
        """
        
    def write_to_json(self)->None:
        dir = self.path
        path = dir + f"{self.keyword.replace(" ", " - ")}_{self.start_date}_{self.end_date}.json".replace(
            " ", ""
        )
        tweets_dict = {
            f"tweet_{i + 1}": tweet_data 
            for i, tweet_data in enumerate(self.tweets_data_list)
        }
        print(f"\nWriting to json...")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(tweets_dict, file, ensure_ascii=False, indent=4)
        print("Complete!!!")
     
  
    def crawl(self) -> None:

        current_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
        current_next_date = current_date + datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime(self.start_date,  "%Y-%m-%d").date()
        end_date=datetime.datetime.strptime(self.end_date,  "%Y-%m-%d").date()
        total_days = (end_date - start_date).days + 1
         
        progress_bar_length = 50
               
        while current_date <= end_date:
                     
            email = self.email
            username = self.username
            password = self.password
            
            current_date_str = current_date.strftime("%Y-%m-%d")
            current_next_date_str = current_next_date.strftime("%Y-%m-%d")
            keyword = self.keyword

            since = "since:" + current_date_str
            until = "until:" + current_next_date_str
            search = f"{keyword} {since} {until}".replace(" ", "%20").replace(
                ":", "%3A"
            )
            url = f"https://twitter.com/search?q={search}"
                       
            self.driver.get(url)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                        )
                    )
                )
                print(f"Trying to login...", end="\r")
                email_input = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                )
                
                email_input.send_keys(email)
                email_input.send_keys(Keys.ENTER)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                        )
                    )
                )

                check_user = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                )
                check_user.send_keys(username)
                check_user.send_keys(Keys.ENTER)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                        )
                    )
                )
                password_input = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                )
                password_input.send_keys(password)
                password_input.send_keys(Keys.ENTER)
                print(f"Login successfully", end="\r")
                time.sleep(5)
            except:
                print("Please double check your login information")
                exit()
        
            days_passed = (current_date - start_date ).days
            progress_percent = (days_passed / total_days) * 100 
            progress_bar = "#" * int(progress_percent / 100 * progress_bar_length)           
            
           
            try:
                error_element = self.driver.find_element(By.XPATH, '//span[contains(text(), "Something went wrong")]')                   
            except:
                error_element = None
                
            if error_element is not None:
                    self.error_count += 1
                    os.system('cls')
                    print(f"Something went wrong. I'll try it again... -> {self.error_count} retries")
                    print(f"Progress: [{progress_percent:.2f} %] [{progress_bar.ljust(progress_bar_length)}]", end="\r")
                    # return
                    continue
           
            

            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="tweetText"]')
                )
            )
            self.get_articles(10, 15)  
                   
         
            current_date = current_next_date
            current_next_date += datetime.timedelta(days=1)
            self.error_count = 0

            # 打印进度条
            days_passed = (current_date - start_date ).days
            progress_percent = (days_passed / total_days) * 100 
            progress_bar = "#" * int(progress_percent / 100 * progress_bar_length)           
            print(f"Progress: [{progress_percent:.2f} %] [{progress_bar.ljust(progress_bar_length)}]", end="\r")
            
dir_path = "./new_tweets/"
if not os.path.exists(dir_path):
    os.makedirs(dir_path) 
    
x_crawler = crawler(
    keyword="tesla",
    start_date="2024-01-01",
    end_date="2024-01-02",
    email = "AN4126068@gs.ncku.edu.tw",
    username = "ccep_an4126068",
    password = "an4126068",
    path=dir_path,
    debug=False # This means a headless browser will be used.
)
x_crawler.crawl() 
x_crawler.write_to_json()
