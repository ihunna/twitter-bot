import requests,json
from datetime import datetime



def scrape_users(cookies,headers,target,limit,type="following",proxies={},append=False,all_items=True):
    try:
        entries = []
        url = 'https://api.twitter.com/graphql/fzE3zNMTkr-CJufrDwjC4A/Following'
        if type.lower() == "followers":
            url = 'https://api.twitter.com/graphql/1cgYcnPVHWthBz2tv6aG7Q/Followers'
        
        uid = get_uid(cookies,headers,target,proxies=proxies)
        depth = "followers_count" if type.lower() == "followers" else "friends_count"
        total = uid["legacy"][depth] if all_items else limit
        
        params = {
                    'variables': '{"userId":'+'"'+f"{uid['rest_id']}"+'"' + ',"count":'+'"'+f"{100}"+'"' + ',"includePromotedContent":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}',
                    'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}',
                }
        
        response = requests.get(
            url,
            params=params,
            cookies=cookies,
            headers=headers,
            proxies=proxies
        ).json()

        # with open('test.json','w', encoding='utf-8') as f:
        #     json.dump(response,f,ensure_ascii=False,indent=4)
        # return

        data = response["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
        data = [d for d in data if d["type"] == "TimelineAddEntries"][0]
        entries += [entry for entry in data["entries"] if entry["content"]["entryType"] == "TimelineTimelineItem"]
        cursor = data["entries"][len(data["entries"])-2]["content"]["value"]


        while len(entries) < total:
            print(len(entries))
            params = {
                    'variables': '{"userId":'+'"'+f"{uid['rest_id']}"+'"' + ',"count":'+'"'+f"{100}"+'"' + ',"cursor":'+'"'+f"{cursor}"+'"' + ',"includePromotedContent":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}',
                    'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}',
                }
        
            response = requests.get(
                url,
                params=params,
                cookies=cookies,
                headers=headers,
                proxies=proxies
            ).json()

            data = response["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
            data = [d for d in data if d["type"] == "TimelineAddEntries"][0]
            entries += [entry for entry in data["entries"] if entry["content"]["entryType"] == "TimelineTimelineItem"]
            cursor = data["entries"][len(data["entries"])-2]["content"]["value"]


        with open(f'accounts/accounts.json','r+',encoding='utf-8') as f:
            file_data = json.load(f)
            file_data["data"] = [] if append == False else file_data["data"]
            i = 0
            for user in entries:
                followers_count = user["content"]["itemContent"]["user_results"]["result"]["legacy"]["followers_count"]
                if followers_count < 30000:
                    continue
                
                old_user = False
                user_id = user["content"]["itemContent"]["user_results"]["result"]["id"]
                for id in file_data["data"]:
                    if id["id"] == user_id:
                       old_user = True
                       break 

                user_data = {
                                "type": user["content"]["__typename"],
                                "id": user_id,
                                "user_id": user["content"]["itemContent"]["user_results"]["result"]["rest_id"],
                                "username":user["content"]["itemContent"]["user_results"]["result"]["legacy"]["screen_name"],
                                "followers_count":followers_count,
                                "tweets":[]
                                }
                if not old_user:
                    file_data["data"].append(user_data)
                    i+=1
            f.seek(0)
            json.dump(file_data,f,ensure_ascii=False,indent=4)

            print(f"scraped {i} accounts")

            return True
    except Exception as error:
        print(error)
        return error



def get_uid(cookies,headers,username,proxies={}):
    print("getting user's data ....")
    params = {
        'variables': '{"screen_name":'+'"'+f"{username}"+'"' + ',"withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}',
        'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
    }

    response = requests.get(
        'https://api.twitter.com/graphql/rePnxwe9LZ51nQ7Sn_xN_A/UserByScreenName',
        params=params,
        cookies=cookies,
        headers=headers,
        proxies=proxies
    )
    data = response.json()["data"]["user"]["result"]
    return data



