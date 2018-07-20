import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from crawler.crawler import CarCrawler


class QCrawler(CarCrawler, QThread):
    def __init__(self):
        CarCrawler.__init__(self)
        QThread.__init__(self)

    def run(self):
        self.crawl()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crawler = QCrawler()

        self.setWindowTitle("CarSolution")
        self.setGeometry(700, 100, 800, 600)

        self.comboMakerLabel = QLabel("제조사: ", self)
        self.comboMakerLabel.move(10, 20)
        self.comboMaker = QComboBox(self)
        self.set_combo_maker()

        self.btnCrawl = QPushButton("Crawl", self)
        self.btnCrawl.move(200, 20)
        self.btnCrawl.clicked.connect(self.crawler.start)

        self.comboPriceLabel = QLabel("판매가격: ", self)
        self.comboPriceLabel.move(5, 60)
        self.comboPrice1 = QComboBox(self)
        self.comboPrice1.move(70, 60)
        self.comboPrice2 = QComboBox(self)
        self.comboPrice2.move(200, 60)
        self.comboPrice1.addItem("이상")
        self.comboPrice2.addItem("이하")
        self.set_combo_price(self.comboPrice1)
        self.set_combo_price(self.comboPrice2)
        self.comboPrice1.currentIndexChanged.connect(self.combo_price1_select)
        self.comboPrice2.currentIndexChanged.connect(self.combo_price2_select)

        self.lineEditPageLabel = QLabel("검색 페이지: ", self)
        self.lineEditPageLabel.move(0, 100)
        self.lineEditStartPage = QLineEdit("1", self)
        self.lineEditStartPage.move(70, 100)
        self.lineEditEndPage = QLineEdit("1", self)
        self.lineEditEndPage.move(200, 100)
        self.lineEditStartPage.textEdited.connect(self.lineedit_start_select)
        self.lineEditEndPage.textEdited.connect(self.lineedit_end_select)

    def set_combo_maker(self):
        self.comboMaker.addItem("현대")
        self.comboMaker.addItem("기아")
        self.comboMaker.addItem("대우")
        self.comboMaker.addItem("삼성")
        self.comboMaker.addItem("쌍용")
        self.comboMaker.addItem("제네시스")
        self.comboMaker.addItem("쉐보레")
        self.comboMaker.addItem("중대형버스")
        self.comboMaker.addItem("중대형화물")
        self.comboMaker.addItem("기타제조사")
        self.comboMaker.move(70, 20)
        self.comboMaker.currentIndexChanged.connect(self.combo_maker_select)

    def set_combo_price(self, comboBox):
        for i in range(1, 21):
            comboBox.addItem(str(i)+"00만원")
        comboBox.addItem("2500만원")
        comboBox.addItem("3000만원")
        comboBox.addItem("3500만원")
        for i in range(4, 11):
            comboBox.addItem(str(i)+"000만원")

    @pyqtSlot()
    def combo_maker_select(self):
        self.crawler.maker = self.comboMaker.currentIndex()

    @pyqtSlot()
    def combo_price1_select(self):
        self.crawler.carmoney1 = self.comboPrice1.currentIndex()

    @pyqtSlot()
    def combo_price2_select(self):
        self.crawler.carmoney2 = self.comboPrice2.currentIndex()

    @pyqtSlot()
    def lineedit_start_select(self):
        try:
            if len(self.lineEditStartPage.text()) > 0:
                newpage = int(self.lineEditStartPage.text())
                if newpage > 0:
                    self.crawler.startpage = newpage
                else:
                    self.lineEditStartPage.setText("1")
                    self.crawler.startpage = 1
        except ValueError:
            self.lineEditStartPage.setText("1")
            self.crawler.startpage = 1

    @pyqtSlot()
    def lineedit_end_select(self):
        try:
            if len(self.lineEditEndPage.text()) > 0:
                newpage = int(self.lineEditEndPage.text())
                if newpage > 0:
                    self.crawler.endpage = newpage
                else:
                    self.lineEditEndPage.setText("1")
                    self.crawler.endpage = 1
        except ValueError:
            self.lineEditEndPage.setText("1")
            self.crawler.endpage = 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
