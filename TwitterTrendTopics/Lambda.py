import requests
import json
import boto3

print("getTrendTopics lambda starting!")
    
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("TwitterTrendTopics23424768")
s3 = boto3.resource('s3')
bucket = s3.Bucket("diotwittertrends")
    
def lambda_handler(event, context):
    print(event)
    print(context)
    json_response = connect_to_endpoint(search_url, query_params)
    as_of = json_response[0]['as_of']
    asof_splitted = as_of.split('T')
    key = asof_splitted[0]+"/"+asof_splitted[1]+".json"
    file=""
    for item in json_response[0]['trends']:
        item['as_of'] = as_of
        table.put_item(Item=item)
        file +=json.dumps(item)+"\n"
    
    bucket.put_object(Key=key, Body=file)
    return {
        'statusCode': 200,
        'body': json.dumps(json_response, indent=4, sort_keys=True)
    }




# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token ="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

search_url = "https://api.twitter.com/1.1/trends/place.json"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'id': 23424768}


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

