import string,random,time,json
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType


options = Options()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument("--mute-audio")
options.add_argument("--log-level=OFF")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
options.add_argument('disable-infobars')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
options.add_argument("--disable-extensions")
options.add_argument("--headless")




def get_cookies(url,proxies={}):
    print("\n---------------------------getting guest token---------------------------")

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxies["http"],
        'sslProxy': proxies["http"],
    })

    Options.Proxy = proxy
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    
    cookies = {}
    for cookie in driver.get_cookies():
        cookies[cookie["name"]] = cookie["value"]
    driver.quit()
    cookies['at_check'] = 'true'

    print(f'guest token {cookies["gt"]}')
    return cookies

def generate_sensor_data(type="sensor_data"):
    if type == "sensor_data":
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    elif type == "ct0":
        return ''.join(random.choices(string.digits + string.ascii_letters, k=32)).lower()

    elif type == "gt":
        return ''.join(random.choices(string.digits, k=19))

    elif type == "random_string":
        return  ''.join(random.choices( string.hexdigits[:6] + string.digits, k=10))
    
def load_proxies():
    with open('proxies.txt','r') as pro_file:
        proxies = []
        for proxy in pro_file:
            proxy = proxy.split(":")
            proxy = f"{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
            proxies.append({
                "http":f"http://{proxy}",
            })
    return proxies


def check_limit(actions):
    if time_diff(actions["last_action_time"]) < 24:
        return {"limit":True,"actions":actions}
    actions["actions_count"] = 0
    actions["last_action_time"] = f"{datetime.now()}"
    return {"limit":False,"actions":actions}

def time_diff(old_time):
    old_time = datetime.strptime(str(old_time), "%Y-%m-%d %H:%M:%S.%f")
    time_difference =  datetime.now() - old_time
    return round(time_difference.total_seconds() / 3600)

def update_cookies(new_cookies):
    try:
        # rewriting updated cookies to account for new limit
        with open('cookies/cookies.json', 'r+', encoding='utf-8') as cookies_file:
            file_data = json.load(cookies_file)
            for cookies in new_cookies:
                for i in range(len(file_data["data"])):
                    if cookies["user_id"] == file_data["data"][i]["user_id"]:
                        file_data["data"][i] = cookies

            cookies_file.seek(0)
            json.dump(file_data, cookies_file, ensure_ascii=False, indent=4, default=str)
        return True
    except Exception as error:
        print(error)
        return