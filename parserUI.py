import requests
import webbrowser
import keyboard
from pymsgbox import *
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
app = QtWidgets.QApplication([])
ui = uic.loadUi("design2.ui")
ui.setWindowTitle("Парсер")
URL = 'https://www.google.com/search?q=Бетон'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://www.google.com/search?q=Бетон'
global cars
global debugMode

debugMode = False
cars = []
ui.tableWidget.setColumnCount(2)     # Устанавливаем три колонки
def getRows():
    
    try:
        RowItems = prompt(text='Введите кол-во результатов (максимум 82)', title='Настройка')
        RowItems = int(RowItems)
        return RowItems
    except Exception as e:
        if debugMode:
            
            print(e)
        getRows()
ui.tableWidget.setRowCount(getRows())

#Widget УстWidgetанавливаем заголовки таблицы
ui.tableWidget.setHorizontalHeaderLabels(["Текст", "Ссылка"])

#Widget УстWidgetанавливаем всплывающие подсказки на заголовки


#Widget УстWidgetанавливаем выравнивание на заголовки
ui.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
ui.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)


#Widget запWidgetолняем первую строку
# ui.tableWidget.setItem(0, 0, QTableWidgetItem("Text in column 1"))
# ui.tableWidget.setItem(0, 1, QTableWidgetItem("Text in column 2"))
# ui.tableWidget.setItem(0, 2, QTableWidgetItem("Text in column 3"))

#Widget делWidgetаем ресайз колонок по содержимому

def get_html(url, page, params=None):
    URL = 'https://www.google.com/search?q={0}&start=0{1}'.format(url,page)
    r = requests.get(URL, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='yuRUbf')

    
    for item in items:
        title = item.find('h3', class_='LC20lb DKV0Md').get_text()
        link = item.find('a', href=True)['href']
        cars.append({
            'title': title,
            'link': link
        })
        
    return cars


def parse(search):
    
    for i in range(0,9):
        html = get_html(search, page=i)
        if html.status_code == 200:
            cars = get_content(html.text)
            if debugMode:
                print(cars)

        else:
            if debugMode:
                print('Error')
def search():
    text = ui.lineEdit.text()
    if debugMode:
        print(text)
    parse(text)
    for a in range(len(cars)):
        i = cars[a]
        title = i['title']
        link = i['link']
        ui.tableWidget.setItem(a, 0, QTableWidgetItem(title))
        ui.tableWidget.setItem(a, 1, QTableWidgetItem(link))
    b = confirm(text='Хотите открыть результаты в браузере', title='Просмотр результатов', buttons=['Да', 'Нет'])
    if b == 'Да':
        count = int(prompt(text='Сколько результатов вы хотите просмотреть?', title='Просмотр результатов'))
        count = count - 1
        for i in range(count):
            a = cars[i]
            url = a['link']
            if debugMode:
                print(url)
            webbrowser.open_new_tab(url)
            keyboard.wait('n')


ui.tableWidget.resizeColumnsToContents()
ui.pushButton.clicked.connect(search)
ui.show()
app.exec()

