import time, sys
from PyQt6.QtCore import (QDateTime, QSize, Qt)

from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSpinBox, QTabWidget, QVBoxLayout, QWidget)
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply
from datetime import datetime, timezone, timedelta 
import requests
from enum import Enum
import json
import webbrowser
from functools import partial

class tags(Enum):
    Nothing = 0
    Sports = 1
    Politics = 2
    Crypto = 21
    Weather = 84
    Technology = 22
    News = 38
    Elections = 144
    Predictions = 41
    Future_Events = 8
    Awards = 18
    Video_Games = 3
    Release_Date = 5
    Person_of_the_year = 17
    Box_Office = 51
    Blockchain = 20
    Esports = 64
    Business = 107
    Time_magazine = 16
    US = 86
    Climate = 87
    Joe_Biden = 15
    Musk = 6
    Zuck = 7
    Football = 10
    Basketball = 28
    Gta_6 = 4
    
    

class ManyDealApp(QWidget):
    def __init__(self):
        super().__init__()
        self.eventManager = QNetworkAccessManager()
        self.eventManager.finished.connect(self.onResponse)
        self.init_ui()
        
    def init_ui(self):
        self.eventsGrid = QGridLayout()
        self.setGeometry(0, 0, 1200, 720)
        mainFrame = QVBoxLayout()
        self.mainBox = QGridLayout()
        self.mainBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.filters = QGroupBox()
        self.filters.setMaximumHeight(160)
        self.filtersLayout = QHBoxLayout(self.filters)
        self.filtersLayout.setContentsMargins(3, 3, 3, 3)
        self.filtersLayout.setSpacing(2)
        #Filter 1
        self.filter1 = QGroupBox(self.filters)
        self.filterLayout1 = QGridLayout(self.filter1)
        self.filterLayout1.setSpacing(0)
        self.filterLayout1.setContentsMargins(3, 0, 3, 0)
        #Ascending
        self.ascend = QLabel("Ascend", self.filter1)
        self.filterLayout1.addWidget(self.ascend, 0, 0, 1, 1)
        
        self.ascendBox = QComboBox(self.filter1)
        self.ascendBox.addItem("None")
        self.ascendBox.addItem("True")
        self.ascendBox.addItem("False")
        self.ascendBox.setEditable(False)
        self.filterLayout1.addWidget(self.ascendBox, 0, 1, 1, 1)
        
        self.ascendBox.setCurrentIndex(2)
        #Active
        self.active = QLabel("Active", self.filter1)
        self.filterLayout1.addWidget(self.active, 1, 0, 1, 1)
        
        self.activeBox = QComboBox(self.filter1)
        self.activeBox.addItem("None")
        self.activeBox.addItem("True")
        self.activeBox.addItem("False")
        self.activeBox.setEditable(False)
        self.filterLayout1.addWidget(self.activeBox, 1, 1, 1, 1)
        
        self.activeBox.setCurrentIndex(1)
        #Closed
        self.closed = QLabel("Closed", self.filter1)
        self.filterLayout1.addWidget(self.closed, 2, 0, 1, 1)
        
        self.closedBox = QComboBox(self.filter1)
        self.closedBox.addItem("None")
        self.closedBox.addItem("True")
        self.closedBox.addItem("False")
        self.closedBox.setEditable(False)
        self.filterLayout1.addWidget(self.closedBox, 2, 1, 1, 1)
        
        self.closedBox.setCurrentIndex(2)
        #Choose your own market
        self.cyom = QLabel("CYOM", self.filter1)
        self.filterLayout1.addWidget(self.cyom, 3, 0, 1, 1)
        
        self.cyomBox = QComboBox(self.filter1)
        self.cyomBox.addItem("None")
        self.cyomBox.addItem("True")
        self.cyomBox.addItem("False")
        self.cyomBox.setEditable(False)
        self.filterLayout1.addWidget(self.cyomBox, 3, 1, 1, 1)
        
        self.cyomBox.setCurrentIndex(0)
        
        self.filtersLayout.addWidget(self.filter1)
        #Filter 2
        self.filter2 = QGroupBox(self.filters)
        self.filterLayout2 = QGridLayout(self.filter2)
        self.filterLayout2.setSpacing(0)
        self.filterLayout2.setContentsMargins(3, 0, 3, 0)
        #Limit
        self.limit = QLabel("Limit", self.filter2)
        self.filterLayout2.addWidget(self.limit, 0, 0, 1, 1)
        
        self.limitBox = QSpinBox(self.filter2)
        self.limitBox.setMaximumSize(QSize(80, 40))
        self.limitBox.setMaximum(999)
        
        self.filterLayout2.addWidget(self.limitBox, 0, 1, 1, 1)
        #Offset
        self.offset = QLabel("Offset", self.filter2)
        self.filterLayout2.addWidget(self.offset, 1, 0, 1, 1)
        
        self.offsetBox = QSpinBox(self.filter2)
        self.offsetBox.setMaximumSize(QSize(80, 40))
        self.offsetBox.setMaximum(99999)
        
        self.filterLayout2.addWidget(self.offsetBox, 1, 1, 1, 1)
        #Tag ID
        self.id = QLabel("ID", self.filter2)
        self.filterLayout2.addWidget(self.id, 2, 0, 1, 1)
        
        self.idBox = QSpinBox(self.filter2)
        self.idBox.setMaximumSize(QSize(80, 40))
        self.idBox.setMaximum(9999999)
        
        self.filterLayout2.addWidget(self.idBox, 2, 1, 1, 1)
        
        self.filtersLayout.addWidget(self.filter2)
        #Filter 3
        self.filter3 = QGroupBox(self.filters)
        self.filterLayout3 = QGridLayout(self.filter3)
        self.filterLayout3.setSpacing(0)
        self.filterLayout3.setContentsMargins(3, 0, 3, 0)
        #Start
        self.startMin = QLabel("Start Date Min", self.filter3)
        self.filterLayout3.addWidget(self.startMin, 0, 0, 1, 1)

        minDateTime = QDateTime.fromString("2020-01-01T01:01:01Z", "yyyy-MM-ddThh:mm:ssZ")
        
        self.startMinBox = QDateTimeEdit(self.filter3)
        self.startMinBox.setMaximumSize(QSize(180, 30))
        self.startMinBox.setCalendarPopup(True)
        self.startMinBox.setDisplayFormat(u"yyyy-MM-ddThh:mm:ssZ")
        self.startMinBox.setMinimumDateTime(minDateTime)
        
        self.filterLayout3.addWidget(self.startMinBox, 0, 1, 1, 1)
        #Max
        self.startMax = QLabel("Start Date Max", self.filter3)
        self.filterLayout3.addWidget(self.startMax, 1, 0, 1, 1)

        self.startMaxBox = QDateTimeEdit(self.filter3)
        self.startMaxBox.setMaximumSize(QSize(180, 30))
        self.startMaxBox.setCalendarPopup(True)
        self.startMaxBox.setDisplayFormat(u"yyyy-MM-ddThh:mm:ssZ")
        self.startMaxBox.setMinimumDateTime(minDateTime)
        self.filterLayout3.addWidget(self.startMaxBox, 1, 1, 1, 1)
        #End
        self.endMin = QLabel("End Date Min", self.filter3)
        self.filterLayout3.addWidget(self.endMin, 2, 0, 1, 1)

        self.endMinBox = QDateTimeEdit(self.filter3)
        self.endMinBox.setMaximumSize(QSize(180, 30))
        self.endMinBox.setCalendarPopup(True)
        self.endMinBox.setDisplayFormat(u"yyyy-MM-ddThh:mm:ssZ")
        self.endMinBox.setMinimumDateTime(minDateTime)
        self.filterLayout3.addWidget(self.endMinBox, 2, 1, 1, 1)
        #Max
        self.endMax = QLabel("End Date Max", self.filter3)
        self.filterLayout3.addWidget(self.endMax, 3, 0, 1, 1)
        
        self.endMaxBox = QDateTimeEdit(self.filter3)
        self.endMaxBox.setMaximumSize(QSize(180, 30))
        self.endMaxBox.setCalendarPopup(True)
        self.endMaxBox.setDisplayFormat(u"yyyy-MM-ddThh:mm:ssZ")
        self.endMaxBox.setMinimumDateTime(minDateTime)
        self.filterLayout3.addWidget(self.endMaxBox, 3, 1, 1, 1)
        
        
        self.filtersLayout.addWidget(self.filter3)
        #Filter 4
        self.filter4 = QGroupBox(self.filters)
        self.filterLayout4 = QGridLayout(self.filter4)
        self.filterLayout4.setSpacing(0)
        self.filterLayout4.setContentsMargins(3, 0, 3, 0)
        #Volume
        self.minVol = QLabel("Min Volume",self.filter4)
        self.filterLayout4.addWidget(self.minVol, 0, 0, 1, 1)
        
        self.minVolBox = QSpinBox(self.filter4)
        self.minVolBox.setMaximumSize(QSize(90, 30))
        self.minVolBox.setMaximum(999999999)
        self.filterLayout4.addWidget(self.minVolBox, 0, 1, 1, 1)
        #Max
        self.maxVol = QLabel("Max Volume",self.filter4)
        self.filterLayout4.addWidget(self.maxVol, 1, 0, 1, 1)
        
        self.maxVolBox = QSpinBox(self.filter4)
        self.maxVolBox.setMaximumSize(QSize(90, 30))
        self.maxVolBox.setMaximum(999999999)
        self.filterLayout4.addWidget(self.maxVolBox, 1, 1, 1, 1)
        #Liquidity
        self.minLiq = QLabel("Min Liquidity",self.filter4)
        self.filterLayout4.addWidget(self.minLiq, 2, 0, 1, 1)
        
        self.minLiqBox = QSpinBox(self.filter4)
        self.minLiqBox.setMaximumSize(QSize(90, 30))
        self.minLiqBox.setMaximum(999999999)
        self.filterLayout4.addWidget(self.minLiqBox, 2, 1, 1, 1)
        #Max
        self.maxLiq = QLabel("Max Liquidity",self.filter4)
        self.filterLayout4.addWidget(self.maxLiq, 3, 0, 1, 1)
        
        self.maxLiqBox = QSpinBox(self.filter4)
        self.maxLiqBox.setMaximumSize(QSize(90, 30))
        self.maxLiqBox.setMaximum(999999999)
        self.filterLayout4.addWidget(self.maxLiqBox, 3, 1, 1, 1)
        
        self.filtersLayout.addWidget(self.filter4)
        #Filter 5
        self.filter5 = QGroupBox(self.filters)
        self.filterLayout5 = QVBoxLayout(self.filter5)
        self.filterLayout5.setSpacing(0)
        self.filterLayout5.setContentsMargins(3, 0, 3, 0)
        self.filter5.setMinimumSize(QSize(200, 16777215))
        self.filter5.setMaximumSize(QSize(300, 16777215))

        self.tagsTab = QTabWidget(self.filter5)
        self.includeTab = QWidget()

        self.includeTabLayout = QVBoxLayout(self.includeTab)
        self.includeTabScroll = QScrollArea(self.includeTab)
        self.includeTabScrollBox = QWidget()
        self.includeTabScrollBoxLayout = QVBoxLayout(self.includeTabScrollBox)
        self.includeTabScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.include1 = QCheckBox("Sports", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include1)

        self.include2 = QCheckBox("Politics", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include2)

        self.include3 = QCheckBox("Crypto", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include3)

        self.include26 = QCheckBox("Weather", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include26)


        self.include4 = QCheckBox("Technology", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include4)

        self.include5 = QCheckBox("News", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include5)

        self.include6 = QCheckBox("Elections", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include6)

        self.include7 = QCheckBox("Predictions", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include7)

        self.include8 = QCheckBox("Future_Events", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include8)

        self.include9 = QCheckBox("Awards", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include9)

        self.include10 = QCheckBox("Video_Games", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include10)

        self.include11 = QCheckBox("Release_Date", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include11)

        self.include12 = QCheckBox("Person_of_the_year", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include12)

        self.include13 = QCheckBox("Box_Office", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include13)

        self.include14 = QCheckBox("Blockchain", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include14)

        self.include15 = QCheckBox("Esports", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include15)

        self.include16 = QCheckBox("Business", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include16)

        self.include17 = QCheckBox("Time_magazine", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include17)

        self.include18 = QCheckBox("US", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include18)

        self.include19 = QCheckBox("Climate", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include19)

        self.include20 = QCheckBox("Joe_Biden", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include20)

        self.include21 = QCheckBox("Musk", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include21)

        self.include22 = QCheckBox("Zuck", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include22)

        self.include23 = QCheckBox("Football", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include23)

        self.include24 = QCheckBox("Basketball", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include24)

        self.include25 = QCheckBox("Gta_6", self.includeTabScrollBox)
        self.includeTabScrollBoxLayout.addWidget(self.include25)

        self.includeTabScroll.setWidget(self.includeTabScrollBox)
        self.includeTabLayout.addWidget(self.includeTabScroll)
        self.tagsTab.addTab(self.includeTab, "Include Tags")


        self.excludeTab = QWidget()

        self.excludeTabLayout = QVBoxLayout(self.excludeTab)
        self.excludeTabScroll = QScrollArea(self.excludeTab)
        self.excludeTabScrollBox = QWidget()
        self.excludeTabScrollBoxLayout = QVBoxLayout(self.excludeTabScrollBox)
        self.excludeTabScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.exclude1 = QCheckBox("Sports", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude1)

        self.exclude2 = QCheckBox("Politics", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude2)

        self.exclude3 = QCheckBox("Crypto", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude3)

        self.exclude26 = QCheckBox("Weather", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude26)

        self.exclude4 = QCheckBox("Technology", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude4)

        self.exclude5 = QCheckBox("News", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude5)

        self.exclude6 = QCheckBox("Elections", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude6)

        self.exclude7 = QCheckBox("Predictions", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude7)

        self.exclude8 = QCheckBox("Future_Events", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude8)

        self.exclude9 = QCheckBox("Awards", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude9)

        self.exclude10 = QCheckBox("Video_Games", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude10)

        self.exclude11 = QCheckBox("Release_Date", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude11)

        self.exclude12 = QCheckBox("Person_of_the_year", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude12)

        self.exclude13 = QCheckBox("Box_Office", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude13)

        self.exclude14 = QCheckBox("Blockchain", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude14)

        self.exclude15 = QCheckBox("Esports", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude15)

        self.exclude16 = QCheckBox("Business", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude16)

        self.exclude17 = QCheckBox("Time_magazine", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude17)

        self.exclude18 = QCheckBox("US", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude18)

        self.exclude19 = QCheckBox("Climate", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude19)

        self.exclude20 = QCheckBox("Joe_Biden", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude20)

        self.exclude21 = QCheckBox("Musk", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude21)

        self.exclude22 = QCheckBox("Zuck", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude22)

        self.exclude23 = QCheckBox("Football", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude23)

        self.exclude24 = QCheckBox("Basketball", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude24)

        self.exclude25 = QCheckBox("Gta_6", self.excludeTabScrollBox)
        self.excludeTabScrollBoxLayout.addWidget(self.exclude25)

        self.excludeTabScroll.setWidget(self.excludeTabScrollBox)
        self.excludeTabLayout.addWidget(self.excludeTabScroll)
        self.tagsTab.addTab(self.excludeTab, "Exclude Tags")

        self.filterLayout5.addWidget(self.tagsTab)
        self.filtersLayout.addWidget(self.filter5)

        #Filter 6
        self.filter6 = QGroupBox(self.filters)
        self.filterLayout6 = QVBoxLayout(self.filter6)
        self.filterLayout6.setSpacing(0)
        self.filterLayout6.setContentsMargins(3, 0, 3, 0)
        self.filterLayout6.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.orderLabel = QLabel("Order By", self.filter6)
        self.filterLayout6.addWidget(self.orderLabel)

        self.eventOrderFrame = QFrame(self.filter6)
        self.eventOrderFrameLayout = QHBoxLayout(self.eventOrderFrame)

        self.eventOrder = QLabel("Event", self.eventOrderFrame)
        self.eventOrderFrameLayout.addWidget(self.eventOrder)


        self.eventOrderBox = QComboBox(self.eventOrderFrame)
        self.eventOrderBox.setMinimumSize(QSize(160, 0))
        self.eventOrderBox.setMaximumSize(QSize(160, 500))
        self.eventOrderBox.addItem("None")
        self.eventOrderBox.addItem("volume_24hr")
        self.eventOrderBox.addItem("volume")
        self.eventOrderBox.addItem("liquidity")
        self.eventOrderBox.addItem("startDate")
        self.eventOrderBox.addItem("endDate")
        self.eventOrderBox.addItem("competitive")
        self.eventOrderBox.addItem("closed_time")

        self.eventOrderFrameLayout.addWidget(self.eventOrderBox)
        self.eventOrderBox.setCurrentIndex(0)
        self.filterLayout6.addWidget(self.eventOrderFrame)

        #Market Order Box
        self.marketOrderFrame = QFrame(self.filter6)
        self.marketOrderFrameLayout = QHBoxLayout(self.marketOrderFrame)

        self.marketOrder = QLabel("Market", self.marketOrderFrame)
        self.marketOrderFrameLayout.addWidget(self.marketOrder)

        self.marketOrderBox = QComboBox(self.marketOrderFrame)
        self.marketOrderBox.setMinimumSize(QSize(160, 0))
        self.marketOrderBox.setMaximumSize(QSize(160, 500))
        self.marketOrderBox.addItem("None")
        self.marketOrderBox.addItem("oneHourPriceChange")
        self.marketOrderBox.addItem("oneDayPriceChange")
        self.marketOrderBox.addItem("volume_24hr")
        self.marketOrderBox.addItem("volume")
        self.marketOrderBox.addItem("liquidity")
        self.marketOrderBox.addItem("startDate")
        self.marketOrderBox.addItem("endDate")

        self.marketOrderFrameLayout.addWidget(self.marketOrderBox)
        self.marketOrderBox.setCurrentIndex(0)

        self.filterLayout6.addWidget(self.marketOrderFrame)
        self.filtersLayout.addWidget(self.filter6)
        self.mainBox.addWidget(self.filters, 0, 0, 1, 1)
        
        #Tool Bar
        self.toolBar = QGroupBox()
        self.toolBar.setMaximumSize(QSize(16777215, 40))
        self.toolBarLayout = QHBoxLayout(self.toolBar)
        self.toolBarLayout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        
        self.searchBar = QLineEdit(self.toolBar)
        self.searchBar.setMinimumSize(QSize(300, 0))
        self.searchBar.setMaximumSize(QSize(300, 16777215))
        self.toolBarLayout.addWidget(self.searchBar)
        
        self.searchButton = QPushButton("Search", self.toolBar)
        self.searchButton.setMaximumSize(QSize(60, 16777215))
        self.toolBarLayout.addWidget(self.searchButton)
        self.searchButton.clicked.connect(self.search_events)
        
        self.back = QPushButton("<", self.toolBar)
        self.back.setMaximumSize(QSize(30, 16777215))
        self.back.clicked.connect(self.setBackward)
        self.toolBarLayout.addWidget(self.back)
        
        self.forward = QPushButton(">", self.toolBar)
        self.forward.setMaximumSize(QSize(30, 16777215))
        self.forward.clicked.connect(self.setForward)
        self.toolBarLayout.addWidget(self.forward)
        
        self.tracked = QPushButton("Tracked Markets", self.toolBar)
        self.tracked.setMaximumSize(QSize(120, 16777215))
        self.toolBarLayout.addWidget(self.tracked)
        
        self.past = QPushButton("Past Markets", self.toolBar)
        self.past.setMaximumSize(QSize(110, 16777215))
        self.toolBarLayout.addWidget(self.past)
        
        self.mainBox.addWidget(self.toolBar, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        mainFrame.addLayout(self.mainBox)
        self.setLayout(mainFrame)
        
    def setForward(self):
        offset = self.offsetBox.value() 
        limit = self.limitBox.value()
        value = offset + limit
        self.offsetBox.setValue(value)
    def setBackward(self):
        offset = self.offsetBox.value() 
        limit = self.limitBox.value()
        value = offset - limit
        self.offsetBox.setValue(value)


    def search_events(self):
        self.clearLayout(self.eventsGrid)
        order = False
        params = {}
        params["related_tags"] = "false"
        params["tag_id"] = []
        params["exclude_tag_id"] = []
        ascend = self.ascendBox.currentText()
        if ascend != "None":
            params["ascending"] = ascend
            #f
        
        active = self.activeBox.currentText()
        if active != "None":
            params["active"] = active
            #f
        
        closed= self.closedBox.currentText()
        if closed != "None":
            params["closed"] = closed
            #f  
        
        cyom = self.cyomBox.currentText()
        if cyom != "None":
            params["cyom"] = cyom
            #f
        
        limit = self.limitBox.value()
        if limit != 0:
            params["limit"] = f"{limit}"

        offset = self.offsetBox.value()
        if offset != 0:
            params["offset"] = f"{offset}"
         
        eventID = self.idBox.value()
        if eventID != 0:
            params["id"] = f"{eventID}"
        
        start_date_min = self.startMinBox.dateTime().toString("yyyy-MM-ddThh:mm:ssZ")
        if start_date_min != "2020-01-01T01:01:01Z":
            params["start_date_min"] = start_date_min
            #f
        #2026-02-07T05%3A31%3A56Z
        #2020-01-01T01%3A01%3A01Z
        start_date_max = self.startMaxBox.dateTime().toString("yyyy-MM-ddThh:mm:ssZ")
        if start_date_max != "2020-01-01T01:01:01Z":
            params["start_date_max"] = start_date_max
            #f
            
        end_date_min = self.endMinBox.dateTime().toString("yyyy-MM-ddThh:mm:ssZ")
        if end_date_min != "2020-01-01T01:01:01Z":
            params["end_date_min"] = end_date_min
            #f
        
        end_date_max = self.endMaxBox.dateTime().toString("yyyy-MM-ddThh:mm:ssZ")
        if end_date_max != "2020-01-01T01:01:01Z":
            params["end_date_max"] = end_date_max
            #f
        
        volume_min = self.minVolBox.value()
        if volume_min != 0:
            params["volume_min"] = f"{volume_min}"
        
        volume_max = self.maxVolBox.value()
        if volume_max != 0:
            params["volume_max"] = f"{volume_max}"
            
        liquidity_min = self.minLiqBox.value()
        if liquidity_min != 0:
            params["liquidity_min"] = f"{liquidity_min}"
        
        liquidity_max = self.maxLiqBox.value()
        if liquidity_max != 0:
            params["liquidity_max"] = f"{liquidity_max}"

        if self.exclude1.isChecked() == True:
            exclude_tag_enum = self.exclude1.text()
            params["exclude_tag_id"].append(tags[exclude_tag_enum].value)

        if self.exclude2.isChecked() == True:
            exclude_tag_enum = self.exclude2.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude3.isChecked() == True:
            exclude_tag_enum = self.exclude3.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude26.isChecked() == True:
            exclude_tag_enum = self.exclude26.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude4.isChecked() == True:
            exclude_tag_enum = self.exclude4.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude5.isChecked() == True:
            exclude_tag_enum = self.exclude5.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude6.isChecked() == True:
            exclude_tag_enum = self.exclude6.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude7.isChecked() == True:
            exclude_tag_enum = self.exclude7.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude8.isChecked() == True:
            exclude_tag_enum = self.exclude8.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude9.isChecked() == True:
            exclude_tag_enum = self.exclude9.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude10.isChecked() == True:
            exclude_tag_enum = self.exclude10.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude11.isChecked() == True:
            exclude_tag_enum = self.exclude11.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude12.isChecked() == True:
            exclude_tag_enum = self.exclude12.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude13.isChecked() == True:
            exclude_tag_enum = self.exclude13.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude14.isChecked() == True:
            exclude_tag_enum = self.exclude14.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude15.isChecked() == True:
            exclude_tag_enum = self.exclude15.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude16.isChecked() == True:
            exclude_tag_enum = self.exclude16.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude17.isChecked() == True:
            exclude_tag_enum = self.exclude17.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude18.isChecked() == True:
            exclude_tag_enum = self.exclude18.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude19.isChecked() == True:
            exclude_tag_enum = self.exclude19.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude20.isChecked() == True:
            exclude_tag_enum = self.exclude20.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude21.isChecked() == True:
            exclude_tag_enum = self.exclude21.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude22.isChecked() == True:
            exclude_tag_enum = self.exclude22.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude23.isChecked() == True:
            exclude_tag_enum = self.exclude23.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude24.isChecked() == True:
            exclude_tag_enum = self.exclude24.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.exclude25.isChecked() == True:
            exclude_tag_enum = self.exclude25.text()
            exclude_tag_id = tags[exclude_tag_enum].value
            params["exclude_tag_id"].append(exclude_tag_id)

        if self.include1.isChecked() == True:
            tag_enum = self.exclude1.text()
            params["tag_id"].append(tags[tag_enum].value)

        if self.include2.isChecked() == True:
            tag_enum = self.include2.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include3.isChecked() == True:
            tag_enum = self.include3.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include26.isChecked() == True:
            tag_enum = self.include26.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include4.isChecked() == True:
            tag_enum = self.include4.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include5.isChecked() == True:
            tag_enum = self.include5.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include6.isChecked() == True:
            tag_enum = self.include6.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include7.isChecked() == True:
            tag_enum = self.include7.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include8.isChecked() == True:
            tag_enum = self.include8.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include9.isChecked() == True:
            tag_enum = self.include9.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include10.isChecked() == True:
            tag_enum = self.include10.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include11.isChecked() == True:
            tag_enum = self.include11.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include12.isChecked() == True:
            tag_enum = self.include12.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include13.isChecked() == True:
            tag_enum = self.include13.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include14.isChecked() == True:
            tag_enum = self.include14.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include15.isChecked() == True:
            tag_enum = self.include15.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include16.isChecked() == True:
            tag_enum = self.include16.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include17.isChecked() == True:
            tag_enum = self.include17.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include18.isChecked() == True:
            tag_enum = self.include18.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include19.isChecked() == True:
            tag_enum = self.include19.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include20.isChecked() == True:
            tag_enum = self.include20.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include21.isChecked() == True:
            tag_enum = self.include21.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include22.isChecked() == True:
            tag_enum = self.include22.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include23.isChecked() == True:
            tag_enum = self.include23.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include24.isChecked() == True:
            tag_enum = self.include24.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)

        if self.include25.isChecked() == True:
            tag_enum = self.include25.text()
            tag_id = tags[tag_enum].value
            params["tag_id"].append(tag_id)
        
        market_order = self.marketOrderBox.currentText()
        if market_order != "None":
            params["order"] = market_order
            order = True
            #f
        event_order = self.eventOrderBox.currentText()
        if event_order != "None" and order != True:
            params["order"] = event_order
            #f
        
        if order: 
            url = "https://gamma-api.polymarket.com/markets"
            response = requests.get(url, params=params)
            print(params)
            markets = {}
            params = {}
            markets = response.json()
            params["id"] = []
            for market in markets:
                marketEventID = market["events"][0]["id"]
                params["id"].append(marketEventID)
        url = "https://gamma-api.polymarket.com/events"
        response = requests.get(url, params=params)
        events = {}
        events = response.json()
        print(start_date_min)
        print(params)
        self.displayEvents(events)


    def displayEvents(self, events):
        row = 0
        col = 0
        
        self.eventsGrid.setAlignment(Qt.AlignmentFlag.AlignTop)
        #|Qt.AlignmentFlag.AlignLeft
        self.eventScrollBox = QScrollArea()
        self.eventScrollBox.setFrameShape(QFrame.Shape.NoFrame)
        self.eventScrollBox.setFrameShadow(QFrame.Shadow.Raised)
        self.eventScrollBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.eventWidget = QWidget()
        self.eventWidgetLayout = QGridLayout(self.eventWidget)
        slug = []
        for event in events:
            if row == 3:
                row = 0
                col += 1
            self.eventBox = QGroupBox()
            self.eventBox.setMinimumSize(QSize(300, 0))
            self.eventBox.setMaximumSize(QSize(800, 500))
            self.eventBoxLayout = QVBoxLayout(self.eventBox)
            self.eventBoxLayout.setSpacing(0)
            
            try:
                event_title = event.get("title", "None")
            except:
                return

            self.title = QLabel(event_title, self.eventBox)
            self.title.setWordWrap(True)
            self.title.setMargin(6)
            self.eventBoxLayout.addWidget(self.title)
            
            self.timeFrame = QFrame(self.eventBox)
            self.timeFrame.setFrameShape(QFrame.Shape.StyledPanel)
            self.timeFrameLayout = QHBoxLayout(self.timeFrame)
            self.timeFrameLayout.setContentsMargins(0, 0, 0, 0)
            self.timeFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
            self.startEndBox = QGroupBox(self.timeFrame)
            self.startEndBoxLayout = QVBoxLayout(self.startEndBox)
            self.startEndBoxLayout.setContentsMargins(0, 0, 0, 0)
            self.startEndBoxLayout.setSpacing(3)
            
            self.startFrame = QFrame(self.startEndBox)
            self.startFrameLayout = QHBoxLayout(self.startFrame)

            self.startFrameLayout.setContentsMargins(6, 3, 6, 0)
            self.startFrameLayout.setSpacing(3)
            self.start = QLabel("Start", self.startFrame)
            self.startFrameLayout.addWidget(self.start)
            self.startLine = QFrame(self.startFrame)
            self.startLine.setFrameShape(QFrame.Shape.VLine)
            self.startLine.setFrameShadow(QFrame.Shadow.Sunken)
            self.startFrameLayout.addWidget(self.startLine)
            start = event.get("startDate", "2020-01-01T01:01:01Z")
            startVar = self.parseTime(start)
            startDate = startVar.date()
            
            self.startTime = QLabel(str(startDate), self.startFrame)
            self.startFrameLayout.addWidget(self.startTime)
            self.startEndBoxLayout.addWidget(self.startFrame)
            
            self.endFrame = QFrame(self.startEndBox)
            self.endFrameLayout = QHBoxLayout(self.endFrame)

            self.end = QLabel("End", self.endFrame)
            self.endFrameLayout.addWidget(self.end)
            self.endFrameLayout.setContentsMargins(6, 0, 6, 3)
            self.endFrameLayout.setSpacing(3)
            self.endLine = QFrame(self.startFrame)
            self.endLine.setFrameShape(QFrame.Shape.VLine)
            self.endLine.setFrameShadow(QFrame.Shadow.Sunken)
            self.endFrameLayout.addWidget(self.endLine)
            end = event.get("endDate", "2020-01-01T01:01:01Z")
            endVar = self.parseTime(end)
            
            endDate = endVar.date()
            
            self.endTime = QLabel(str(endDate), self.endFrame)
            self.endFrameLayout.addWidget(self.endTime)
            self.startEndBoxLayout.addWidget(self.endFrame)
            self.timeFrameLayout.addWidget(self.startEndBox)
            
            self.resolveBox = QGroupBox(self.timeFrame)
            self.resolveBoxLayout = QVBoxLayout(self.resolveBox)
            
            self.resolveBoxLayout.setContentsMargins(3, 3, 0, 3)
            self.resolveBoxLayout.setSpacing(3)
            self.resolve = QLabel("Remaining time", self.resolveBox)
            self.resolveBoxLayout.addWidget(self.resolve)
            self.resolveLine = QFrame(self.resolveBox)
            self.resolveLine.setFrameShape(QFrame.Shape.HLine)
            self.resolveBoxLayout.addWidget(self.resolveLine)
        
            endTime = event.get("endDate", "2020-01-01T01:01:01Z")
            target_time = self.parseTime(endTime)
            now = datetime.now(timezone.utc)
            time_remaining = target_time - now
            time_remaining -= timedelta(microseconds=time_remaining.microseconds)
            
            self.resolveTime = QLabel(str(time_remaining), self.resolveBox)
            self.resolveBoxLayout.addWidget(self.resolveTime)
            self.timeFrameLayout.addWidget(self.resolveBox)
            self.eventBoxLayout.addWidget(self.timeFrame)
            
            self.marketLabel = QLabel("Markets", self.eventBox)
            self.marketLabel.setMargin(6)
            self.eventBoxLayout.addWidget(self.marketLabel)
            
            self.marketScrollBox = QScrollArea(self.eventBox)
            self.marketScrollBox.setFrameShape(QFrame.Shape.NoFrame)
            self.marketScrollBox.setFrameShadow(QFrame.Shadow.Raised)
            self.marketWidget = QWidget()
            self.marketWidgetLayout = QVBoxLayout(self.marketWidget)
            self.marketWidgetLayout.setContentsMargins(0, 0, 0, 0)
            slug = event.get("slug", "None")
            
            
            markets = event["markets"]
            for market  in markets:
                self.marketBox = QGroupBox(self.marketWidget)
                self.marketBoxLayout = QHBoxLayout(self.marketBox)
                self.marketBoxLayout.setContentsMargins(3, 3, 3, 3)
                self.marketBoxLayout.setSpacing(3)
                self.marketInfoFrame = QFrame(self.marketBox)
                self.marketInfoFrameLayout = QVBoxLayout(self.marketInfoFrame)
                self.marketInfoFrameLayout.setContentsMargins(0, 0, 3, 0)
                self.marketInfoFrameLayout.setSpacing(3)
                self.marketTopBox = QGroupBox(self.marketInfoFrame)
                self.marketTopBoxLayout = QHBoxLayout(self.marketTopBox)
                
                self.marketTopic = market.get("question", "Nothing") 
                self.marketTopicLabel = QLabel(self.marketTopic, self.marketTopBox)
                self.marketTopicLabel.setWordWrap(True)
                self.marketTopBoxLayout.addWidget(self.marketTopicLabel)
                                
                self.marketInfoFrameLayout.addWidget(self.marketTopBox)
                
                self.marketBottomBox = QGroupBox(self.marketInfoFrame)
                self.marketBottomBoxLayout = QHBoxLayout(self.marketBottomBox)
                
                self.marketLiquidity = market.get("liquidity", 0) 
                self.marketLiquidityLabel = QLabel(f"liq: {float(self.marketLiquidity):.0f}", self.marketBottomBox)
                self.marketBottomBoxLayout.addWidget(self.marketLiquidityLabel)
                
                self.line1M = QFrame(self.marketBottomBox)
                self.line1M.setFrameShape(QFrame.Shape.VLine)
                self.line1M.setFrameShadow(QFrame.Shadow.Sunken)
                self.marketBottomBoxLayout.addWidget(self.line1M)
                
                self.oneHour = str(market.get("oneHourPriceChange", 0))
                self.oneHourLabel = QLabel(f"1hr: {float(self.oneHour):.2f}", self.marketBottomBox)
                self.marketBottomBoxLayout.addWidget(self.oneHourLabel)
                
                self.line2M = QFrame(self.marketBottomBox)
                self.line2M.setFrameShape(QFrame.Shape.VLine)
                self.line2M.setFrameShadow(QFrame.Shadow.Sunken)
                self.marketBottomBoxLayout.addWidget(self.line2M)
                
                self.oneDay = str(market.get("oneDayPriceChange", 0))
                self.oneDayLabel = QLabel(f"24hr: {float(self.oneDay):.2f}", self.marketBottomBox)
                self.marketBottomBoxLayout.addWidget(self.oneDayLabel)
                
                self.marketInfoFrameLayout.addWidget(self.marketBottomBox)
                self.marketBoxLayout.addWidget(self.marketInfoFrame)
                
                self.buttonsFrame = QFrame(self.marketBox)
                self.buttonsFrame.setMaximumSize(60, 16777215)
                
                self.buttonsFrameLayout = QVBoxLayout(self.buttonsFrame)
                self.buttonsFrameLayout.setSpacing(0)
                self.buttonsFrameLayout.setContentsMargins(0, 0, 0, 0)
                # This is still a string: "[\"0.06\", \"0.94\"]"
                string = market.get("outcomePrices", "[\"0.00\", \"0.00\"]")  
                # Parse it a second time to turn it into a real list
                outcome_prices = json.loads(string)

                
                self.buttonYes = QPushButton(f"Yes: {float(outcome_prices[0]):.2f}", self.buttonsFrame)
                self.buttonYes.setMinimumSize(60, 40)
                self.buttonYes.clicked.connect(partial(self.openBrowser, slug))
                self.buttonsFrameLayout.addWidget(self.buttonYes)
                
                self.buttonNo = QPushButton(f"No: {float(outcome_prices[1]):.2f}", self.buttonsFrame)
                self.buttonNo.setMinimumSize(60, 40)
                self.buttonNo.clicked.connect(partial(self.openBrowser, slug))
                self.buttonsFrameLayout.addWidget(self.buttonNo)
                
                self.marketBoxLayout.addWidget(self.buttonsFrame)
                self.marketWidgetLayout.addWidget(self.marketBox)
            #set market contents to scroll box
            self.marketScrollBox.setWidget(self.marketWidget)
            #set markets to an event
            self.eventBoxLayout.addWidget(self.marketScrollBox)
            #set an event to 3rd section contents
            self.eventWidgetLayout.addWidget(self.eventBox, col, row, 1, 1)
            row += 1
        #set 3rd section contents to scroll box
        self.eventScrollBox.setWidget(self.eventWidget)
        #Add scroll box to 3rd section
        self.eventsGrid.addWidget(self.eventScrollBox)
        #Add 3rd section to main
        self.mainBox.addLayout(self.eventsGrid, 2, 0, 1, 1)
        print(slug)
    
    def parseTime(self, text):
        try:
            return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        except ValueError:
            return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
    def openBrowser(self, slug):
        webbrowser.open(f"https://polymarket.com/event/{slug}")


    def onResponse(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            self.label.setText(f"Error: {reply.errorString()}")
            reply.deleteLater()
            return

        raw = reply.readAll()
        reply.deleteLater()
        
    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_app = ManyDealApp()
    window_app.show()
    sys.exit(app.exec())
#response = requests.get("https://randomfox.ca/floof")
#fox = response.json()
#print(fox['image'])
