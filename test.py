from discord_webhook import DiscordWebhook, DiscordEmbed

# 웹훅 URL 설정
webhook_url = 'https://discord.com/api/webhooks/1233783047523012759/u7-Qh6WMH0jBgI4mSLNZJCXZHGQKDQsOLKnMzBdFFqI__lWPMjPluST501w5_KhCcHjD'

# 덱 이름 설정
deck_name = "덱 이름"
deck_link = "덱 웹페이지 링크"

# 챔피언 정보 리스트 구성
champions = [
    {"image": "https://example.com/link_image1.png", "name": "챔피언 1", "cost": 3, "stars": 2, "items": ["https://example.com/item1.png", "https://example.com/item2.png"]},
    {"image": "https://example.com/link_image2.png", "name": "챔피언 2", "cost": 2, "stars": 3, "items": ["https://example.com/item3.png", "https://example.com/item4.png"]},
    {"image": "https://example.com/link_image3.png", "name": "챔피언 3", "cost": 1, "stars": 1, "items": ["https://example.com/item5.png", "https://example.com/item6.png"]},
    {"image": "https://example.com/link_image4.png", "name": "챔피언 4", "cost": 4, "stars": 3, "items": ["https://example.com/item7.png", "https://example.com/item8.png"]},
    {"image": "https://example.com/link_image5.png", "name": "챔피언 5", "cost": 5, "stars": 1, "items": ["https://example.com/item9.png", "https://example.com/item10.png"]},
    {"image": "https://example.com/link_image6.png", "name": "챔피언 6", "cost": 3, "stars": 2, "items": ["https://example.com/item11.png", "https://example.com/item12.png"]},
    {"image": "https://example.com/link_image7.png", "name": "챔피언 7", "cost": 2, "stars": 2, "items": ["https://example.com/item13.png", "https://example.com/item14.png"]},
    {"image": "https://example.com/link_image8.png", "name": "챔피언 8", "cost": 1, "stars": 3, "items": ["https://example.com/item15.png", "https://example.com/item16.png"]},
    {"image": "https://example.com/link_image9.png", "name": "챔피언 9", "cost": 4, "stars": 1, "items": ["https://example.com/item17.png", "https://example.com/item18.png"]},
    {"image": "https://example.com/link_image10.png", "name": "챔피언 10", "cost": 5, "stars": 3, "items": ["https://example.com/item19.png", "https://example.com/item20.png"]},
]

# 웹훅 생성
webhook = DiscordWebhook(url=webhook_url)

# 챔피언 정보 추가
def process_champion_info(champions, webhook):
    for i in range(0, len(champions), 2):
        embed = DiscordEmbed(title='', description='', color='03b2f8')
        
        # 첫 번째 챔피언 정보
        embed.add_embed_field(name='챔피언 이미지', value=f"[링크 이미지]({champions[i]['image']})", inline=True)
        embed.add_embed_field(name='챔피언 설명', value=f"**{champions[i]['name']}** 코스트: {champions[i]['cost']} {'⭐' * champions[i]['stars']} 아이템: {' '.join([f'[아이템 이미지]({item})' for item in champions[i]['items']])}", inline=True)
        
        # 두 번째 챔피언 정보가 있을 경우 추가
        if i + 1 < len(champions):
            embed.add_embed_field(name='챔피언 이미지', value=f"[링크 이미지]({champions[i+1]['image']})", inline=True)
            embed.add_embed_field(name='챔피언 설명', value=f"**{champions[i+1]['name']}** 코스트: {champions[i+1]['cost']} {'⭐' * champions[i+1]['stars']} 아이템: {' '.join([f'[아이템 이미지]({item})' for item in champions[i+1]['items']])}", inline=True)
        
        webhook.add_embed(embed)

# 챔피언 정보 추가
process_champion_info(champions, webhook)

# 웹훅 전송
embed_title = DiscordEmbed(title=deck_name, description='', color='03b2f8')
webhook.add_embed(embed_title)

# 덱 링크를 웹훅 제일 하단에 추가
embed_footer = DiscordEmbed(title='', description=deck_link, color='03b2f8')
webhook.add_embed(embed_footer)

response = webhook.execute()
print(response.status_code, response.text)
