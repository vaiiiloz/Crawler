from unicodedata import name
import pandas
import os
import requests
from tqdm import tqdm
import shutil
import argparse
from CollectLink import ChromeCrawler


def make_dir(keyword):
    
    current_path = os.getcwd()
    path = os.path.join(current_path, keyword)
    if not os.path.exists(path):
        os.mkdir(path)
        return 0
    else:
        return len([name for name in os.listdir(path) if os.path.isfile(name)])

def download(filename, link):
    try:
        response = requests.get(link, stream=True)
    except:
        return
    file_size = int(response.headers.get('content-length', 0))
    
    progress = tqdm(response.iter_content(chunk_size=1024), f"Downloading {filename}", total=file_size, unit='B', unit_scale=True, unit_divisor=1024)
    print(f"Download file {filename}")
    with open(filename, 'wb') as f:
        # shutil.copyfileobj(response.raw, f)
        for data in progress:
            f.write(data)
            progress.update(len(data))
            
def search(keyword, data):
    keys = keyword.split(" ")[1:-1]
    key = ''
    for i in keys:
        key+=i
    folder = os.path.join('data', key)
    #create folder if not exist
    n=make_dir(folder)
    #translate english to data['language]
    trans = crawler.translate(data['language'], keyword)
    #collect links
    links = data['search_engine'](trans)
    
    #download images
    for idx, link in enumerate(links):
        filename = "{}.png".format(str(n+idx))
        download(os.path.join(folder, filename), link)
    
    
if __name__ == "__main__":
    #argparse
    parse = argparse.ArgumentParser()
    parse.add_argument('--google', type=str, default='true', help='Use google search')
    parse.add_argument('--naver', type=str, default='true', help='Use naver search')
    parse.add_argument('--baidu', type=str, default='true', help='Use baidu search')
    args = parse.parse_args()
    
    _google = args.google.lower() == 'true'
    _naver = args.naver.lower() == 'true'
    _baidu = args.baidu.lower() == 'true'
    
    
        
    # Main object
    df = pandas.read_csv('./keywords.csv')
    crawler = ChromeCrawler()
    
    #config search engine and language
    data={'language': None, 'search_engine': None}
    if _google:
        data = {'language': 'en', 'search_engine': crawler.google}
    elif _naver:
        data = {'language': 'ko', 'search_engine': crawler.naver}
    elif _baidu:
        data = {'language': 'zh-CN', 'search_engine': crawler.baidu}
    
    #search for each keyword
    for keyword in df['keyword']:
        search(keyword, data)
    crawler.browser.close()
        
    
    
    