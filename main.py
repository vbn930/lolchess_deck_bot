from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed
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
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# 2. 페이지 열기 및 크롤링하기
def crawl_page(driver: webdriver.Chrome, url):
    try:
        # URL로 이동
        driver.get(url)
        elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Champion.css-6e2gh1.e9927jh0"))
    )
        
        # 예: 페이지에서 특정 요소 찾기 (예: 제목 태그 찾기)
        body_element = driver.find_element(By.CLASS_NAME, 'css-s9pipd.e2kj5ne0')
        deck_info_elements = body_element.find_elements(By.CLASS_NAME, 'css-1iudmso.emls75t0')
        
        decks = list()
        
        for deck_info_element in deck_info_elements:
            # 초기 덱 리스트에 있는 덱 정보 스크래핑
            deck = Deck()
            deck.name = deck_info_element.find_element(By.CLASS_NAME, 'css-35tzvc.emls75t4').text
            if "HOT" in deck.name:
                deck.name = deck.name.replace("\n", "").replace("HOT", "")
                deck.name = f'🔥{deck.name}🔥'
                
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
                
            decks.append(deck)
            print(f"덱 '{deck.name}'의 기본 정보 크롤링을 완료하였습니다.")
            
        for deck in decks:
            deck.champs = get_deck_detail(driver=driver, url=deck.detail_link, deck=deck, champs=deck.champs)
            print(f"덱 '{deck.name}'의 챔피온 정보 크롤링을 완료하였습니다.")
        
    except Exception as e:
        print("An error occurred:", e)
        
    return decks

def get_deck_detail(driver: webdriver.Chrome, url, deck: Deck, champs: list):
    driver.get(url)
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "css-11hlchy.e1k9xd3h2"))
    )
    
    champ_elements = driver.find_elements(By.CLASS_NAME, "Slot")
    for i in range(len(champ_elements)):
        champ_element = champ_elements[i]
        try:
            champ_name = champ_element.find_element(By.CLASS_NAME, "css-wgmjlp.ed21b2i3").text
            champ_star = len(champ_element.find_element(By.CLASS_NAME, "css-11hlchy.e1k9xd3h2").find_elements(By.TAG_NAME, "div")) - 1
            for champ in champs:
                if champ.name in champ_name:
                    champ.star = champ_star
        
        except NoSuchElementException:
            pass
    
    return champs

def send_discord_webhook(webhook: DiscordWebhook, deck: Deck):
    time.sleep(2)
    embed = DiscordEmbed(title=deck.name, url=deck.detail_link)
    
    for champ in deck.champs:
        embed_name = f"{'⭐'*champ.star}{champ.name}{champ.cost}"
        embed_value = f""
        if len(champ.items) != 0:
            item_name = ""
            for item in champ.items:
                if "Emblem" in item:
                    item_name = item.split("/")[-1].split("_")[0]
                else:
                    item_name = item.split("/")[-1].replace("TFT_Item_", "").replace(".png", "")
                embed_value = embed_value + f"**{item_name}**\n"
        else:
            embed_value = "No item\n"*3
        embed.add_embed_field(name=embed_name, value=embed_value)
        
    embed.set_footer(text="롤토체스 인기 덱 알림이")
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    webhook.embeds.clear()

# 3. 드라이버 종료
def close_driver(driver):
    driver.quit()

# 메인 함수
def main():
    # 1. 드라이버 설정
    driver = setup_driver()
    
    # 2. 크롤링할 URL 설정
    url_pbe = "https://lolchess.gg/meta?pbe=true"
    url = "https://lolchess.gg/meta"
    
    # 3. 페이지 크롤링
    decks = crawl_page(driver, url)
    
    webhook_url = 'https://discord.com/api/webhooks/1233783047523012759/u7-Qh6WMH0jBgI4mSLNZJCXZHGQKDQsOLKnMzBdFFqI__lWPMjPluST501w5_KhCcHjD'
    webhook = DiscordWebhook(url=webhook_url)
    
    for deck in decks:
        send_discord_webhook(webhook=webhook, deck=deck)
    
    # 4. 드라이버 종료
    close_driver(driver)

if __name__ == "__main__":
    main()