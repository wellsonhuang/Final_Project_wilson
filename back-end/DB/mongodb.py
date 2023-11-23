#資料庫
from collections import Counter
from datetime import datetime, timedelta
from pymongo import MongoClient

total_topic=["運動","生活","國際","娛樂","社會地方","科技","健康","財經"]

def check_duplicate(topic,subtopic,title_list,URL_list,image_list): # 過濾掉資料庫內已經有的
    # 連接到 MongoDB
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
    db = client["News"]
    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_2 = client_2["News"]
    db_3 =client_2["TodayNews"]
    client_3= MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_4 = client_3["News"]
    collection = db[topic]
    collection_2 = db_2[topic]
    collection_3 = db_3[topic]
    collection_4 = db_4[topic]
    

    filtered_title = []
    filtered_url=[]
    filtered_image=[]
    final_filtered_title=[]
    final_filtered_url=[]
    final_filtered_image=[]
    double_filtered_title = []
    double_filtered_url=[]
    double_filtered_image=[]
    third_filtered_title = []
    third_filtered_url=[]
    third_filtered_image=[]
# 遍歷手上的資料清單
    for title,url,image in zip(title_list,URL_list,image_list):
        # 在資料庫中查找與當前標題相符的資料
        result = collection.find_one({'subtopic':subtopic,'title': title})
        
        # 如果找不到相符的資料，則將當前標題添加到篩選後的資料清單
        if result is None:
            filtered_title.append(title)
            filtered_url.append(url)
            filtered_image.append(image)

    for title,url,image in zip(filtered_title,filtered_url,filtered_image):
        # 在資料庫中查找與當前標題相符的資料
        result = collection_4.find_one({'subtopic':subtopic,'title': title})
        
        # 如果找不到相符的資料，則將當前標題添加到篩選後的資料清單
        if result is None:
            third_filtered_title.append(title)
            third_filtered_url.append(url)
            third_filtered_image.append(image)

    for title,url,image in zip(filtered_title,filtered_url,filtered_image):
        # 在資料庫中查找與當前標題相符的資料
        result = collection_2.find_one({'subtopic':subtopic,'title': title})
        
        # 如果找不到相符的資料，則將當前標題添加到篩選後的資料清單
        if result is None:
            double_filtered_title.append(title)
            double_filtered_url.append(url)
            double_filtered_image.append(image)

    for title,url,image in zip(double_filtered_title,double_filtered_url,double_filtered_image):
        # 在資料庫中查找與當前標題相符的資料
        result = collection_3.find_one({'subtopic':subtopic,'title': title})
        
        # 如果找不到相符的資料，則將當前標題添加到篩選後的資料清單
        if result is None:
            final_filtered_title.append(title)
            final_filtered_url.append(url)
            final_filtered_image.append(image)
    # 關閉與 MongoDB 的連接
    client.close()
    return final_filtered_title,final_filtered_url,final_filtered_image

def save_to_db(db_name,topic,insert_data):
    # 連接到 MongoDB
    client = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db = client[db_name]
    collection = db[topic]
# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

         # 插入数据
        collection.insert_one(insert_data)
    except Exception as e:
        print(e) 
    # 關閉與 MongoDB 的連接
    client.close()

def save_to_kmeans_db(db_name,topic,insert_data):
    # 連接到 MongoDB
    client = MongoClient("mongodb+srv://user2:user2@cluster0.zgtguxv.mongodb.net/?retryWrites=true&w=majority")
    db = client[db_name]
    collection = db[topic]
# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

         # 插入数据
        collection.insert_one(insert_data)
    except Exception as e:
        print(e) 
    # 關閉與 MongoDB 的連接
    client.close()

