#情緒分析
from cemotion import Cemotion
from hanziconv import HanziConv
c = Cemotion()
#爬蟲
from Spider.kw_spider import *
from Spider.url_spider import *
from Spider.news_time import *
#摘要
from Summarize.summarization import *
#關鍵字
from Keyword.keyword import get_keyword
from Keyword.hot_keyword import calculate_keywords
# 資料處理
import pandas as pd
import numpy as np
#資料庫
from DB.mongodb import *
#Kmeans
from Kmeans.kmeans import *
from Kmeans.search_news import * 
#PTT
from PTT.choose_ptt_title import *
from PTT.grab_ptt_article import *
from MySQL.copy_cloud_to_local import *
from datetime import datetime,timedelta
#停用詞
stops = []
with open('Summarize\stopWord_summar.txt', 'r', encoding='utf-8-sig') as f:
    for line in f.readlines():
        stops.append(line.strip())

def dataframe(topic,subtopic,title,URL,image_url,content,summary,emotion_value,new_keyword,converted_date,keyword_weight):
    
    insert_data = {
                "topic":topic,
                "subtopic":subtopic,
                "title": title,
                "url":URL,
                "image":image_url,
                "content":content,
                "summary":summary,
                "emotion_value":emotion_value,
                "views":0,
                "new_keyword":new_keyword,
                "timestamp":converted_date,
                "keyword_weight":keyword_weight
                }
    return insert_data

def kw_dataframe(all_keywords,date):
    
    insert_data = {
                'keywords': all_keywords,
                'date': date
                }  
    return insert_data

def newest_kmeans_news_dataframe(topic,news_list,date):
    insert_data = {
                'topic': topic,
                'news_list':news_list,
                'date': date
                }  
    return insert_data

def hot_kmeans_news_dataframe(topic,keyword,news_list,start_news_date,end_news_date,date):
    insert_data = {
                'topic': topic,
                'keyword':keyword,
                'news_list':news_list,
                'start_news_date':start_news_date,
                'end_news_date':end_news_date,
                'date': date
                }  
    return insert_data

def kw(topic,subtopic):
    title_list,URL_list,image_list=grab_yahoo_usersearch(subtopic)
    filtered_title_list,filtered_URL_list,filtered_image_list=check_duplicate(topic,subtopic,title_list,URL_list,image_list)
    for title,URL,image_url in zip(filtered_title_list,filtered_URL_list,filtered_image_list):
        content=get_content(URL)                            #取得該網址的新聞內容
        sentences, indexs =split_sentence(content)          # 按標點分割句子
        tfidf = get_tfidf_matrix(sentences, stops)             # 移除停用詞並轉換為矩陣
        word_weight =get_sentence_with_words_weight(tfidf)    # 計算句子關鍵詞權重
        posi_weight = get_sentence_with_position_weight(sentences)     # 計算位置權重
        scores = get_similarity_weight(tfidf)                  # 計算相似度權重
        sort_weight = ranking_base_on_weigth(word_weight, posi_weight, scores, feature_weight=[3,0,2]) #按句子權重排序
        summary = get_summarization(indexs ,sort_weight, topK_ratio=0.2) # 取得摘要比例
        processed_summary=HanziConv.toSimplified(summary)
        emotion_value=c.predict(processed_summary)
        emotion_value = float("{:.6f}".format(emotion_value))
        new_keywords,keyword_weight=get_keyword(title,summary)
        spider_date=get_date(URL)
        converted_date = datetime.fromisoformat(spider_date[:-1])
        save_to_db("TodayNews",topic,dataframe(topic,subtopic,title,URL,image_url,content,summary,emotion_value,new_keywords,converted_date,keyword_weight))  #放進資料庫

