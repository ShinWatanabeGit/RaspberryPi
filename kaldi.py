import re
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import line

URL = "https://map.kaldi.co.jp/kaldi/articleList?account=kaldi&accmd=1&ftop=1&kkw001=2026-02-28T10%3A11%3A31"
SEARCH_TEXTS = ["西新井", "草加", "厚木", "海老名", "北千住"]

# ヘッドレス設定（画面表示なし）
options = Options()
options.set_preference("dom.webnotifications.enabled", False)
options.add_argument("--headless")
options.binary_location = "/usr/bin/firefox"
service = Service(executable_path="/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get(URL)

    # JS描画待ち（必要に応じて調整）
    sleep(1)

    page_source = driver.page_source

    for text in SEARCH_TEXTS:
        if text in page_source:
            line.send_line_message(f"✅ CALDIセール情報 '{text}' を確認！")

finally:
    driver.quit()
