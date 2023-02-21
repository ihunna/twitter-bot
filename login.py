import requests,json,random
from datetime import datetime

from make_post import make_post,upload_image


def login(username="",password="",email="",bio_data={},proxies={},cookies={},edit=False):
    try:
        print(f"logging in account {username}")
        with requests.Session() as session:
            url = 'https://api.twitter.com/1.1/onboarding/task.json'
           
            #defining headers
            headers = {
                'authority': 'api.twitter.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                # 'cookie': 'guest_id_marketing=v1%3A167595665094231047; guest_id_ads=v1%3A167595665094231047; kdt=aKHxwDPxiBJGHZAxJfMt5DX7PcKEogn8ykBqelZa; des_opt_in=Y; _gcl_au=1.1.1685196104.1676074394; _gid=GA1.2.323923301.1676297193; at_check=true; lang=en; mbox=PC#12800f8dc8104e928ea00d6d5da8575c.34_0#1739567248|session#fdec33bd6cf6402681a30de9fd856b59#1676324308; _ga_34PHSZMC42=GS1.1.1676321110.3.1.1676322559.0.0.0; _ga=GA1.2.946060602.1675956657; dnt=1; gt=1625242918377095169; att=1-GsXi59kAG0Kor5KdAJXHlQ5UpBo0xLyqeQu3oGwB; personalization_id="v1_vfyH68Gk1Eiojj91+DDM5A=="; guest_id=v1%3A167632517561603793; ct0=3f4cabe3542cdf366df3074d7d40ab4c; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPSLxUyGAToMY3NyZl9p%250AZCIlNzU4NDY1ZGRhYjFmZGQxNTU4OGNkNjYxYmFkMjhhZmE6B2lkIiUwYTM4%250ANmFkZjNmNThiYzE4YTA0OGJiNWYzYTUyMTYyYQ%253D%253D--15d12b8012fb4a8ca2e2c4d5cd0dcb41877f28da',
                'origin': 'https://twitter.com',
                'referer': 'https://twitter.com/',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'x-csrf-token': cookies['ct0'],
                'x-guest-token': cookies['gt'],
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'en-GB',
            }

            #updating cookies and headers in the request session
            session.headers.update(headers)
            session.cookies.update(cookies)
            session.proxies.update(proxies)

            #defining the params for the login starting flow
            params = {
                'flow_name': 'login',
            }

            #defining the data for the login starting flow
            json_data = {
                'input_flow_data': {
                    'flow_context': {
                        'debug_overrides': {},
                        'start_location': {
                            'location': 'unknown',
                        },
                    },
                },
                'subtask_versions': {
                    'action_list': 2,
                    'alert_dialog': 1,
                    'app_download_cta': 1,
                    'check_logged_in_account': 1,
                    'choice_selection': 3,
                    'contacts_live_sync_permission_prompt': 0,
                    'cta': 7,
                    'email_verification': 2,
                    'end_flow': 1,
                    'enter_date': 1,
                    'enter_email': 2,
                    'enter_password': 5,
                    'enter_phone': 2,
                    'enter_recaptcha': 1,
                    'enter_text': 5,
                    'enter_username': 2,
                    'generic_urt': 3,
                    'in_app_notification': 1,
                    'interest_picker': 3,
                    'js_instrumentation': 1,
                    'menu_dialog': 1,
                    'notifications_permission_prompt': 2,
                    'open_account': 2,
                    'open_home_timeline': 1,
                    'open_link': 1,
                    'phone_verification': 4,
                    'privacy_options': 1,
                    'security_key': 3,
                    'select_avatar': 4,
                    'select_banner': 2,
                    'settings_list': 7,
                    'show_code': 1,
                    'sign_up': 2,
                    'sign_up_review': 4,
                    'tweet_selection_urt': 1,
                    'update_users': 1,
                    'upload_media': 1,
                    'user_recommendations_list': 4,
                    'user_recommendations_urt': 1,
                    'wait_spinner': 3,
                    'web_modal': 1,
                },
            }

            #sending the request for the login first flow
            flow= session.post(
                url,
                params=params,
                json=json_data,
            ).json()

            #sending the request to get some secret data from a javascript file
            res = session.get(flow['subtasks'][0]['js_instrumentation']['url'])
            
            #extracting and rearranging the secret value from the javascript file to form a json string
            rf = False
            while not rf:
                #sending the request to get some secret data from a javascript file
                res = session.get(flow['subtasks'][0]['js_instrumentation']['url'])
                try:
                    rf = str(res.text).split('{var ')[1].split('=~(')[0]
                    rf = rf[:285].replace('var ','').split(';')
                    r_data = {}
                    for r in rf:
                        r = str(r).split('=')
                        r_data[r[0]] = int(r[1])

                    s_data = str(res.text).split("'s':")[1][:354].replace("'","")

                    rf = str({
                        "rf":r_data,
                        "s":s_data
                    }).replace("'",'"')
                except:
                    rf = False

            

            #setting the data for the second flow with the secret data from the javascript file above
            json_data = {
                'flow_token': flow['flow_token'],
                'subtask_inputs': [
                    {
                        'subtask_id': 'LoginJsInstrumentationSubtask',
                        'js_instrumentation': {
                            'response': f'{rf}',
                            'link': 'next_link',
                        },
                    },
                ],
            }

            #sending the request for the second flow with the secret data from the javascript file above
            flow= session.post(
                url,
                json=json_data,
            ).json()

            #setting the data for the third flow 
            json_data = {
                'flow_token': flow['flow_token'],
                'subtask_inputs': [
                    {
                        'subtask_id': 'LoginEnterUserIdentifierSSO',
                        'settings_list': {
                            'setting_responses': [
                                {
                                    'key': 'user_identifier',
                                    'response_data': {
                                        'text_data': {
                                            'result': username,
                                        },
                                    },
                                },
                            ],
                            'link': 'next_link',
                        },
                    },
                ],
            }

            #sending the request for the data for the third flow 
            flow = session.post(
                url,
                json=json_data,
            ).json()

            #setting the data for the forth flow 
            json_data = {
                    'flow_token': flow['flow_token'],
                    'subtask_inputs': [
                        {
                            'subtask_id': 'LoginEnterPassword',
                            'enter_password': {
                                'password': password,
                                'link': 'next_link',
                            },
                        },
                    ],
                }
            
            #sending  the request for the forth flow 
            flow = session.post(
                url,
                json=json_data,
            ).json()

            #checking if account is protected
            if flow["subtasks"][0]["subtask_id"] == "LoginAcid":
                json_data = {
                    'flow_token': flow["flow_token"],
                    'subtask_inputs': [
                        {
                            'subtask_id': 'LoginAcid',
                            'enter_text': {
                                'text': email,
                                'link': 'next_link',
                            },
                        },
                    ],
                }

            #setting the data for the last flow 
            json_data = {
            'flow_token': flow['flow_token'],
            'subtask_inputs': [
                    {
                        'subtask_id': 'AccountDuplicationCheck',
                        'check_logged_in_account': {
                            'link': 'AccountDuplicationCheck_false',
                        },
                    },
                ],
            }

            #sending  the request for the last login flow 
            flow = session.post(
                url,
                json=json_data,
            ).json()

            user_id = flow['subtasks'][0]['open_account']['user']['id_str']

        #opening home page to get complete cookies
        params = {
            'variables': '{"withCommunitiesMemberships":true,"withCommunitiesCreation":true,"withSuperFollowsUserFields":true}',
            'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        }

        flow = session.get(
            'https://api.twitter.com/graphql/QXO9SjUJXid3NNEovZXydw/Viewer',
            params=params,
        )

        params = {
            'variables': '{"count":20,"includePromotedContent":true,"latestControlAvailable":true,"requestContext":"launch","withCommunity":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}',
            'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}',
        }

        flow = session.get(
            'https://api.twitter.com/graphql/D8Tklm7zoICDtod5RCC6qg/HomeTimeline',
            params=params,
        )

        #reasigning cookies,headers
        cookies = session.cookies.get_dict()
        headers['x-csrf-token'] = cookies['ct0']

        
        print(f"login successful on | {username}")

        if edit:
            print(f"editing account | {username}")
            bio_data["birthdate_day"] = random.randrange(1,30)
            bio_data["birthdate_month"] = random.randrange(1,12)
            bio_data["birthdate_year"] = random.randrange(1988,2005)

            #updating account information
            session.headers.update({"content-type":"application/x-www-form-urlencoded"})
            profile = session.post('https://api.twitter.com/1.1/account/update_profile.json',data=bio_data)
            assert profile.status_code == 200

            #uploading profile picture
            profile_pic = upload_image(cookies,headers,
                                       'images/profile_pic_images',
                                       proxies=proxies,
                                       type="profile picture")

            #updating profile image
            if "error" not in profile_pic.keys():
                data = {
                    'include_profile_interstitial_type': '1',
                    'include_blocking': '1',
                    'include_blocked_by': '1',
                    'include_followed_by': '1',
                    'include_want_retweets': '1',
                    'include_mute_edge': '1',
                    'include_can_dm': '1',
                    'include_can_media_tag': '1',
                    'include_ext_has_nft_avatar': '1',
                    'include_ext_is_blue_verified': '1',
                    'include_ext_verified_type': '1',
                    'skip_status': '1',
                    'return_user': 'true',
                    'media_id': f'{profile_pic["media_id_string"]}',
                }
                
                #resetting session headers
                session.headers.pop("content-type")

                #updating profile picture
                profile_pic = session.post('https://api.twitter.com/1.1/account/update_profile_image.json',data=data)
                assert profile_pic.status_code== 200

                
                print(f"profile picture updated on | {username}")

            #uploading profile picture
            profile_banner = upload_image(cookies,headers,
                                       'images/profile_banner_images',
                                       proxies=proxies,
                                       type="profile banner picture")
            
            if "error" not in profile_banner.keys():
                data = {
                    'include_profile_interstitial_type': '1',
                    'include_blocking': '1',
                    'include_blocked_by': '1',
                    'include_followed_by': '1',
                    'include_want_retweets': '1',
                    'include_mute_edge': '1',
                    'include_can_dm': '1',
                    'include_can_media_tag': '1',
                    'include_ext_has_nft_avatar': '1',
                    'include_ext_is_blue_verified': '1',
                    'include_ext_verified_type': '1',
                    'skip_status': '1',
                    'return_user': 'true',
                    'media_id': f'{profile_banner["media_id_string"]}',
                }
                
                #updating profile picture
                profile_banner = session.post('https://api.twitter.com/1.1/account/update_profile_banner.json',data=data)
                assert profile_banner.status_code== 200
                
                print(f"profile banner picture updated on | {username}")
                
            #making posts
            post = make_post(cookies,headers,count=1,proxies=proxies)
            if post:
                
                print(f"post successful on | {username}")

            
            print(f"account edit successful on | {username}")
            
        return {
            "user_id":user_id,
            "username":username,
            "actions":{
            "action_count":0,
            "comment_count":0,
            "like_count":0,
            "last_action_time":datetime.now()
            },

            "cookies":cookies,
            "headers":headers
        }
    except Exception as error:
        print(error)