import re
import os
from datetime import datetime
from time import sleep
import message
from dotenv import load_dotenv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def url_open(driver, url):
    driver.get(url)


def login(driver, input_id, input_pass):

    login_url = "https://www.rakuten.co.jp/"

    # Rakuten Top Page Open
    url_open(driver, login_url)
    sleep(2)

    # Login Btn
    login_btn = driver.find_element(By.XPATH, "//a[.//span[text()='ログイン']]")
    login_btn.click()
    sleep(2)

    # Login ID
    login_id = driver.find_element(By.ID, "user_id")
    sleep(2)
    login_id.click()
    sleep(2)
    login_id.send_keys(input_id)
    sleep(2)

    # Next Btn
    next_btn = driver.find_element(By.ID, "cta001")
    sleep(2)
    next_btn.click()
    sleep(2)

    # Login Pass
    login_pass = driver.find_element(By.ID, "password_current")
    sleep(2)
    login_pass.click()
    sleep(2)
    login_pass.send_keys(input_pass)
    sleep(2)

    # Login Btn
    login_btn = driver.find_element(By.ID, "cta011")
    sleep(2)
    login_btn.click()
    sleep(2)


def get_counts(driver):

    summary_url = "https://rakucoin.appspot.com/rakuten/kuji/"

    url_open(driver, summary_url)
    sleep(2)

    pc_number_text = driver.find_element(
        By.XPATH, "//h3[contains(text(),'PC版ラッキーくじ')]"
    ).text
    smartphone_text = driver.find_element(
        By.XPATH, "//h3[contains(text(),'スマホ版ラッキーくじ')]"
    ).text
    other_text = driver.find_element(
        By.XPATH, "//h3[contains(text(),'特殊なくじ')]"
    ).text

    counts = {
        "pc": int(re.search(r"\d+", pc_number_text).group()),
        "smartphone": int(re.search(r"\d+", smartphone_text).group()),
        "other": int(re.search(r"\d+", other_text).group()),
    }

    count = counts["pc"] + counts["smartphone"]

    return count


def draw(input_id, input_pass):

    options = Options()
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument("--headless")
    options.binary_location = "/usr/bin/firefox"
    service = Service(executable_path="/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)

    # wating time setting
    wait = WebDriverWait(driver, 30)

    # Login
    login(driver, input_id, input_pass)

    # URL
    count = get_counts(driver)
    a_tags = driver.find_elements(By.TAG_NAME, "a")
    a_tags = a_tags[:count]

    # Link List Append
    link_list = []
    for a_tag in a_tags:
        href = a_tag.get_attribute("href")
        link_list.append(href)

    # Link click
    i = 0
    while i < len(link_list):

        now = datetime.now()

        try:
            url_open(driver, link_list[i])
            sleep(1)
            image = driver.find_element(By.XPATH, "//img[@id='entry']")
            driver.execute_script("arguments[0].click();", image)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//img[@class='img-responsive']")
                )
            )
            print(
                f"{i+1:02d}/{len(link_list)} {now.hour:02d}:{now.minute:02d}:{now.second:02d} クリック",
                flush=True,
            )

        except (NoSuchElementException, TimeoutException):
            print(
                f"{i+1:02d}/{len(link_list)} {now.hour:02d}:{now.minute:02d}:{now.second:02d} 完了済み",
                flush=True,
            )

        finally:
            i += 1

    driver.quit()


load_dotenv()
users = []

os.system("clear")
message.send("🚀 楽天くじ 開始しました")

for i in range(4):
    users.append(
        {
            "id": os.getenv(f"ID_{i}"),
            "pass": os.getenv(f"PASS_{i}"),
        }
    )

for user in users:
    draw(user["id"], user["pass"])

message.send("🚀 楽天くじ 完了しました")