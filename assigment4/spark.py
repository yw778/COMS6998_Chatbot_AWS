import random
from pyspark.mllib.recommendation import ALS
from pyspark.mllib.recommendation import Rating
from pyspark import SparkContext

sc = SparkContext(appName="yjc_spark")

user2art = sc.textFile("s3://yjc-spark/user_artist_data.txt").map(lambda x:[int(k) for k in x.split()])

# weights = [.1, .9]
# seed = random.randrange(100)
# user2art,_ = raw_user2art.randomSplit(weights, seed)

def safe_name(x):
    data = x.split('\t',1)
    if len(data) == 1:
        return None
    else:
        try:
            return (int(data[0]),data[1])
        except:
            return None
    
art2name = sc.textFile("s3://yjc-spark/artist_data.txt").map(safe_name).filter(lambda x: x is not None)

def safe_alias(x):
    data = x.split('\t',1)
    if len(data) == 1:
        return None
    else:
        try:
            return (int(data[0]),int(data[1]))
        except:
            return None
art_alias = sc.textFile("s3://yjc-spark/artist_alias.txt").map(safe_alias).filter(lambda x: x is not None)


b_art_alias = sc.broadcast( art_alias.collectAsMap() )


def convert_alias(x):
    art = b_art_alias.value[x[1]] if x[1] in b_art_alias.value else x[1]
    x[1] = art 
    return Rating(*x)
train_data = user2art.map(convert_alias).cache() 

test_user = 2093760
art4user = user2art.filter(lambda x:x[0] == test_user)
art_name = art4user.map(convert_alias)

art_id = set(art_name.map(lambda x:x[1]).distinct().collect())
art_real_name = art2name.filter(lambda x:x[0] in art_id).map(lambda x:x[1]).collect()
print "Extract the IDs of artists that this user 2093760 has listened to and print their names"
print "------------"
print art_real_name
print "------------"

model = ALS.trainImplicit(train_data,rank = 10, iterations= 5, lambda_=0.01, alpha = 1.0)
recommed_res = model.call("recommendProducts", test_user, 10)
print "let's see the ratings for recommendation"
print "--------------"
print recommed_res
print "--------------"

art2name.cache()
recommend_art_name= [ art2name.lookup(x.product)[0] for x in recommed_res ]
print "the top recommendation for the user 2093760 is"
print "--------------"
print recommend_art_name
print "--------------"