def url(topic,subtopic,spider_url):
    title_list,URL_list,image_list=grab_yahoo_url(spider_url)
    filtered_title_list,filtered_URL_list,filtered_image_list=check_duplicate(topic,subtopic,title_list,URL_list,image_list)
    for title,URL,image_url in zip(filtered_title_list,filtered_URL_list,filtered_image_list):
        content=get_content(URL)                            #取得該網址的新聞內容
        sentences, indexs =split_sentence(content)          # 按標點分割句子
        tfidf = get_tfidf_matrix(sentences, stops)             # 移除停用詞並轉換為矩陣
        word_weight =get_sentence_with_words_weight(tfidf)    # 計算句子關鍵詞權重
        posi_weight = get_sentence_with_position_weight(sentences)     # 計算位置權重
        scores = get_similarity_weight(tfidf)                  # 計算相似度權重
        sort_weight = ranking_base_on_weigth(word_weight, posi_weight, scores, feature_weight=[3,0,2]) #按句子權重排序
        summary = get_summarization(indexs ,sort_weight, topK_ratio=0.2) # 取得摘要比例
        processed_summary=HanziConv.toSimplified(summary)
        emotion_value=c.predict(processed_summary)
        emotion_value = float("{:.6f}".format(emotion_value))
        new_keywords,keyword_weight=get_keyword(title,summary)
        spider_date=get_date(URL)
        converted_date = datetime.fromisoformat(spider_date[:-1])
        save_to_db("TodayNews",topic,dataframe(topic,subtopic,title,URL,image_url,content,summary,emotion_value,new_keywords,converted_date,keyword_weight))  #放進資料庫

