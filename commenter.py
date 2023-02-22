import json,requests,random,base64,sys,config,msvcrt,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime

from login import login
from scrape_users import scrape_users
from utils import check_limit,update_cookies,get_cookies
from make_post import upload_image



def main():
    with open('texts.txt', 'r') as file:
        texts = file.read().splitlines()
    image_folder,texts = 'images',texts

    proxies = config.proxies
    all_cookies = []

    print('\n------------------------------choose and action------------------------------\n')
    print('[1] Get cookies from account')
    print('[2] Scrape accounts from the following lists')
    print('[3] Start commenting & liking (note) you will have to start liker.py separately\n')

    action = input("Enter number: ").strip()
    while action == "" or action not in ('1','2','3'):
        action = input("Enter number: ").strip()
    action = int(action)

    if action == 1:
        print("\nappend new accounts? (Y/n) y for yes, n for no")
        append = input("append new account? (Y/n): ").strip().lower()
        while append not in ("y", "n","yes","no"):
            append = input("please enter y or n, yes or no: ").strip().lower()
        append = True if append in ("y","yes") else False

        print("edit accounts bio? (Y/n) y for yes, n for no")
        edit = input("edit accounts bio? (Y/n): ").strip().lower()
        while edit not in ("y", "n","yes","no"):
            edit = input("please enter y or n, yes or no: ").strip().lower()
        edit = True if edit in ("y","yes") else False

        loginusers(proxies,append=append,edit=edit)
        return

    elif action == 2:
        print("enter target account")
        target = input("Enter target account): ").strip().lower()
        while target == "":
            target = input("Please enter target account: ").strip().lower()

        print("\nappend new accounts? (Y/n) y for yes, n for no")
        append = input("Append new account? (Y/n): ").strip().lower()
        while append not in ("y", "n","yes","no"):
            append = input("Please enter y or n, yes or no: ").strip().lower()
        append = True if append in ("y","yes") else False

        print(f"\ndo you want to scrape all {target}'s following/followers? (Y/n) y for yes, n for no")
        all_items = input(f"Do you want to scrape all {target}'s following/followers? (Y/n): ").strip().lower()
        while all_items not in ("y", "n","yes","no"):
            all_items = input("please enter y or n, yes or no: ").strip().lower()
        all_items = True if all_items in ("y","yes") else False
        
        if not all_items:
            limit = input("Enter limit count: ").strip()
            while limit == "" or not limit.isdigit():
                limit = input("Please limit count: ").strip()
        limit = int(limit) if not all_items else 0


        scrape_accounts(target,limit,proxies,append=append,all_items=all_items)
        return

    elif action == 3:
        actions_limit = input("Enter action limit count: ").strip()
        while actions_limit == "" or not actions_limit.isdigit():
            actions_limit = input("Enter action limit count: ").strip()
        actions_limit = int(actions_limit)
    else:
        raise Exception('No action chosen between (1,2,3)')

    with open('cookies/cookies.json','r',encoding='utf-8-sig') as cookie_file:
        all_cookies = json.load(cookie_file)["data"]
        if len(all_cookies) < 1:
            raise Exception("Empty cookies file, run commenter.py and choose 1 to login users and obtain cookies")

    
    while True:
        check_update(all_cookies,image_folder,texts,actions_limit)
        time.sleep(10)


def check_update(all_cookies,image_folder,texts,actions_limit):
    proxies = config.proxies
    try:
        with open(f"accounts/accounts.json","r+",encoding="utf-8") as f:
            #locking the file 
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

            accounts = json.load(f)
            for account in accounts["data"]:
                cookies = random.choice(all_cookies)
                actions = cookies["actions"]
                if actions["action_count"] >= actions_limit:
                    actions = check_limit(actions)
                    if not actions["limit"]:
                        cookies["actions"] = actions["actions"]

                        #rewriting updated cookies to account for new limit
                        update_cookies([cookies])
                    
                    else:
                        print(f"account {cookies['username']} reached limit")
                        #rewriting updated cookies to account for new limit

                        # writing the new tweets
                        f.seek(0)
                        f.truncate()
                        json.dump(accounts,f,ensure_ascii=False,indent=4,default=str)

                        update_cookies([cookies])
                        break

                tweets = account["tweets"]
                tweet = check_feed(cookies["cookies"],cookies["headers"],account["user_id"],proxies=random.choice(proxies))
                tweet_ids = [tweet['tweet_id'] for tweet in tweets]
                
                if tweet['tweet_id'] not in tweet_ids:
                    print("------------------------New Tweet--------------------------")
                    print(f'{tweet["text"]}')
                    
                    kwargs = [
                        {
                            "cookies":cookies,
                            "tweet":tweet,
                            "image_folder":image_folder,
                            "text":random.choice(texts),
                            "proxies":random.choice(proxies),
                            "actions_limit":actions_limit
                        }for cookies in all_cookies]

                    new_cookies = []
                    with ThreadPoolExecutor(max_workers=len(all_cookies)) as executor:
                        futures = []
                        for kwargs in kwargs:
                            future = executor.submit(comment, **kwargs)
                            futures.append(future)

                        for future in as_completed(futures):
                            result = future.result()
                            if result[0]:print(f'{result[1]["username"]} commented on this post and {result[1]["actions"]["comment_count"]} posts overall')

                            if result[0]:new_cookies.append(result[1])
                        
                        update_cookies(new_cookies)

                    account["tweets"].append(tweet)
                    print("commented on this tweet")
                    print("------------------------Done With Tweet--------------------------\n")


                #rewriting updated cookies to account for new limit
                cookies["actions"]["action_count"] += 1
                cookies["actions"]["last_action_time"] = f"{datetime.now()}"
                update_cookies([cookies])
             
                time.sleep(5)

             # writing the new tweets
            f.seek(0)
            f.truncate()
            json.dump(accounts,f,ensure_ascii=False,indent=4,default=str)

            #freeing the file
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
    except Exception as error:
        print(error)


