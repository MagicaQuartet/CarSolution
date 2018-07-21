import os
import time
import requests
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class CarCrawler(object):
    def __init__(self):
        self._baseURL = "http://www.리얼카.com/main.php?m=sale&s=list&dealer=&recommend=&p=%d&seq=&psub=&part=&car_intro=&car_tou=&carnation=%d&carinfo1=%s&carseries=&carinfo2=&carinfo3=&carinfo4=&ord_chk=6&listtype=img&caryear1=0&caryear2=0&oil_type=&cartype=&carmoney1=%s&carmoney2=%s&carauto=&carcolor=&carkm1=&carkm2=&lpguse=&keyword="
        self._cwd = os.getcwd()
        self._driver = None
        self.startpage = 1
        self.endpage = 1
        self.carnation = 1
        self.maker = ""
        self.carmoney1 = ""
        self.carmoney2 = ""
        self.cnt = 0

    def parse_info(self, infohead, carinfo, cnt):
        dic = dict()
        dic["이름"] = infohead.find_element_by_id("carname").text
        dic["가격"] = infohead.find_element_by_id("carprice").text+"만원"

        lhs = carinfo.find_elements_by_class_name("infoleft")
        rhs = carinfo.find_elements_by_class_name("inforight")

        for i in range(len(lhs)):
            dic[lhs[i].text] = rhs[i].text

        with open(self._cwd+"/data/"+str(self.maker)+"/"+str(cnt)+'/info.json', 'w', encoding='utf8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)

    def save_info(self):
        for i in range(20):
            post = self._driver.find_element_by_id("listcar").find_elements_by_tag_name("img")[i]
            post.click()
            time.sleep(2)

            infohead = self._driver.find_element_by_id("infohead")
            carinfo = self._driver.find_element_by_id("carinfo").find_element_by_tag_name("tbody")
            images = self._driver.find_element_by_id("detailpic").find_elements_by_tag_name("img")

            try:
                if not (os.path.isdir(self._cwd+"/data/"+str(self.maker)+"/"+str(self.cnt))):
                    os.makedirs(self._cwd+"/data/"+str(self.maker)+"/"+str(self.cnt))
            except OSError as e:
                print("Failed to create directory!!!!!")
                break

            self.parse_info(infohead, carinfo, self.cnt)

            for img in images:
                image_url = img.get_property("src")
                image = requests.get(image_url).content
                filename = self._cwd+"/data/"+str(self.maker)+"/"+str(self.cnt)+"/"+os.path.basename(image_url)
                with open(filename, 'wb') as f:
                    f.write(image)

            self._driver.execute_script("window.history.go(-1)")
            time.sleep(2)

            self.cnt += 1

    def crawl(self):
        self._driver = webdriver.Firefox(executable_path="C:/Users/m2ucr/PycharmProjects/CarSolution/driver/geckodriver.exe")
        for i in range(self.startpage, self.endpage+1):
            self._driver.get(self._baseURL % (i, self.carnation, self.maker, self.carmoney1, self.carmoney2))
            time.sleep(2)
            try:
                self.save_info()
            except NoSuchElementException:
                break
            except IndexError:
                break
        self._driver.close()
