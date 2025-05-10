import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import random

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/google-chrome"  # 加這行
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")  # 如果你是跑在 server/container，通常要加這個
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

nm_names = []
st_names = []
st_address = []
df = pd.read_csv("/workspaces/poetry-demo-test2/toDB/restaurant_no.csv")
for nm_name, st_name, st_url in zip(df['nm_name'], df['st_name'], df['st_url']):
    try:
        driver.get(st_url)
        wait = WebDriverWait(driver,10,0.1)
        print(f"進入攤位{st_name}")
    except:
        print("未進入店家成功!")
        pass

    try:
        address = driver.find_element(By.CLASS_NAME,"CsEnBe").get_attribute("aria-label").replace("地址: ", "")
        print(f"爬取地址{address}成功")
    except:
        address = ''
        print("沒有爬取地址")

    nm_names.append(nm_name)
    st_names.append(st_name)
    st_address.append(address)

driver.quit()
time.sleep(1)

data = {
    "nm_name" : nm_names,
    "st_name" : st_names,
    "st_address" : st_address
}

df = pd.DataFrame(data=data)
df.to_csv("/workspaces/poetry-demo-test2/toDB/restaurant_no_address.csv")