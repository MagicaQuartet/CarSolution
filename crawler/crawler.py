import os
import time
import requests
from selenium import webdriver


class CarCrawler(object):
    def __init__(self):
        self._baseURL = "http://www.리얼카.com"
        self._cwd = os.getcwd()
        self._driver = None

        self.maker = 0

    def save_text(self, elems):
        for li in elems:
            print(li.text)

    def save_img(self):
        for cnt in range(20):
            post = self._driver.find_element_by_id("listcar").find_elements_by_tag_name("img")[cnt]
            time.sleep(3)
            post.click()
            time.sleep(3)

            try:
                images = self._driver.find_element_by_id("detailpic").find_elements_by_tag_name("img")
            except IndexError:
                break

            try:
                if not (os.path.isdir(self._cwd+"/images/"+str(self.maker)+"/"+str(cnt))):
                    os.makedirs(self._cwd+"/images/"+str(self.maker)+"/"+str(cnt))
            except OSError as e:
                print("Failed to create directory!!!!!")

            for img in images:
                image_url = img.get_property("src")
                image = requests.get(image_url).content
                filename = self._cwd+"/images/"+str(self.maker)+"/"+str(cnt)+"/"+os.path.basename(image_url)
                with open(filename, 'wb') as f:
                    f.write(image)

            self._driver.execute_script("window.history.go(-1)")
            time.sleep(3)

    def crawl(self):
        if self.maker == -1:
            print("Choose car maker!")
            return

        self._driver = webdriver.Firefox(executable_path="C:/Users/m2ucr/PycharmProjects/CarSolution/driver/geckodriver.exe")
        self._driver.get(self._baseURL)
        time.sleep(1)
        self._driver.find_element_by_name("image1").click()     # 국산차
        time.sleep(1)
        self._driver.find_element_by_id("car1_"+str(self.maker)).click()
        time.sleep(1)
        self._driver.find_element_by_id("carselectbox").find_elements_by_tag_name("input")[1].click()
        time.sleep(1)
        listcar = self._driver.find_element_by_id("listcar")

        listcar_text = listcar.find_elements_by_tag_name("li")[::3]

        self.save_text(listcar_text)
        self.save_img()

        self._driver.close()

    def set_maker(self, maker):
        self.maker = maker