def check_feed(cookies,headers,user_id,proxies={}):
    print("checking feed ....")
    try:
        params = {
            'variables':'{"userId":'+'"'+f"{user_id}"+'"' + ',"count":2,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true}',
            'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"freedom_of_speech_not_reach_appeal_label_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}',
        }

        response = requests.get(
            'https://api.twitter.com/graphql/rCpYpqplOq3UJ2p6Oxy3tw/UserTweets',
            params=params,
            cookies=cookies,
            headers=headers,
            proxies=proxies
        )

        data = response.json()["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
        for entry in data:
            data = entry["entries"][0]["content"]["itemContent"]["tweet_results"] if entry["type"] == "TimelineAddEntries" else data

        tweet = {
            "tweet_id":data["result"]["rest_id"],
            "text":data["result"]["legacy"]["full_text"],
            "liked":False,
            "timestamp": datetime.now()
        }
        return tweet
    except Exception as error:
        return error

def comment(cookies={},tweet={},image_folder="",text="",proxies={},actions_limit=0):
    print("commenting")
    try:
        actions = cookies["actions"]
        if actions["action_count"] >= actions_limit:
            actions = check_limit(actions)
            if not actions["limit"]:
                cookies["actions"] = actions["actions"]

                print(f"account {cookies['username']} limit has been reset")
            else:
                print(f"account {cookies['username']} reached limit")
                return None,cookies
        

        #uploading comment image
        image = upload_image(cookies["cookies"],cookies["headers"],image_folder,proxies=proxies)
        if "error" in image.keys() or "errors" in image.keys():
            print(f"error with uploading  {image['error']}")
            return False,cookies
        else: print(f"image upload successful on | {cookies['username']}")

        #making comment
        json_data = {
            'variables': {
                'tweet_text': text,
                'reply': {
                    'in_reply_to_tweet_id': f'{tweet["tweet_id"]}',
                    'exclude_reply_user_ids': [],
                },
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
            cookies=cookies["cookies"],
            headers=cookies["headers"],
            json=json_data,
            proxies=proxies
        )
        comt = response.json()
        if "errors" in comt.keys():
            print("-------------------------------------------------------------------------------\n")
            print(comt)
            print("-------------------------------------------------------------------------------\n")
            return False, cookies
        
        cookies["actions"]["action_count"] += 1
        cookies["actions"]["comment_count"] += 1
        cookies["actions"]["last_action_time"] = f"{datetime.now()}"
        return True,cookies
    except Exception as error:
        print("-------------------------------------------------------------------------------\n")
        print(error)
        print("-------------------------------------------------------------------------------\n")
        return False,cookies


def loginusers(proxies,append=False,edit=False):
    all_cookies = []
    bio_data = {}
    with open ('accounts/account_bio.json','r',encoding='utf-8-sig') as bio:
        bio_data = json.load(bio)

    with open('accounts/users.txt','r') as users_file:
        users = users_file.read().splitlines()
        guest_tokens = get_cookies('https://twitter.com/login',
                                    proxies=random.choice(proxies))
        print("\n---------------------------logging in users-----------------------------\n")
        
        kwargs = [
                {
                    "username":user.split(',')[0],
                    "password":user.split(',')[1],
                    "email":user.split(',')[2] if len(user.split(',')) > 2 else "",
                    "bio_data":bio_data,
                    "proxies":random.choice(proxies),
                    "cookies":guest_tokens,
                    "edit":edit
                }
                for user in users
            ]
        
        with ThreadPoolExecutor(max_workers=len(users)) as executor:
            futures = []
            for kwargs in kwargs:
                future = executor.submit(login, **kwargs)
                futures.append(future)

            for future in as_completed(futures):
                if future.result() is not None:all_cookies.append(future.result())

    if append:
        with open('cookies/cookies.json','r+',encoding='utf-8-sig') as cookies_file:
            file_data = json.load(cookies_file)
            file_data["data"] += all_cookies
            cookies_file.seek(0)
            json.dump(file_data,cookies_file,ensure_ascii=False,indent=4,default=str)
    else:
        with open('cookies/cookies.json','w',encoding='utf-8-sig') as cookies_file:
            json.dump({"data":all_cookies},cookies_file,ensure_ascii=False,indent=4,default=str)

    
def scrape_accounts(target,limit,proxies,append=False,all_items=True,scrape_type='following'):
    print("\n---------------------------scraping accounts-----------------------------\n")
    with open('cookies/cookies.json','r',encoding='utf-8-sig') as cookie_file:
        all_cookies = json.load(cookie_file)["data"]

        cookies = random.choice(all_cookies)
        
        scraped = scrape_users(cookies['cookies'],
                                cookies['headers'],
                                target,limit,
                                type=scrape_type,
                                proxies=random.choice(proxies),
                                append=append,all_items=all_items)
        if not scraped:
            raise Exception(f"error scraping data {scraped}")


if __name__=="__main__":
    main()

