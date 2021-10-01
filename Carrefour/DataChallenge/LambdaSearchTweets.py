import requests
import json
import boto3
import datetime

print("getTweets lambda starting!")

search_url = "https://api.twitter.com/2/tweets/search/recent"
# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(Carrefour lang: en)', 'max_results': 100, 'tweet.fields': 'created_at'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("TwitterTrendTopics23424768")
s3 = boto3.resource('s3')
sns = boto3.client('sns')
bucket = s3.Bucket("diosentimentanalysis")
comprehend = boto3.client('comprehend')
word_filters = ['carrefour']
today = datetime.datetime.now()
key_pref = today.strftime("%Y/%m/%d/%H/")


def lambda_handler(event, context):
    print(event)
    print(context)
    json_response = connect_to_endpoint(search_url, query_params)
    for data in json_response['data']:
        data['created_at'] = data['created_at'].replace("T", " ")
        data['created_at'] = data['created_at'].replace("Z", " ")
        txt = data['text']
        data['sentiment'] = comprehend.detect_sentiment(Text=txt, LanguageCode='en')['Sentiment']
        key = key_pref + data['id']
        bucket.put_object(Key=key, Body=json.dumps(data))

    return {
        'statusCode': 200,
        'body': json.dumps(json_response, indent=4, sort_keys=True)
    }


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "importTopTrends"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

