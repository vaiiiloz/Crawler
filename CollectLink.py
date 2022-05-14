import time
from pygments import highlight
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from sympy import ImageSet
from webdriver_manager.chrome import ChromeDriverManager
import os.path as osp

class ChromeCrawler:
    def __init__(self, no_gui=False, proxy=None):
        executable = None
        #chose driver
        if platform.system() == 'Windows':
            print("Detected OS : Windows")
            executable = './chromedriver/chromedriver_win.exe'
        elif platform.system() == 'Linux':
            print("Detect OS : Linux")
            executable = './chromedriver/chromedriver_linux'
        elif platform.system() == "Darwin":
            print("Detected OS : Mac")
            executable = './chromedirver/chromedirver_mac'
        else:
            raise OSError("Unknow OS Type")

        if not osp.exists(executable):
            raise FileNotFoundError(f"Chromedriver file should be placed at {executable}")
        
        #Chrome config
        chrome_option = Options()
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--disable-dev-shm-usage')
        chrome_option.add_argument('--headless')
        if no_gui:
            chrome_option.add_argument('--headless')
        if proxy:
            chrome_option.add_argument("--proxy-server={}".format(proxy))

        #Install browser
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_option)

        #print config browser
        browser_version = 'Failed to detect version'
        chromedriver_version = 'Failed to detect version'
        major_version_different = False

        if 'browserVersion' in self.browser.capabilities:
            browser_version = str(self.browser.capabilities['browserVersion'])

        if 'chrome' in self.browser.capabilities:
            if 'chromedriverVersion' in self.browser.capabilities['chrome']:
                chromedriver_version = str(self.browser.capabilities['chrome']['chromedriverVersion'])

        if browser_version.split('.')[0] != chromedriver_version.split('.')[0]:
            major_version_different = True      

        print('__________________________')
        print(f'Current web-browser version:\t{browser_version}')
        print(f'Current chrome-driver version:\t{chromedriver_version}')
        if major_version_different:
            print('Warning: Version different')
            print('http://chromedriver.chromium.org/downloads')
            
    def translate(self, language, keyword):
        if language == 'en':
            return keyword
        
        self.browser.get(f'https://translate.google.com/?sl=en&tl={language}&text={keyword}&op=translate')
        text = self.browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[8]/div/div[1]/span[1]/span/span')
        return text.text

    def get_scroll(self):
        pos = self.browser.execute_script("return window.pageYOffset;")
        return pos

    def click(self, xpath):
        w = WebDriverWait(self.browser, 15)
        elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
        
    def wait_and_click(self, xpath):
        try:
            w = WebDriverWait(self.browser, 15)
            elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elem.click()
        except:#repeat click until done
            print(f'Clieck time out -{xpath}')
            print('Refreshing borwser ...')
            self.browser.refresh()
            time.sleep(2)
            return self.wait_and_click(xpath)
        return elem

    def click_and_retrieve(self, img):
        src = None
        try:
            self.wait_and_click(img)
            src = self.browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')

        except:
            print("__HTTPError____")
            src = None
        
        return src
        
    def highlight(self, element):
        return
        # self.browser.execute_script("arguemnts[0].setAttribute('style'm arguments[1]);", element, "background: yellow; border: 2px solid red;")

    @staticmethod
    def remove_duplicates(_list):
        return list(dict.fromkeys(_list))

    def google(self, keyword, add_url="", num_page = 1):
        #get into page
        self.browser.get("https://www.google.com/search?q={}&source=lnms&tbm=isch{}".format(keyword, add_url))

        time.sleep(1)

        print('Scrolling down')

        elem = self.browser.find_element_by_tag_name("body")
        
        page = 0
        while True:
            for i in range(60):
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
            try:
                self.click('//input[@type="button"]')
            except:
                break
            page+=1
            if page>num_page:
                break
        
        elem.send_keys(Keys.HOME)
        

        self.click('//div[@data-ri="0"]')
        time.sleep(1)

        links = []

        last_scroll = 0
        scroll_patience = 0

        while True:
            try:
                xpath = '//div[@id="islsp"]//div[@class="v4dQwb"]'
                div_box = self.browser.find_element(By.XPATH, xpath)
               

                xpath = '//img[@class="n3VNCb"]'
                img = div_box.find_element(By.XPATH, xpath)
                

                xpath = '//div[@class="k7O2sd"]'
                loading_bar = div_box.find_element(By.XPATH, xpath)
                #Wait for image to load
                while str(loading_bar.get_attribute('style')) != 'display: none;':
                    time.sleep(0.2)
                
                src = img.get_attribute('src')

                if src is not None and not src.startswith('data:image'):
                    links.append(src)
            except StaleElementReferenceException:
                pass
            except Exception as e:
                print('[Exception occurred while collecting links from google_full] {}'.format(e))

            scroll = self.get_scroll()


            if scroll == last_scroll:
                scroll_patience += 1
            else:
                scroll_patience = 0
                last_scroll = scroll

            if scroll_patience >= 100:
                break

            elem.send_keys(Keys.RIGHT)


        
        #remove duplicates
        links = self.remove_duplicates(links)
        # self.browser.close()
        return links

    def naver(self, keyword, add_url="", scroll_time = 60):
        #get into page
        self.browser.get("https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}{}".format(keyword, add_url))

        time.sleep(1)

        print('Scrolling down')

        elem = self.browser.find_element_by_tag_name("body")

        self.wait_and_click('//div[@class="photo_bx api_ani_send _photoBox"]')
        time.sleep(1)


        
        #get list of images' div
        images = self.browser.find_elements(By.XPATH, '//div[@class="photo_bx api_ani_send _photoBox"]//img[@class="_image _listImage"]')

        print('Scraping links')

        links = []


        #get source of all imgs
        last_scroll = 0
        scroll_patience = 0

        while True:
            try:
                xpath = '//div[@class="image _imageBox"]//img[@class="_image"]'
                imgs = self.browser.find_elements(By.XPATH, xpath)
                
                for img in imgs:
                    self.highlight(img)
                    src = img.get_attribute('src')

                    if src is not None:
                        links.append(src)
            except StaleElementReferenceException:
                pass
            except Exception as e:
                print('[Exception occurred while collecting links from google_full] {}'.format(e))

            scroll = self.get_scroll()


            if scroll == last_scroll:
                scroll_patience += 1
            else:
                scroll_patience = 0
                last_scroll = scroll

            if scroll_patience >= 100:
                break

            elem.send_keys(Keys.RIGHT)
            elem.send_keys(Keys.PAGE_DOWN)


        
        #remove duplicates
        links = self.remove_duplicates(links)
        # self.browser.close()
        return links

    def baidu(self, keyword, num_scroll=100):
        self.browser.get(f"https://image.baidu.com/search/index?tn=baiduimage&word=${keyword}")

        elem = self.browser.find_element_by_tag_name("body")
        for i in range(num_scroll):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        links = []

        pages = self.browser.find_elements_by_xpath('//div[@id="imgid"]//div[@class="imgpage"]')
        for page in pages:
            lis = page.find_elements_by_tag_name('li')
            
            for li in lis:
                if li.get_attribute('class') == 'newfcImgli':
                    src = li.find_element_by_tag_name('img').get_attribute('src')
                else:
                    src = li.get_attribute('data-objurl')
                if src is not None:
                    links.append(src)
            
            # if link is not None:
            #     links.append(link)
        # self.browser.close()
        return links

