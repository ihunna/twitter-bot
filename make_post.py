import requests,random,time,base64
from PIL import Image
from os import listdir
from os.path import isfile,abspath



def make_post(cookies,headers,count=1,proxies={}):
    try:
        with open('texts.txt', 'r') as file:
            texts = file.read().splitlines()
        image_folder,texts = 'images',texts

        for i in range(count):
            text = random.choice(texts)
            image = upload_image(cookies,headers,image_folder,proxies=proxies,type="post")
            if "error" in image.keys():
                print(f"error uploading image {image['error']}")
                return False
            else: print("image upload successful ...")


            json_data = {
                'variables': {
                    'tweet_text': text,
                    'dark_request': False,
                    'media': {
                        'media_entities': [
                            {
                                'media_id': f'{image["media_id_string"]}',
                                'tagged_users': [],
                            },
                        ],
                        'possibly_sensitive': False,
                    },
                    'withDownvotePerspective': False,
                    'withReactionsMetadata': False,
                    'withReactionsPerspective': False,
                    'withSuperFollowsTweetFields': True,
                    'withSuperFollowsUserFields': True,
                    'semantic_annotation_ids': [],
                },
                'features': {
                    'tweetypie_unmention_optimization_enabled': True,
                    'vibe_api_enabled': True,
                    'responsive_web_edit_tweet_api_enabled': True,
                    'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                    'view_counts_everywhere_api_enabled': True,
                    'longform_notetweets_consumption_enabled': True,
                    'tweet_awards_web_tipping_enabled': False,
                    'interactive_text_enabled': True,
                    'responsive_web_text_conversations_enabled': False,
                    'responsive_web_twitter_blue_verified_badge_is_enabled': True,
                    'responsive_web_graphql_exclude_directive_enabled': False,
                    'verified_phone_label_enabled': False,
                    'freedom_of_speech_not_reach_fetch_enabled': False,
                    'standardized_nudges_misinfo': True,
                    'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
                    'responsive_web_graphql_timeline_navigation_enabled': True,
                    'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                    'responsive_web_enhance_cards_enabled': False,
                },
                'queryId': 'Tz_cZL9zkkY2806vRiQP0Q',
            }

            response = requests.post(
                'https://api.twitter.com/graphql/Tz_cZL9zkkY2806vRiQP0Q/CreateTweet',
                cookies=cookies,
                headers=headers,
                json=json_data,
            )

            assert response.status_code < 400
            if count > 1: time.sleep(random.randrange(5,10))
        return True
    
    except Exception as error:
        print(error)
        return False



def upload_image(cookies,headers,image_folder,proxies={},type="comment"):
    print(f"uploading {type} image")
    try:
        image_folder = abspath(image_folder)
        images = [image for image in listdir(image_folder) if isfile(f"{image_folder}/{image}")]
        image = random.choice(images)
        image_path = f'{image_folder}/{image}'
        with open(image_path,'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        #uploading image
        url = 'https://upload.twitter.com/i/media/upload.json?media_category=tweet_image'
        headers = {
            'authority': 'upload.twitter.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            # 'content-length': '0',
            # 'cookie': 'guest_id_marketing=v1%3A167595665094231047; guest_id_ads=v1%3A167595665094231047; kdt=aKHxwDPxiBJGHZAxJfMt5DX7PcKEogn8ykBqelZa; des_opt_in=Y; _gcl_au=1.1.1685196104.1676074394; _gid=GA1.2.323923301.1676297193; dnt=1; _ga_BYKEBDM7DS=GS1.1.1676386741.2.0.1676386741.0.0.0; lang=en; at_check=true; mbox=PC#12800f8dc8104e928ea00d6d5da8575c.37_0#1739714554|session#eeb39fbe92a244309634645dca87b371#1676471614; _ga_34PHSZMC42=GS1.1.1676467842.8.1.1676469760.0.0.0; personalization_id="v1_x1FOjueI23XooXoEAWdAZw=="; guest_id=v1%3A167647092321854990; gt=1625863009724690435; _ga=GA1.2.946060602.1675956657; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCB1zdFWGAToMY3NyZl9p%250AZCIlM2VhNDI5ZDgxMTkyNzA4NmVhMzY5NGZlMWNiZDA1YWU6B2lkIiU3YmE5%250AMmRhOWY0ZTg4MzFlNWQxYjQ2MGZiZWYyZmJmZg%253D%253D--ebdacf6be488b032dcb773a723c375dcac7ba2c3; auth_token=6a59abc5177dc83cc3afef6c6e824189fb9f2a02; ct0=639d3ccbb5753fbfa85a7678bdddaecb98621369272e68e58aaae86e21bd762c32a8b564e43575e2c9c64407691866ae4faea7b9b16a481b1445f276a6596a2bd55d7f6873e30fc0aca2aa4c32bba065; twid=u%3D1625238489334796288; att=1-uBamSEFpD6ab6a5s1rzZ4edAEeA7M0HhrVh2gm6K',
            'origin': 'https://twitter.com',
            'referer': 'https://twitter.com/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }


        data = {
            'media_data':f'{image_data}'
        }

        image = requests.post(url,cookies=cookies, 
                              headers=headers,
                              data=data,
                              proxies=proxies).json()
        if "errors" in image.keys():
            raise Exception(f"{image}")
        return image
    except Exception as error:
        return {'error':error}