def copy_to_db():
    # 連接到 MongoDB
    client = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    source_db = client["TodayNews"]
    target_db = client["News"]

    # 获取集合名称列表
    collection_names = source_db.list_collection_names()
    
    for collection_name in collection_names:
        # 获取源集合中的所有文档
        source_collection = source_db[collection_name]
        documents = source_collection.find()

        # 将文档插入到目标集合
        target_collection = target_db[collection_name]
        for document in documents:
            # 刪除 _id
            del document['_id']
            # 插入文檔到目標集合
            target_collection.insert_one(document)
    # 關閉與 MongoDB 的連接
    client.close()
    print("DB複製完成!")

def clean_todaydb():
    client = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db = client["TodayNews"]
    # 获取集合名称列表
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        collection = db[collection_name]
        # 清除集合中的所有文档
        collection.delete_many({})
    # 關閉與 MongoDB 的連接
    client.close()

def get_all_data(clientnm,item):
    item_list=[]
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
    db = client[clientnm]
    # 获取集合名称列表
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        # 获取源集合中的所有文档
        collection = db[collection_name]
        for document in collection.find():
            item_list.append(document[item])
    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_2 = client_2[clientnm]
    # 获取集合名称列表
    collection_names = db_2.list_collection_names()
    for collection_name in collection_names:
        # 获取源集合中的所有文档
        collection_2 = db_2[collection_name]
        for document in collection_2.find():
            item_list.append(document[item])
            
    client_3 = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_3= client_3[clientnm]
    # 获取集合名称列表
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        # 获取源集合中的所有文档
        collection_3 = db_3[collection_name]
        for document in collection_3.find():
            item_list.append(document[item])
            
            
            
    # 關閉與 MongoDB 的連接
    client.close()
    return item_list

def get_col_data(collection_name,start_date,end_date):
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
    db_today= client["TodayNews"]
    kw_list=[]
    collection = db_today[collection_name]
    # 檢查是否有日期範圍，並套用查詢條件
    query = {}
    if start_date and end_date:
        query["timestamp"] = {"$gte": start_date, "$lt": end_date}
    for document in collection.find(query):
        kw_list.append(document['new_keyword'])

    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_today_2= client_2["TodayNews"]
    collection_2 = db_today_2[collection_name]
    if start_date and end_date:
        query["timestamp"] = {"$gte": start_date, "$lt": end_date}
    for document in collection_2.find(query):
        kw_list.append(document['new_keyword'])
        
    client_3 = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_today_3= client_3["TodayNews"]
    collection_3 = db_today_3[collection_name]
    if start_date and end_date:
        query["timestamp"] = {"$gte": start_date, "$lt": end_date}
    for document in collection_3.find(query):
        kw_list.append(document['new_keyword'])
        
    return  kw_list

def get_tol_col_data(start_date,end_date):
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
    db_today= client["TodayNews"]
    kw_list = []
    for collection_name in total_topic:
        collection = db_today[collection_name]
        # 檢查是否有日期範圍，並套用查詢條件
        query = {}
        if start_date and end_date:
            query["timestamp"] = {"$gte": start_date, "$lt": end_date}

        for document in collection.find(query):
            kw_list.append(document['new_keyword'])

    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_today_2= client_2["TodayNews"]
    kw_list = []
    for collection_name in total_topic:
        collection_2 = db_today_2[collection_name]
        if start_date and end_date:
            query["timestamp"] = {"$gte": start_date, "$lt": end_date}

        for document in collection_2.find(query):
            kw_list.append(document['new_keyword'])
            
    client_3 = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_today_3= client_3["TodayNews"]
    kw_list = []
    for collection_name in total_topic:
        collection_3 = db_today_3[collection_name]
        if start_date and end_date:
            query["timestamp"] = {"$gte": start_date, "$lt": end_date}

        for document in collection_3.find(query):
            kw_list.append(document['new_keyword'])        
    
    return kw_list

