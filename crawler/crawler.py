import os
import time
import requests
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class CarCrawler(object):
    def __init__(self):
        self._baseURL = "http://www.리얼카.com"
        self._cwd = os.getcwd()
        self._driver = None
        self.maker = 0
        self.carmoney1 = 0
        self.carmoney2 = 0
        self.startpage = 1
        self.endpage = 1

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
        for i in range((self.startpage-1) // 10):
            try:
                self._driver.find_element_by_class_name("next").click()
                time.sleep(1)
            except NoSuchElementException:
                return

        try:
            pages = self._driver.find_element_by_class_name("paginate")
            if pages.find_element_by_tag_name("strong").text != ("%s" % self.startpage):
                if self.startpage <= 10:
                    pages.find_elements_by_tag_name("a")[(self.startpage-2) % 10].click()
                else:
                    pages.find_elements_by_tag_name("a")[(self.startpage-1) % 10].click()
                time.sleep(1)
        except NoSuchElementException:
            pass
        except IndexError:
            return

        cnt = 0

        for page in range(self.startpage, self.endpage+1):
            for i in range(20):
                try:
                    post = self._driver.find_element_by_id("listcar").find_elements_by_tag_name("img")[i]
                except IndexError:
                    break
                except NoSuchElementException:
                    break
                time.sleep(1)
                post.click()
                time.sleep(1)

                infohead = self._driver.find_element_by_id("infohead")
                carinfo = self._driver.find_element_by_id("carinfo").find_element_by_tag_name("tbody")
                images = self._driver.find_element_by_id("detailpic").find_elements_by_tag_name("img")

                try:
                    if not (os.path.isdir(self._cwd+"/data/"+str(self.maker)+"/"+str(cnt))):
                        os.makedirs(self._cwd+"/data/"+str(self.maker)+"/"+str(cnt))
                except OSError as e:
                    print("Failed to create directory!!!!!")
                    break

                self.parse_info(infohead, carinfo, cnt)

                for img in images:
                    image_url = img.get_property("src")
                    image = requests.get(image_url).content
                    filename = self._cwd+"/data/"+str(self.maker)+"/"+str(cnt)+"/"+os.path.basename(image_url)
                    with open(filename, 'wb') as f:
                        f.write(image)

                self._driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                cnt += 1

            try:
                if page <= 10:
                    self._driver.find_element_by_class_name("paginate").find_elements_by_tag_name("a")[(page-1) % 10].click()
                else:
                    self._driver.find_element_by_class_name("paginate").find_elements_by_tag_name("a")[(page-1) % 10 + 1].click()
                time.sleep(1)
            except NoSuchElementException:
                return
            except IndexError:
                return

    def crawl(self):
        self._driver = webdriver.Firefox(executable_path="C:/Users/m2ucr/PycharmProjects/CarSolution/driver/geckodriver.exe")
        self._driver.get(self._baseURL)
        time.sleep(1)
        self._driver.find_element_by_name("image1").click()     # 국산차
        time.sleep(1)
        self._driver.find_element_by_id("car1_"+str(self.maker)).click()
        time.sleep(1)
        if self.carmoney1 != 0:
            comboBox = self._driver.find_element_by_name("carmoney1")
            comboBox.click()
            time.sleep(1)
            comboBox.find_elements_by_tag_name("option")[self.carmoney1].click()
            time.sleep(1)
        if self.carmoney2 != 0:
            comboBox = self._driver.find_element_by_name("carmoney2")
            comboBox.click()
            time.sleep(1)
            comboBox.find_elements_by_tag_name("option")[self.carmoney2].click()
            time.sleep(1)
        self._driver.find_element_by_id("carselectbox").find_elements_by_tag_name("input")[1].click()
        time.sleep(1)

        self.save_info()
        self._driver.close()
