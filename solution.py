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
        self.setGeometry(700, 100, 600, 800)

        self.comboMakerLabel = QLabel("제조사: ", self)
        self.comboMakerLabel.move(20, 20)
        self.comboMaker = QComboBox(self)
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

        self.btnCrawl = QPushButton("Crawl", self)
        self.btnCrawl.move(200, 20)
        self.btnCrawl.clicked.connect(self.crawler.start)

    def combo_maker_select(self):
        self.crawler.set_maker(self.comboMaker.currentIndex())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
