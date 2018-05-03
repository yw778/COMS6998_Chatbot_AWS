import random,json,csv

with open("restaurants.json",'r',encoding='utf-8') as f:
    restaurants = json.load(f)

good_count = 0
bad_count = 0

max_cate = 18
cate={
    'chinese':{
        'good':0,
        'bad':0,
    },'mexican':{
        'good':0,
        'bad':0,
    },'newamerican':{
        'good':0,
        'bad':0,
    },'halal':{
        'good':0,
        'bad':0,
    },'italian':{
        'good':0,
        'bad':0,
    },'japanese':{
        'good':0,
        'bad':0,
    }
}

f1 = open('FILE_1.csv','w',encoding='utf-8')
f2 = open('FILE_2.csv','w',encoding='utf-8')

csv_writer_1 = csv.writer(f1)
csv_writer_1.writerow(['Cuisine','NumberOfReviews','Rating','RestaurantId'])
csv_writer_2 = csv.writer(f2)
csv_writer_2.writerow(['Cuisine','NumberOfReviews','Rating','RestaurantId','Recommended'])

for item in restaurants:
    if  item['review_count'] >= 50 and item['review_count'] <= 500 and good_count < 100 and random.randrange(0,10) * item['rating'] >= 30 and cate[item['categories']]['good'] < max_cate:
        csv_writer_2.writerow([item['categories'],item['review_count'],item['rating'],item['id'],1])
        good_count += 1
        cate[item['categories']]['good'] += 1
    elif item['review_count'] <= 500 and item['review_count'] >= 50 and bad_count < 100 and random.randrange(0,10) * item['rating'] < 20 and cate[item['categories']]['bad'] < max_cate:
        csv_writer_2.writerow([item['categories'],item['review_count'],item['rating'],item['id'],0])
        bad_count += 1
        cate[item['categories']]['bad'] += 1
    else:
        csv_writer_1.writerow([item['categories'],item['review_count'],item['rating'],item['id']])

print(good_count,bad_count)

f1.close()
f2.close()