def get_DB_News_data(topic):
    # 連接到 MongoDB
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
    db = client['News']
    # 連接到 MongoDB
    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_2 = client_2['News']
    
    client_3 = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_3 = client_3['News']


    current_datetime = datetime.now()
    end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    start_datetime = end_datetime - timedelta(days=1)
    print(start_datetime)
    print(end_datetime)
    collection = db[topic]
    collection_2 = db_2[topic]
    collection_3 = db_3[topic]
    pipeline = [
        {'$match': {'timestamp': {"$gte": start_datetime, "$lte": end_datetime}}},
        {"$sort": {"timestamp": -1}}
        #,{"$limit": 10}
    ]

    data = list(collection.aggregate(pipeline))
    data_2 = list(collection_2.aggregate(pipeline))
    data.extend(data_2)
    data_3 = list(collection_3.aggregate(pipeline))
    data.extend(data_3)
    #print("這個是data:",list(data))
    return data

#print(get_DB_News_data("運動"))

def get_DB_News_all_data():
    # 連接到 MongoDB
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
    db = client['News']
    # 連接到 MongoDB
    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_2 = client_2['News']
    
    client_3 = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_3 = client_3['News']

    current_datetime = datetime.now()
    end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    start_datetime = end_datetime - timedelta(days=1)
    print(start_datetime)
    print(end_datetime)
    pipeline = [
            {'$match': {'timestamp': {"$gte": start_datetime, "$lte": end_datetime}}},
            {"$sort": {"timestamp": -1}}
            #,{"$limit": 10}
        ]
    all_data=[]
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        collection = db[collection_name]
        collection_2 = db_2[collection_name]
        collection_3 = db_3[collection_name]
        data = list(collection.aggregate(pipeline))
        data_2 = list(collection_2.aggregate(pipeline))
        data_3 = list(collection_3.aggregate(pipeline))
        all_data.extend(data)
        all_data.extend(data_2)
        all_data.extend(data_3)
    #print("這個是data:",list(data))
    return all_data


def calculate_keywords(keywords_list):

    keyword_counts = Counter()
    all_keywords = []
    for kw in keywords_list:
        keywords = kw.split(" ")
        keyword_counts.update(keywords)

    top_keywords = keyword_counts.most_common(10)
    for keyword, count in top_keywords:
        all_keywords.append(keyword)
    return all_keywords
#取得某主題的關鍵每一天
def get_subject_col_data(collection_name,option):
    client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/TodayNews?retryWrites=true&w=majority")
    db_daily = client['關鍵每一天']
    client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
    db_daily_2 = client_2['關鍵每一天']
    client_3 = MongoClient("mongodb+srv://user3:user3@cluster0.z6fmrfb.mongodb.net/?retryWrites=true&w=majority")
    db_daily_3 = client_3['關鍵每一天']
    current_datetime = datetime.now()
    
    if option == 'daily':
        end_datetime = current_datetime - timedelta(days=0)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime - timedelta(days=0)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime - timedelta(days=0)
        start_datetime = end_datetime - timedelta(days=30)
    else:
      return
    collection = db_daily[collection_name]
    collection_2 = db_daily_2[collection_name]
    collection_3 = db_daily_3[collection_name]
    end_datetime=end_datetime.strftime("%Y-%m-%d")
    start_datetime=start_datetime.strftime("%Y-%m-%d")
    print("關鍵字找:大於等於",start_datetime,"小於",end_datetime)
    documents = list(collection.find({"date": {"$gte": start_datetime, "$lt": end_datetime}}))
    documents_2 = list(collection_2.find({"date": {"$gte": start_datetime, "$lt": end_datetime}}))
    documents.extend(documents_2)
    documents_3 = list(collection_3.find({"date": {"$gte": start_datetime, "$lt": end_datetime}}))
    documents.extend(documents_3)
    


    keywords_list = []
    for document in documents:
        keywords = document.get('keywords')
        if keywords:
            keywords_list.extend(keywords)

    hot_keywords_list=calculate_keywords(keywords_list)

    return hot_keywords_list
