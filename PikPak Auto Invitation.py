# coding:utf-8
import hashlib
import json
import random
import time
import uuid
import requests
from PIL import Image
from io import BytesIO
import base64
from DrissionPage import ChromiumPage, ChromiumOptions
from colorama import Fore, Style, init
import os
import sys

# Initialize colorama
init()

def ca_f_encrypt(frames, index, pid):
    url = "https://api.kiteyuan.info/cafEncrypt"

    payload = json.dumps({
        "frames": frames,
        "index": index,
        "pid": pid
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def image_parse(image, frames):
    url = "https://api.kiteyuan.info/imageParse"

    payload = json.dumps({
        "image": image,
        "frames": frames
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def sign_encrypt(code, captcha_token, rtc_token):
    url = "https://api.kiteyuan.info/signEncrypt"

    payload = json.dumps({
        "code": code,
        "captcha_token": captcha_token,
        "rtc_token": rtc_token
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def d_encrypt(pid, device_id, f):
    url = "https://api.kiteyuan.info/dEncrypt"

    payload = json.dumps({
        "pid": pid,
        "device_id": device_id,
        "f": f
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


# md5加密算法
def captcha_sign_encrypt(encrypt_string, salts):
    for salt in salts:
        encrypt_string = hashlib.md5((encrypt_string + salt["salt"]).encode("utf-8")).hexdigest()
    return encrypt_string


def captcha_image_parse(pikpak, device_id):
    frames_info = pikpak.gen()
    captcha_image = image_download(device_id, frames_info["pid"], frames_info["traceid"])
    if captcha_image:
        # 读取图片数据并转换为 PIL.Image
        img = Image.open(BytesIO(captcha_image))

        # 将图片转换为 Base64 编码
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # 可根据图片格式调整 format
        base64_image = base64.b64encode(buffered.getvalue()).decode()
    best_index = image_parse(base64_image, frames_info["frames"])
    json_data = ca_f_encrypt(frames_info["frames"], best_index["best_index"], frames_info["pid"])
    f = json_data['f']
    npac = json_data['ca']
    d = d_encrypt(frames_info["pid"], device_id, f)
    verify2 = pikpak.image_verify(frames_info["pid"], frames_info["traceid"], f, npac[0], npac[1], npac[2], npac[3],
                                  d)
    return {
        "response_data": verify2,
        "pid": frames_info["pid"],
        "traceid": frames_info["traceid"],
    }


def image_download(device_id, pid, traceid):
    url = f"https://user.mypikpak.com/pzzl/image?deviceid={device_id}&pid={pid}&traceid={traceid}"

    headers = {
        'pragma': 'no-cache',
        'priority': 'u=1, i'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Download failed, status code: {response.status_code}")
        return None


def ramdom_version():
    version_list = [
        {
            "v": "1.42.6",
            "algorithms": [{"alg": "md5", "salt": "frupTFdxwcJ5mcL3R8"},
                           {"alg": "md5", "salt": "jB496fSFfbWLhWyqV"},
                           {"alg": "md5", "salt": "xYLtzn8LT5h3KbAalCjc/Wf"},
                           {"alg": "md5", "salt": "PSHSbm1SlxbvkwNk4mZrJhBZ1vsHCtEdm3tsRiy1IPUnqi1FNB5a2F"},
                           {"alg": "md5", "salt": "SX/WvPCRzgkLIp99gDnLaCs0jGn2+urx7vz/"},
                           {"alg": "md5", "salt": "OGdm+dgLk5EpK4O1nDB+Z4l"},
                           {"alg": "md5", "salt": "nwtOQpz2xFLIE3EmrDwMKe/Vlw2ubhRcnS2R23bwx9wMh+C3Sg"},
                           {"alg": "md5", "salt": "FI/9X9jbnTLa61RHprndT0GkVs18Chd"}]

        },
        {
            "v": "1.47.1",
            "algorithms": [{'alg': 'md5', 'salt': 'Gez0T9ijiI9WCeTsKSg3SMlx'}, {'alg': 'md5', 'salt': 'zQdbalsolyb1R/'},
                           {'alg': 'md5', 'salt': 'ftOjr52zt51JD68C3s'},
                           {'alg': 'md5', 'salt': 'yeOBMH0JkbQdEFNNwQ0RI9T3wU/v'},
                           {'alg': 'md5', 'salt': 'BRJrQZiTQ65WtMvwO'},
                           {'alg': 'md5', 'salt': 'je8fqxKPdQVJiy1DM6Bc9Nb1'},
                           {'alg': 'md5', 'salt': 'niV'}, {'alg': 'md5', 'salt': '9hFCW2R1'},
                           {'alg': 'md5', 'salt': 'sHKHpe2i96'},
                           {'alg': 'md5', 'salt': 'p7c5E6AcXQ/IJUuAEC9W6'}, {'alg': 'md5', 'salt': ''},
                           {'alg': 'md5', 'salt': 'aRv9hjc9P+Pbn+u3krN6'},
                           {'alg': 'md5', 'salt': 'BzStcgE8qVdqjEH16l4'},
                           {'alg': 'md5', 'salt': 'SqgeZvL5j9zoHP95xWHt'},
                           {'alg': 'md5', 'salt': 'zVof5yaJkPe3VFpadPof'}]
        },
        {
            "v": "1.48.3",
            "algorithms": [{'alg': 'md5', 'salt': 'aDhgaSE3MsjROCmpmsWqP1sJdFJ'},
                           {'alg': 'md5', 'salt': '+oaVkqdd8MJuKT+uMr2AYKcd9tdWge3XPEPR2hcePUknd'},
                           {'alg': 'md5', 'salt': 'u/sd2GgT2fTytRcKzGicHodhvIltMntA3xKw2SRv7S48OdnaQIS5mn'},
                           {'alg': 'md5', 'salt': '2WZiae2QuqTOxBKaaqCNHCW3olu2UImelkDzBn'},
                           {'alg': 'md5', 'salt': '/vJ3upic39lgmrkX855Qx'},
                           {'alg': 'md5', 'salt': 'yNc9ruCVMV7pGV7XvFeuLMOcy1'},
                           {'alg': 'md5', 'salt': '4FPq8mT3JQ1jzcVxMVfwFftLQm33M7i'},
                           {'alg': 'md5', 'salt': 'xozoy5e3Ea'}]
        },
        {
            "v": "1.49.3",
            "algorithms": [{'alg': 'md5', 'salt': '7xOq4Z8s'}, {'alg': 'md5', 'salt': 'QE9/9+IQco'},
                           {'alg': 'md5', 'salt': 'WdX5J9CPLZp'}, {'alg': 'md5', 'salt': 'NmQ5qFAXqH3w984cYhMeC5TJR8j'},
                           {'alg': 'md5', 'salt': 'cc44M+l7GDhav'}, {'alg': 'md5', 'salt': 'KxGjo/wHB+Yx8Lf7kMP+/m9I+'},
                           {'alg': 'md5', 'salt': 'wla81BUVSmDkctHDpUT'},
                           {'alg': 'md5', 'salt': 'c6wMr1sm1WxiR3i8LDAm3W'},
                           {'alg': 'md5', 'salt': 'hRLrEQCFNYi0PFPV'},
                           {'alg': 'md5', 'salt': 'o1J41zIraDtJPNuhBu7Ifb/q3'},
                           {'alg': 'md5', 'salt': 'U'}, {'alg': 'md5', 'salt': 'RrbZvV0CTu3gaZJ56PVKki4IeP'},
                           {'alg': 'md5', 'salt': 'NNuRbLckJqUp1Do0YlrKCUP'},
                           {'alg': 'md5', 'salt': 'UUwnBbipMTvInA0U0E9'},
                           {'alg': 'md5', 'salt': 'VzGc'}]
        },
        {
            "v": "1.51.2",
            "algorithms": [{'alg': 'md5', 'salt': 'vPjelkvqcWoCsQO1CnkVod8j2GbcE0yEHEwJ3PKSKW'},
                           {'alg': 'md5', 'salt': 'Rw5aO9MHuhY'}, {'alg': 'md5', 'salt': 'Gk111qdZkPw/xgj'},
                           {'alg': 'md5', 'salt': '/aaQ4/f8HNpyzPOtIF3rG/UEENiRRvpIXku3WDWZHuaIq+0EOF'},
                           {'alg': 'md5', 'salt': '6p1gxZhV0CNuKV2QO5vpibkR8IJeFURvqNIKXWOIyv1A'},
                           {'alg': 'md5', 'salt': 'gWR'},
                           {'alg': 'md5', 'salt': 'iPD'}, {'alg': 'md5', 'salt': 'ASEm+P75YfKzQRW6eRDNNTd'},
                           {'alg': 'md5', 'salt': '2fauuwVCxLCpL/FQ/iJ5NpOPb7gRZs0EWJwe/2YNPQr3ore+ZiIri6s/tYayG'}]
        }
    ]
    return version_list[0]
    # return random.choice(version_list)


def random_rtc_token():
    # 生成 8 组 16 进制数，每组 4 位，使用冒号分隔
    ipv6_parts = ["{:04x}".format(random.randint(0, 0xFFFF)) for _ in range(8)]
    ipv6_address = ":".join(ipv6_parts)
    return ipv6_address


class PikPak:
    def __init__(self, invite_code, client_id, device_id, version, algorithms, email, rtc_token,
                 client_secret, package_name):
        # 初始化实例属性
        self.invite_code = invite_code  # 邀请码
        self.client_id = client_id  # 客户端ID
        self.device_id = device_id  # 设备ID
        self.timestamp = 0  # 时间戳
        self.algorithms = algorithms  # 版本盐值
        self.version = version  # 版本
        self.email = email  # 邮箱
        self.rtc_token = rtc_token  # RTC Token
        self.captcha_token = ""  # Captcha Token
        self.client_secret = client_secret  # Client Secret
        self.user_id = ""  # 用户ID
        self.access_token = ""  # 登录令牌
        self.refresh_token = ""  # 刷新令牌
        self.verification_token = ""  # Verification Token
        self.captcha_sign = ""  # Captcha Sign
        self.verification_id = ""  # Verification ID
        self.package_name = package_name  # 客户端包名

        # 代理配置（如果需要）
        self.proxies = {
            "http": "http://127.0.0.1:7899",  # "http://your-proxy-ip:port",
            "https": "http://127.0.0.1:7899",  # "http://your-proxy-ip:port"
        }

    def send_request(self, method, url, headers=None, params=None, json_data=None, data=None, use_proxy=False):
        headers = headers or {}
        proxies = self.proxies if use_proxy else None

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_data,
            data=data,
            proxies=proxies
        )

        print(response.text)
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text

    def gen(self):
        url = "https://user.mypikpak.com/pzzl/gen"
        params = {"deviceid": self.device_id, "traceid": ""}
        headers = {"Host": "user.mypikpak.com", "accept": "application/json, text/plain, */*"}
        return self.send_request("GET", url, headers=headers, params=params)

    def image_verify(self, pid, trace_id, f, n, p, a, c, d):
        url = "https://user.mypikpak.com/pzzl/verify"
        params = {"pid": pid, "deviceid": self.device_id, "traceid": trace_id, "f": f, "n": n, "p": p, "a": a, "c": c,
                  "d": d}
        headers = {"Host": "user.mypikpak.com", "accept": "application/json, text/plain, */*"}
        return self.send_request("GET", url, headers=headers, params=params)

    def executor(self):
        url = "https://api-drive.mypikpak.com/captcha-jsonp/v2/executor?callback=handleJsonpResult_1741687514856"
        headers = {'pragma': 'no-cache'}
        return self.send_request("GET", url, headers=headers)

    def report(self, request_id, sign, pid, trace_id):
        url = "https://user.mypikpak.com/credit/v1/report"
        params = {
            "deviceid": self.device_id,
            "captcha_token": self.captcha_token,
            "request_id": request_id,
            "sign": sign,
            "type": "pzzlSlider",
            "result": 0,
            "data": pid,
            "traceid": trace_id,
            "rtc_token": self.rtc_token
        }
        headers = {'pragma': 'no-cache', 'priority': 'u=1, i'}
        response = self.send_request("GET", url, params=params, headers=headers)
        self.captcha_token = response.get('captcha_token')

    def verification(self):
        url = 'https://user.mypikpak.com/v1/auth/verification'
        params = {"email": self.email, "target": "ANY", "usage": "REGISTER", "locale": "zh-CN",
                  "client_id": self.client_id}
        headers = {'host': 'user.mypikpak.com', 'x-captcha-token': self.captcha_token, 'x-device-id': self.device_id,
                   "x-client-id": self.client_id}
        response = self.send_request("POST", url, headers=headers, data=params)
        self.verification_id = response.get('verification_id')

    def verify_post(self, verification_code):
        url = "https://user.mypikpak.com/v1/auth/verification/verify"
        params = {"client_id": self.client_id}
        payload = {"client_id": self.client_id, "verification_id": self.verification_id,
                   "verification_code": verification_code}
        headers = {"X-Device-Id": self.device_id}
        response = self.send_request("POST", url, headers=headers, json_data=payload, params=params)
        self.verification_token = response.get('verification_token')

    def init(self, action):
        self.refresh_captcha_sign()
        url = "https://user.mypikpak.com/v1/shield/captcha/init"
        params = {"client_id": self.client_id}
        payload = {
            "action": action,
            "captcha_token": self.captcha_token,
            "client_id": self.client_id,
            "device_id": self.device_id,
            "meta": {
                "captcha_sign": "1." + self.captcha_sign,
                "user_id": self.user_id,
                "package_name": self.package_name,
                "client_version": self.version,
                "email": self.email,
                "timestamp": self.timestamp
            }
        }
        headers = {"x-device-id": self.device_id}
        response = self.send_request("POST", url, headers=headers, json_data=payload, params=params)
        self.captcha_token = response.get('captcha_token')
        return response

    def signup(self, name, password, verification_code):
        url = "https://user.mypikpak.com/v1/auth/signup"
        params = {"client_id": self.client_id}
        payload = {
            "captcha_token": self.captcha_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "email": self.email,
            "name": name,
            "password": password,
            "verification_code": verification_code,
            "verification_token": self.verification_token
        }
        headers = {"X-Device-Id": self.device_id}
        response = self.send_request("POST", url, headers=headers, json_data=payload, params=params)
        self.access_token = response.get('access_token')
        self.refresh_token = response.get('refresh_token')
        self.user_id = response.get('sub')

    def activation_code(self):
        url = "https://api-drive.mypikpak.com/vip/v1/order/activation-code"
        payload = {"activation_code": self.invite_code, "data": {}}
        headers = {
            "Host": "api-drive.mypikpak.com",
            "authorization": "Bearer " + self.access_token,
            "x-captcha-token": self.captcha_token,
            "x-device-id": self.device_id,
            'x-system-language': "ko",
            'content-type': 'application/json'
        }
        return self.send_request("POST", url, headers=headers, json_data=payload)

    def files_task(self, task_link):
        url = "https://api-drive.mypikpak.com/drive/v1/files"
        payload = {
            "kind": "drive#file",
            "folder_type": "DOWNLOAD",
            "upload_type": "UPLOAD_TYPE_URL",
            "url": {"url": task_link},
            "params": {"with_thumbnail": "true", "from": "manual"}
        }
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "x-device-id": self.device_id,
            "x-captcha-token": self.captcha_token,
            "Content-Type": "application/json"
        }
        return self.send_request("POST", url, headers=headers, json_data=payload)

    def refresh_captcha_sign(self):
        self.timestamp = str(int(time.time()) * 1000)
        encrypt_string = self.client_id + self.version + self.package_name + self.device_id + self.timestamp
        self.captcha_sign = captcha_sign_encrypt(encrypt_string, self.algorithms)


def save_account_info(name, account_info):
    with open("./account/" + name + ".json", "w", encoding="utf-8") as f:
        json.dump(account_info, f, ensure_ascii=False, indent=4)


class TempEmailService:
    def __init__(self):
        self.page = None
        self.setup_browser()
        
    def setup_browser(self):
        """Set up the browser"""
        try:
            print(f"{Fore.CYAN}ℹ️ Starting browser...{Style.RESET_ALL}")
            
            # Create browser options
            co = ChromiumOptions()
            co.set_argument("--headless=new")
            
            if sys.platform == "linux":
                co.set_argument("--no-sandbox")
                co.set_argument("--disable-dev-shm-usage")
                co.set_argument("--disable-gpu")
            
            co.auto_port()
            
            self.page = ChromiumPage(co)
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Browser start failed: {str(e)}{Style.RESET_ALL}")
            return False
            
    def create_email(self):
        """Create temporary email"""
        try:
            print(f"{Fore.CYAN}ℹ️ Accessing smailpro.com...{Style.RESET_ALL}")
            
            self.page.get("https://smailpro.com/")
            time.sleep(2)
            
            create_button = self.page.ele('xpath://button[@title="Create temporary email"]')
            if create_button:
                create_button.click()
                time.sleep(1)
                
                modal_create_button = self.page.ele('xpath://button[contains(text(), "Create")]')
                if modal_create_button:
                    modal_create_button.click()
                    time.sleep(2)
                    
                    email_div = self.page.ele('xpath://div[@class="text-base sm:text-lg md:text-xl text-gray-700"]')
                    if email_div:
                        email = email_div.text.strip()
                        if '@' in email:
                            print(f"{Fore.GREEN}✅ Email created successfully: {email}{Style.RESET_ALL}")
                            return email
                            
            print(f"{Fore.RED}❌ Email creation failed{Style.RESET_ALL}")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error creating email: {str(e)}{Style.RESET_ALL}")
            return None

    def wait_for_verification_code(self, max_attempts=30, delay=5):
        """Wait for and get verification code from PikPak"""
        print(f"{Fore.CYAN}ℹ️ Waiting for verification email from PikPak...{Style.RESET_ALL}")
        
        for attempt in range(max_attempts):
            try:
                # Click refresh button
                refresh_button = self.page.ele('xpath://button[@id="refresh"]')
                if refresh_button:
                    refresh_button.click()
                time.sleep(2)
                
                # Find email from PikPak
                email_items = self.page.eles('xpath://div[contains(@class, "cursor-pointer")]')
                
                # Print number of emails found for debugging
                print(f"Found {len(email_items)} emails")
                
                for i, item in enumerate(email_items):
                    text_content = item.text
                    print(f"Email {i+1}: {text_content}")
                    
                    if "noreply@accounts.mypikpak.com" in text_content:
                        print(f"Found email from PikPak, opening...")
                        item.click()
                        time.sleep(3)  # Increase wait time for email content to load
                        
                        # Method 1: Get code from iframe srcdoc
                        try:
                            iframe = self.page.ele('xpath://iframe')
                            if iframe:
                                srcdoc = iframe.attr('srcdoc')
                                if srcdoc:
                                    import re
                                    # Find 6-digit code in srcdoc
                                    matches = re.findall(r'<h2>(\d{6})</h2>', srcdoc)
                                    if matches:
                                        code = matches[0]
                                        print(f"{Fore.GREEN}✅ Found verification code from srcdoc: {code}{Style.RESET_ALL}")
                                        return code
                        except Exception as e:
                            print(f"Error extracting from srcdoc: {str(e)}")
                        
                        # Method 2: Use JavaScript to access iframe and get text
                        try:
                            iframe_content = self.page.run_js('''
                                var iframe = document.querySelector('iframe');
                                if (iframe && iframe.contentDocument) {
                                    return iframe.contentDocument.body.innerText;
                                }
                                return '';
                            ''')
                            if iframe_content:
                                import re
                                matches = re.findall(r'\b\d{6}\b', iframe_content)
                                if matches:
                                    code = matches[0]
                                    print(f"{Fore.GREEN}✅ Found verification code from iframe: {code}{Style.RESET_ALL}")
                                    return code
                        except Exception as e:
                            print(f"Error accessing iframe: {str(e)}")
                        
                        # Method 3: Find code directly in page content
                        try:
                            page_content = self.page.run_js('return document.body.innerText')
                            if page_content:
                                import re
                                matches = re.findall(r'\b\d{6}\b', page_content)
                                if matches:
                                    code = matches[0]
                                    print(f"{Fore.GREEN}✅ Found verification code from page content: {code}{Style.RESET_ALL}")
                                    return code
                        except Exception as e:
                            print(f"Error getting page content: {str(e)}")
                
                print(f"Waiting for email... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(delay)
                
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Error checking email: {str(e)}{Style.RESET_ALL}")
                time.sleep(delay)
                continue
        
        print(f"{Fore.RED}❌ Verification code not received after many attempts{Style.RESET_ALL}")
        return None

    def close(self):
        """Close the browser"""
        if self.page:
            self.page.quit()


# Main function
def main():
    try:
        # Ask user for the number of accounts to create
        try:
            num_accounts = int(input(f"{Fore.CYAN}Enter the number of accounts to create: {Style.RESET_ALL}"))
            if num_accounts <= 0:
                print(f"{Fore.RED}Number of accounts must be greater than 0. Setting to default of 1.{Style.RESET_ALL}")
                num_accounts = 1
        except ValueError:
            print(f"{Fore.RED}Invalid input. Setting to default of 1.{Style.RESET_ALL}")
            num_accounts = 1
        
        # Enter invitation code
        invite_code = input(f"{Fore.CYAN}Enter your invitation code (default: 123123123): {Style.RESET_ALL}")
        if not invite_code:
            invite_code = "123123123"
            
        # Create a list to store created accounts
        created_accounts = []
        
        # Loop to create accounts
        for i in range(num_accounts):
            print(f"\n{Fore.YELLOW}=== Creating account {i+1}/{num_accounts} ==={Style.RESET_ALL}\n")
            
            # Initialize parameters
            current_version = ramdom_version()
            version = current_version['v']
            algorithms = current_version['algorithms']
            client_id = "YNxT9w7GMdWvEOKa"
            client_secret = "dbw2OtmVEeuUvIptb1Coyg"
            package_name = "com.pikcloud.pikpak"
            device_id = str(uuid.uuid4()).replace("-", "")
            rtc_token = random_rtc_token()
            print(f"Current version: {version} Device ID: {device_id} Token: {rtc_token}")
            
            # Initialize temp email service
            email_service = TempEmailService()
            try:
                # Create temporary email
                email = email_service.create_email()
                if not email:
                    print(f"{Fore.RED}❌ Could not create temporary email, skipping this account{Style.RESET_ALL}")
                    continue
                    
                # Initialize PikPak
                pikpak = PikPak(invite_code, client_id, device_id, version, algorithms, email, rtc_token, client_secret, package_name)
                
                # Continue registration process
                pikpak.init("POST:/v1/auth/verification")
                
                # Captcha verification
                captcha_attempts = 0
                captcha_success = False
                while captcha_attempts < 3:  # Limit captcha attempts
                    captcha_attempts += 1
                    try:
                        captcha_result = captcha_image_parse(pikpak, device_id)
                        if captcha_result['response_data']['result'] == 'accept':
                            captcha_success = True
                            break
                        else:
                            print(f'Slider verification failed, retrying ({captcha_attempts}/3)...')
                    except Exception as e:
                        print(f"{Fore.RED}Error during captcha verification: {str(e)}{Style.RESET_ALL}")
                
                if not captcha_success:
                    print(f"{Fore.RED}❌ Could not pass captcha after 3 attempts, skipping this account{Style.RESET_ALL}")
                    continue
                
                # Continue process
                executor_info = pikpak.executor()
                sign_encrypt_info = sign_encrypt(executor_info, pikpak.captcha_token, rtc_token)
                pikpak.report(sign_encrypt_info['request_id'], sign_encrypt_info['sign'], captcha_result['pid'], captcha_result['traceid'])
                pikpak.verification()
                
                # Wait and get verification code
                verification_code = email_service.wait_for_verification_code()
                if not verification_code:
                    print(f"{Fore.RED}❌ Could not get verification code, skipping this account{Style.RESET_ALL}")
                    continue
                    
                # Finalize registration
                pikpak.verify_post(verification_code)
                pikpak.init("POST:/v1/auth/signup")
                
                name = email.split("@")[0]
                password = "default123"
                pikpak.signup(name, password, verification_code)
                pikpak.activation_code()
                
                # Save account info
                account_info = {
                    "version": pikpak.version,
                    "device_id": pikpak.device_id,
                    "email": pikpak.email,
                    "captcha_token": pikpak.captcha_token,
                    "access_token": pikpak.access_token,
                    "refresh_token": pikpak.refresh_token,
                    "user_id": pikpak.user_id,
                    "timestamp": pikpak.timestamp,
                    "password": password,
                    "name": name
                }
                
                # Add to created accounts list
                created_accounts.append(account_info)
                
                print(f"{Fore.GREEN}✅ Account created successfully!{Style.RESET_ALL}")
                print("Account information: ", json.dumps(account_info, indent=4, ensure_ascii=False))
                
                try:
                    if not os.path.exists('./account'):
                        os.makedirs('./account')
                    save_account_info(name, account_info)
                    print(f"Account information saved to ./account/{name}.json")
                except Exception as e:
                    print(f"Could not save account information: {e}")
                
            finally:
                email_service.close()
                time.sleep(5)
                
        # Show summary
        print(f"\n{Fore.GREEN}=== Summary ==={Style.RESET_ALL}")
        print(f"Successfully created {len(created_accounts)}/{num_accounts} accounts.")
        if created_accounts:
            print("List of created emails:")
            for idx, account in enumerate(created_accounts):
                print(f"{idx+1}. {account['email']} - Password: {account['password']}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program stopped by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Unhandled error: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    print("Developer's statement: Free to use, please credit the source when sharing. This tool is only for educational and technical analysis purposes.")
    main()
