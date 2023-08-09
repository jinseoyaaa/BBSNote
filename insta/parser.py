import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from collections import Counter
from bs4 import BeautifulSoup
import platform
from config.settings import STATIC_DIR, BASE_DIR
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import requests
import folium
from folium.plugins import MarkerCluster

def insta_crawling():
    driver = webdriver.Chrome(r'C:\Users\82109\chromedriver_win32\chromedriver.exe')
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(40)

    # # 사용자 이름과 비밀번호 입력
    # username = driver.find_element(By.NAME, 'username')
    # password = driver.find_element(By.NAME, 'password')
    # username.send_keys('사용자 이름')
    # password.send_keys('비밀번호')

    # # 로그인 버튼 클릭
    # login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    # login_button.click()
    # time.sleep(5)

    word = "제주도맛집"
    url = insta_searching(word)
    driver.get(url)
    time.sleep(7)

    select_first(driver)
    time.sleep(3)

    results = []
    target = 10
    for i in range(target):
        try: 
            data = get_content(driver)
            results.append(data)
            move_next(driver)
        except:
            time.sleep(2)
            move_next(driver)
            
    return results

def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" + word
    return url

def select_first(driver):
    first = driver.find_element(By.CLASS_NAME, '_aagu')
    first.click()
    time.sleep(3)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    # 본문내용
    try:
        content = soup.select('div._a9zs > h1')[0].text
    except:
        content = ' '
        
    # 태그
    tags = re.findall(r'#[^\s#,\<]+', content)
    
    # 날짜정보
    date = soup.select('time._aaqe')[0]['datetime'][:10]
    
    # 좋아요 수
    try:
        like = soup.select('div._ae2s._ae3v._ae3w > section._ae5m._ae5n._ae5o > div > div > span > a > span > span')[0].text
    except:
        like = 0
        
    # 장소정보
    try:
        place = soup.select('div._aaqm')[0].text
    except:
        place = '' 
        
    data = [content, date, like, place, tags]
    
    return data

def move_next(driver):
    right = driver.find_element(By.CLASS_NAME, '_aaqg')
    right.click()
    time.sleep(3)

def makeWordCloud(tags_total):
    if platform.system() == 'Windows':   # 윈도우의 경우
        font_path = "c:/Windows/Fonts/malgun.ttf"
    elif platform.system() == "Darwin":   # Mac의 경우
        font_path = "/Users/$USER/Library/Fonts/AppleGothic.ttf"

    pic_info = STATIC_DIR / 'images/wordcloud1.png'

    STOPWORDS = ['', '#일상', '#맞팔', '#먹팔', '#먹팔맞팔', '#울산맛집', '#소통', '#좋아요', '#데일리', '#이태원맛집', '#먹방', '#맛집']

    tag_total_selected = []
    for tag in tags_total:
        if tag not in STOPWORDS:
            tag_total_selected.append(tag)

    tag_counts_selected = Counter(tag_total_selected)
    tag_counts_selected.most_common(50)

    wordcloud=WordCloud(font_path= font_path, # 사용할 글꼴 경로 
                        background_color="white", # 배경색
                        max_words=100, # 최대 몇 개의 단어를 나타낼 것인지 설정
                        relative_scaling= 0.3, # 워드 클라우드 내 글자들의 상대적인 크기(0~1)
                        width = 800, # 워드클라우드 가로
                        height = 400 # 워드클라우드 세로
                    ).generate_from_frequencies(tag_counts_selected)
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig(pic_info)

def makeMap(places_df):
    places_counts = places_df.value_counts()
    df_location_counts = pd.DataFrame(places_counts)
    locations = list(df_location_counts.index)

    locations_inform = []
    for location in locations:
        try:
            data = find_places(location)
            locations_inform.append(data)
            time.sleep(1)
        except:
            pass

    locations_inform_df = pd.DataFrame(locations_inform)
    locations_inform_df.columns = ['name_official', '경도', '위도', '인스타위치명']
    location_data = pd.merge(locations_inform_df, df_location_counts, how='inner', left_on = 'name_official', right_index=True)
    location_data = location_data.pivot_table(index = ['name_official', '경도', '위도'], values = 'count', aggfunc = 'sum')
    location_data = location_data.reset_index()

    Mt_Hanla = [33.362500, 126.533694]
    map_jeju = folium.Map(location = Mt_Hanla, zoom_start = 11)

    locations = []
    names = []
    for i in range(len(location_data)):
        data = location_data.iloc[i]
        locations.append((float(data['위도']), float(data['경도'])))
        names.append(data['name_official'])
        
    icon_create_function = """\
        function(cluster){
            return L.divIcon({
            html:'<b>' + cluster.getChildCount() + '</b>',
            className: 'marker-cluster marker-cluster-large',
            iconSize: new L.Point(30,30)
            });
        }"""

    marker_cluster = MarkerCluster(
        locations=locations, popups=names,
        name='Jeju',
        overlay=True,
        control=True,
        icon_create_function=icon_create_function
    )

    marker_cluster.add_to(map_jeju)
    folium.LayerControl().add_to(map_jeju)

    map_jeju.save(BASE_DIR/'templates/insta/map.html')

def find_places(searching):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
    headers = {
    "Authorization": "KakaoAK ab43579dc22422a631995fd66f0fd36f"
}

    places = requests.get(url, headers = headers).json()['documents']
    place = places[0]

    name = place['place_name']
    x = place['x']
    y = place['y']
    data = [name, x, y, searching]
    
    return data