def hot_kw(topic):
    current_date =(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")
    start_date=(datetime.now()- timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if topic == '綜合全部':
        kw_list=get_tol_col_data(start_date,end_date)
        all_keywords=calculate_keywords(kw_list)
    else:
        kw_list=get_col_data(topic,start_date,end_date)
        all_keywords=calculate_keywords(kw_list)
    #print(all_keywords,current_date)
    save_to_db("關鍵每一天",topic,kw_dataframe(all_keywords,current_date))  #放進資料庫
    
def do_newest_kmeans(topic):
    current_date =(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")
    if topic == '綜合全部':
        after_total_newest_news_list=newest_news_search(total_newest_news_list)
        matched_ptt_news_list=choose_ptt_data('最新',after_total_newest_news_list)
        save_to_kmeans_db('Kmeans新聞','最新',newest_kmeans_news_dataframe(topic,matched_ptt_news_list,current_date))
    else:
        topic_newest_news_list=get_DB_News_data(topic)
        total_newest_news_list.extend(topic_newest_news_list)
        after_topic_newest_news_list=newest_news_search(topic_newest_news_list)
        matched_ptt_news_list=choose_ptt_data('最新',after_topic_newest_news_list)
        save_to_kmeans_db('Kmeans新聞','最新',newest_kmeans_news_dataframe(topic,matched_ptt_news_list,current_date))

def do_hot_kmeans(topic,option):
    current_date =(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")
    if topic == '綜合全部':
        total_hot_news_dic,start_news_date,end_news_date=hot_all_search_news(option)
        for keyword,total_hot_news_list in total_hot_news_dic.items():
            total_hot_news_list=choose_ptt_data('熱門',total_hot_news_list)
            if option =='daily':
                save_to_kmeans_db('Kmeans新聞','當日熱門',hot_kmeans_news_dataframe(topic,keyword,total_hot_news_list,start_news_date,end_news_date,current_date))
            elif option =='weekly':
                save_to_kmeans_db('Kmeans新聞','當週熱門',hot_kmeans_news_dataframe(topic,keyword,total_hot_news_list,start_news_date,end_news_date,current_date))
            else:
                save_to_kmeans_db('Kmeans新聞','當月熱門',hot_kmeans_news_dataframe(topic,keyword,total_hot_news_list,start_news_date,end_news_date,current_date))

    else:
        topic_hot_news_dic,start_news_date,end_news_date=hot_topic_search_news(topic,option)
        for keyword,topic_hot_news_list in topic_hot_news_dic.items():
            topic_hot_news_list=choose_ptt_data('熱門',topic_hot_news_list)
            if option =='daily':
                save_to_kmeans_db('Kmeans新聞','當日熱門',hot_kmeans_news_dataframe(topic,keyword,topic_hot_news_list,start_news_date,end_news_date,current_date))
            elif option =='weekly':
                save_to_kmeans_db('Kmeans新聞','當週熱門',hot_kmeans_news_dataframe(topic,keyword,topic_hot_news_list,start_news_date,end_news_date,current_date))
            else:
                save_to_kmeans_db('Kmeans新聞','當月熱門',hot_kmeans_news_dataframe(topic,keyword,topic_hot_news_list,start_news_date,end_news_date,current_date))

        
if __name__ == '__main__':

     #清空前天新聞爬蟲(TodayNews)
    clean_todaydb()

    #新聞爬蟲
    kw_topics=["運動","生活"]#         
    subtopics = ['足球','排球','田徑','中職','MLB','日職','韓職','中信兄弟','味全龍','統一獅','樂天桃猿','富邦悍將','台鋼雄鷹',
                 'MLB 洋基','MLB 紅襪','MLB 光芒','MLB 金鶯','MLB 藍鳥','MLB 守護者','MLB 白襪','MLB 皇家','MLB 老虎','MLB 雙城','MLB 太空人','MLB 運動家','MLB 水手','MLB 天使',
                 'MLB 遊騎兵','MLB 大都會','MLB 勇士','MLB 費城人','MLB 馬林魚','MLB 國民','MLB 釀酒人','MLB 紅雀','MLB 紅人','MLB 小熊','MLB 海盜','MLB 響尾蛇','MLB 道奇','MLB 落磯','MLB 巨人','MLB 教士',
                 "NBA","波士頓塞爾蒂克","布魯克林籃網","紐約尼克","費城76人","多倫多暴龍","芝加哥公牛","克里夫蘭騎士","底特律活塞","印第安那溜馬","密爾瓦基公鹿","亞特蘭大老鷹",
                 "夏洛特黃蜂","邁阿密熱火","奧蘭多魔術","華盛頓巫師","金州勇士","洛杉磯快艇","洛杉磯湖人","鳳凰城太陽","沙加緬度國王","丹佛金塊","明尼蘇達灰狼","奧克拉荷馬雷霆",
                 "波特蘭拓荒者","猶他爵士","達拉斯獨行俠","休士頓火箭","曼斐斯灰熊","紐奧良鵜鶘","聖安東尼奧馬刺",
                 "PLG",'新北國王','臺北富邦勇士','桃園璞園領航猿','福爾摩沙台新夢想家','高雄17直播鋼鐵人','新竹街口攻城獅',
                 "T1",'新北中信特攻','臺南台鋼獵鷹','高雄全家海神','台灣啤酒英熊','臺中太陽','桃園永豐雲豹']
    for topic in kw_topics:
        if topic in ["運動"]:
            for subtopic in subtopics:
                print(f"Processing topic: {topic},subtopic: {subtopic}")
                try:
                    kw(topic,subtopic)
                except Exception as e:
                    pass
        else :
            print(f"Processing topic: {topic},subtopic: 氣象")
            try:
                kw(topic,"氣象")
            except Exception as e:
                pass
    #新聞爬蟲
    url_topics=["運動","生活","國際","娛樂","社會地方","科技","健康","財經"] #
    for topic in url_topics:
        if topic in ["運動"]:
            subtopics = ["棒球", "籃球", "網球", "高爾夫球"]
            spider_urls=["https://tw.news.yahoo.com/baseball/",
                        "https://tw.news.yahoo.com/basketball/",
                        "https://tw.news.yahoo.com/tennis/",
                        "https://tw.news.yahoo.com/tennis/"]
        elif topic in ["生活"]:
             subtopics = ["美食消費", "旅遊交通", "文教", "兩性親子","新奇"]
             spider_urls=["https://tw.news.yahoo.com/consumption/",
                         "https://tw.news.yahoo.com/travel/",
                         "https://tw.news.yahoo.com/art-edu/",
                         "https://tw.news.yahoo.com/family-gender/",
                         "https://tw.news.yahoo.com/odd/"]
                        
        elif topic in ["國際"]:
             subtopics = ["亞澳", "中港澳", "歐非", "美洲"]
             spider_urls=["https://tw.news.yahoo.com/asia-australia/",
                         "https://tw.news.yahoo.com/china/",
                         "https://tw.news.yahoo.com/euro-africa/",
                         "https://tw.news.yahoo.com/america/"]
        elif topic in ["娛樂"]:
             subtopics = ["日韓娛樂", "藝人動態", "音樂", "電影戲劇"] 
             spider_urls=["https://tw.news.yahoo.com/jp-kr/",
                         "https://tw.news.yahoo.com/celebrity/",
                         "https://tw.news.yahoo.com/music/",
                         "https://tw.news.yahoo.com/tv-radio/"] 
        elif topic in ["社會地方"]:
             subtopics = ["大台北", "北台灣", "中部離島", "南台灣", "東台灣"]
             spider_urls=["https://tw.news.yahoo.com/taipei/",
                         "https://tw.news.yahoo.com/north-taiwan/",
                         "https://tw.news.yahoo.com/mid-taiwan/",
                         "https://tw.news.yahoo.com/south-taiwan/",
                         "https://tw.news.yahoo.com/east-taiwan/"]
        elif topic in ["科技"]:
             subtopics = ["科技新知", "遊戲相關", "3C家電", "手機iOS", "手機Android"]
             spider_urls=["https://tw.news.yahoo.com/tech-development/",
                         "https://tw.news.yahoo.com/game/",
                         "https://tw.news.yahoo.com/3c-appliances/",
                         "https://tw.news.yahoo.com/applephone/",
                         "https://tw.news.yahoo.com/androidphone/"]
        elif topic in ["健康"]:
             subtopics = ["養生飲食", "癌症", "塑身減重", "慢性病"]
             spider_urls=["https://tw.news.yahoo.com/fitness/",
                          "https://tw.news.yahoo.com/cancer/",
                          "https://tw.news.yahoo.com/beauty/",
                          "https://tw.news.yahoo.com/disease/"
                         ]
        elif topic in ["財經"]:
             subtopics = ["股市匯市","房地產","產業動態","理財就業"]
             spider_urls=["https://tw.news.yahoo.com/stock/",
                          "https://tw.news.yahoo.com/real-estate/",
                          "https://tw.news.yahoo.com/industry/",
                          "https://tw.news.yahoo.com/money-career/"
                         ]
        for subtopic, spider_url in zip(subtopics, spider_urls):
            print(f"Processing topic: {topic},subtopic: {subtopic}")
            try:
                url(topic, subtopic, spider_url)
            except Exception as e:
                pass

    #把新聞複製去大資料庫
    copy_to_db()

    #找關鍵每一天
    topics=["運動","生活","國際","娛樂","社會地方","科技","健康","財經","綜合全部"] # 順序不能換
    for topic in topics:
        hot_kw(topic)

    print("爬完新聞的時間:",datetime.now())

    #爬PTT
    #update_ptt_data()

    #將mysql雲端複製到本地端
    copy()

    #做Kmeans + PTT 比對
    total_newest_news_list = []
    #topics=["運動","生活","國際","娛樂","社會地方","科技","健康","財經","綜合全部"] # 順序不能換
    #熱門系列
    #for topic in topics:
        #for option in ['daily','weekly','monthly']:
            #print("熱門:",topic,option)
            #do_hot_kmeans(topic,option)
        #最新系列
        #print("最新:",topic)
        #do_newest_kmeans(topic)

        

    


