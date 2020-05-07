import requests
from bs4 import BeautifulSoup
import common.utils.ExceptionUtil as exutil
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
import pymysql

class HtmlScrapper:
    def __init__(self):
        super().__init__()

    def scrap(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = None
            img_url = None
            body = None
            for tag in soup.find_all("meta"):
                if tag.get("property", None) == "og:title":
                    title = tag.get("content", None)
                elif tag.get("property", None) == "og:image":
                    img_url = tag.get("content", None)
                elif tag.get("property", None) == "og:description":
                    body = tag.get("content", None)
            if title == None: title = soup.title
            if img_url == None: img_url = self.getConditionalImage(url, soup)
            if img_url == None: img_url = self.getFirstImage(url, soup)
            if body == None: body = self.getBodyText(soup)
            title = pymysql.escape_string(title)
            body = pymysql.escape_string(body)
            if len(body) > 100:
                body = body[:100]
            img_url = pymysql.escape_string(img_url)
            return self.__extractTitle(title), body, img_url
        except Exception as ex:
            exutil.printException()

    def __extractTitle(self, title):
        if '-' in title:
            title = title.split('-', -1)
        elif '|' in title:
            title = title.split('|', -1)
        elif ':' in title:
            title = title.split(':', -1)
        if len(title) > 1:
            return title[0], title[1]
        return title, ''

    def getConditionalImage(self, url, soup):
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            if self.findConditionalImage(img, 80) == True:
                img_url = img.attrs.get("src")
                img_url = urljoin(url, img_url)
                pos = img_url.index("?")
                if pos > 0:
                    img_url = img_url[:pos]
                return img_url

    def getFirstImage(self, url, soup):
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            if self.isLogo(img) == False:
                img_url = img.attrs.get("src")
                img_url = urljoin(url, img_url)
                pos = img_url.index("?")
                if pos > 0:
                    img_url = img_url[:pos]
                return img_url

    def findConditionalImage(self, img, size):
        width = img.attrs.get('weight', None)
        height = img.attrs.get('height', None)
        if  width != None and height != None:
            width = ''.join(filter(str.isdigit, width))
            height = ''.join(filter(str.isdigit, height))

            if width > size and height > size and self.isLogo(img) == False:
                return True
        return False

    def isLogo(self, img):
        img_url = img.attrs.get("src")
        if 'logo' in img_url or 'snb_' in img_url:
            return True
        className = img.attrs.get('class')
        if 'logo' in className or 'snb_' in className:
            return True
        return False

    def getBodyText(self, soup):
        plist = soup.find('body').find('p')
        if len(plist) > 0:
            return plist[0].text
        return soup.body.text
