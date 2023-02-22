import requests,json,config,random,time,msvcrt
from itertools import chain
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime


from utils import time_diff,check_limit,update_cookies

def main():
    actions_limit = input("Enter action limit count: ").strip()
    while actions_limit == "" or not actions_limit.isdigit():
        actions_limit = input("Enter action limit count: ").strip()
    
    actions_limit = int(actions_limit)


    proxies = config.proxies
    with open('cookies/cookies.json','r',encoding='utf-8') as cookie_file:
        all_cookies = json.load(cookie_file)["data"]

        while True:
            like_post(all_cookies,actions_limit,proxies)
            time.sleep(3600)


def like_post(all_cookies, actions_limit, proxies):
    try:
        with open('accounts/accounts.json', 'r+', encoding='utf-8-sig') as f:
            #locking the file 
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

            accounts_data = json.load(f)
            accounts = [account for account in accounts_data["data"]]
            tweets = [tweet for tweets in accounts for tweet in tweets['tweets'] if not tweet['liked']]

            for tweet in tweets:
                # checking if tweet is up to 1 hour
                comment_time = tweet['timestamp']
                time_difference = time_diff(comment_time)

                if time_difference >= 1:
                    comments = get_comments(random.choice(all_cookies), tweet, proxies=random.choice(proxies))
                    new_cookies = []

                    if comments[0]:
                        if len(comments[1]) < 1:
                            print("No comments on this tweet")
                            continue

                        kwargs =[
                            {
                                "cookies":cookies,
                                "comments":comments[1],
                                "actions_limit": actions_limit,
                                "proxies":random.choice(proxies)
                            }for cookies in all_cookies]

                        with ThreadPoolExecutor(len(all_cookies)) as executor:
                            likes = []
                            for kwargs in kwargs:
                                like = executor.submit(like_comments, **kwargs)
                                likes.append(like)
                            
                            for like in as_completed(likes):
                                like = like.result()
                                if like[0] or like[0] is None:
                                    if like[2] > 0:
                                        print(f"\n{like[1]['username']} has liked {like[2]} comments and {like[1]['actions']['like_count']} overall\n")
                                        
                                        for account in accounts_data["data"]:
                                            for i in range(len(account["tweets"])):
                                                if account["tweets"][i] == tweet:
                                                    account["tweets"][i]["liked"] = True
                                    elif like[0] is None:
                                        print(f"account {like[1]['username']} reached limit")
                                    new_cookies.append(like[1])
                                else:
                                    print(f"Error liking tweet {like[1]}")
                    else:
                        print(f"Error getting comments: {comments[1]}")

                    update_cookies(new_cookies) 

            # writing the new tweets
            f.seek(0)
            f.truncate()
            json.dump(accounts_data, f, ensure_ascii=False, indent=4, default=str)
            
            #freeing the file
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

    except Exception as error:
        print(error)


def like_comments(cookies={},comments={},actions_limit={},proxies={}):
    likes = 0
    liked = False
    try:
        for  comment in comments:
            actions = cookies["actions"]
            if actions["action_count"] >= actions_limit:
                actions = check_limit(actions)
                if not actions["limit"]:
                    cookies["actions"] = actions["actions"]
                else:
                    liked = None 
                    break

            json_data = {
                    'variables': {
                        'tweet_id': f'{comment["comment_id"]}',
                    },
                    'queryId': 'lI07N6Otwv1PhnEgXILM7A',
                }

            response = requests.post(
                'https://api.twitter.com/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet',
                cookies=cookies["cookies"],
                headers=cookies["headers"],
                json=json_data,
                proxies=proxies
            )
            assert response.status_code <= 200

            cookies["actions"]["action_count"] += 1
            cookies["actions"]["like_count"] += 1
            cookies["actions"]["last_action_time"] = f"{datetime.now()}"
            
            print(f'{cookies["username"]} liked {comment["commenter_id"]}' + "'s comment")
            liked = True
            likes += 1
            time.sleep(5)
        return  liked,cookies,likes
    except Exception as error:
        return liked,error,likes

        


def get_comments(cookies,tweet,proxies={}):
    print(tweet['tweet_id'])
    try:
        params = {
            'variables': '{"focalTweetId":'+'"'+f"{tweet['tweet_id']}"+'"' + ',"cursor":"CgAAAKAcGQYlBhEVEAAA","referrer":"tweet","controller_data":"DAACDAABDAABCgABAPEIREMCCEEKAAIAIAAAAAMiAAMACAEKAAknnX2h56MjBQgACwAAAAAPAAwDAAAAFEEIAkNECPEAACIDAAAAIAAAAAA8DgANCgAAAAAKAA5k+23yuapCawIADwAKABA1tgOH1j3KWAAAAAA=","with_rux_injections":false,"includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true}',
            'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}',
        }
        
        response = requests.get(
        'https://api.twitter.com/graphql/NNiD2K-nEYUfXlMwGCocMQ/TweetDetail',
        params=params,
        cookies=cookies["cookies"],
        headers=cookies["headers"],
        proxies=proxies
        ).json()

        data = response["data"]["threaded_conversation_with_injections_v2"]["instructions"]

        all_comments = []
        comments = []

        for d in data:
            if d["type"] == "TimelineAddEntries":
                for i in d["entries"]:
                    all_comments += i["content"]["items"] if "conversationthread" in i["entryId"] else all_comments

        for comment in all_comments:
            if "tweet_results" not in comment["item"]["itemContent"].keys(): continue
            comment = comment["item"]["itemContent"]["tweet_results"]["result"]
            comments.append({
                "comment_id":comment["rest_id"],
                "commenter_id":comment["legacy"]["user_id_str"]
            })
        
        return True,comments
    except Exception as error:
        return False,error

if __name__ == "__main__":
    main()



