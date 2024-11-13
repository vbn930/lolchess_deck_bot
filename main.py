from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from dataclasses import dataclass, field


@dataclass
class Chapion:
    name: str = ""
    cost: str = ""
    star: int = 1
    img_src: str = ""
    items: list = field(default_factory=list)
    
@dataclass
class Deck:
    name: str = ""
    champs: list = field(default_factory=list)
    team_code: str = ""
    detail_link: str = ""

# 1. 웹드라이버 설정 및 브라우저 열기
def setup_driver():
    # ChromeDriverManager를 통해 자동으로 크롬 드라이버 설치 및 설정
    driver = webdriver.Chrome()
    return driver

# 2. 페이지 열기 및 크롤링하기
def crawl_page(driver: webdriver.Chrome, url):
    try:
        # URL로 이동
        driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기 (필요시 조정)
        
        # 예: 페이지에서 특정 요소 찾기 (예: 제목 태그 찾기)
        body_element = driver.find_element(By.CLASS_NAME, 'css-s9pipd.e2kj5ne0')
        deck_info_elements = body_element.find_elements(By.CLASS_NAME, 'css-1iudmso.emls75t0')
        
        for deck_info_element in deck_info_elements:
            # URL로 이동
            driver.get(url)
            time.sleep(3)  # 페이지 로딩 대기 (필요시 조정)
            
            deck = Deck()
            deck.name = deck_info_element.find_element(By.CLASS_NAME, 'css-35tzvc.emls75t4').text
            deck.detail_link = deck_info_element.find_element(By.CLASS_NAME, "link-wrapper").find_element(By.TAG_NAME, "a").get_attribute("href")
            
            deck_champ_icons_elements = deck_info_element.find_elements(By.CLASS_NAME, 'Champion.css-6e2gh1.e9927jh0')
            for deck_champ_icons_element in deck_champ_icons_elements:
                champ = Chapion()
                champ_potrait_element = deck_champ_icons_element.find_element(By.CLASS_NAME, "champion-portrait")
                champ.img_src = champ_potrait_element.find_element(By.TAG_NAME, "img").get_attribute("src")
                champ.name = deck_champ_icons_element.find_element(By.CLASS_NAME, "css-yox8du.e9927jh2").text
                champ.cost = deck_champ_icons_element.find_element(By.CLASS_NAME, "css-z1wt3q.e9927jh3").text
                item_elements = deck_champ_icons_element.find_elements(By.CLASS_NAME, "item")
                items = list()
                for item_element in item_elements:
                    item = item_element.find_element(By.TAG_NAME, "img").get_attribute("src")
                    items.append(item)
                    
                champ.items = items
                
                deck.champs.append(champ)

            
            deck.champs = get_deck_detail(driver, deck.detail_link, deck.champs)
            print(deck)
        
    except Exception as e:
        print("An error occurred:", e)

def get_deck_detail(driver: webdriver.Chrome, url, champs: list):
    driver.get(url)
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "css-11hlchy.e1k9xd3h2"))
    )
    
    champ_elements = driver.find_elements(By.CLASS_NAME, "Slot.css-jet0gc.e1k9xd3h0")
    for champ_element in champ_elements:
        try:
            champ_name = champ_element.find_element(By.CLASS_NAME, "css-wgmjlp.ed21b2i3").text
            print(champ_name)
            champ_star = len(champ_element.find_element(By.CLASS_NAME, "css-11hlchy.e1k9xd3h2").find_elements(By.TAG_NAME, "div")) - 1
            print(champ_star)
            
            for champ in champs:
                if champ.name is champ_name:
                    champ.star = champ_star
        except NoSuchElementException:
            # 요소를 찾지 못한 경우 패스
            print("요소를 찾지 못했습니다. 패스합니다.")
                
    return champs
    
# 3. 드라이버 종료
def close_driver(driver):
    driver.quit()

# 메인 함수
def main():
    # 1. 드라이버 설정
    driver = setup_driver()
    
    # 2. 크롤링할 URL 설정
    url = "https://lolchess.gg/meta?pbe=true"
    
    # 3. 페이지 크롤링
    crawl_page(driver, url)
    
    # 4. 드라이버 종료
    close_driver(driver)

if __name__ == "__main__":
    main()