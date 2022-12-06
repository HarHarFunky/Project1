#!/bin/python3

import re
import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_pocketDNSresolver(object):
    fDomain=""
    fIP=""
    def InputCheck(self, pocketDNSresolver, area=0):
        self.inputError.setText("")
        if area: #IP
            if self.ip4.isChecked(): 
                if not re.match(r'(?:(?:(?:1?\d{,2})|(?:2[01234]?\d?)|(?:25[012345]?))\.){,3}(?:(?:1?\d{,2})|(?:2[01234]?\d?)|(?:25[012345]?))$',cIP:=self.ipBox.text()): self.ipBox.setText(self.fIP)
                else: self.fIP = self.ipBox.text()
            elif self.ip6.isChecked():
                if not re.match(r'(?:[\da-f]{,4}\:){,7}[\da-f]{,4}$',cIP:=self.ipBox.text().lower()): self.ipBox.setText(self.fIP)
                else: self.fIP=cIP
        else: #Domain
            if not re.match(r'(?:[a-zA-Z\d\-]{1,63}\.)?[a-zA-Z\d\-]{,63}$',cDomain:=self.domainBox.text()): self.domainBox.setText(self.fDomain)
            else: self.fDomain=cDomain
        
    def add(self,ip,domain):
        if self.domainBox.text() == "": self.inputError.setText("Please put a domain down")
        elif not re.match(r'[a-zA-Z\d\-]{1,63}\.[a-zA-Z\d\-]{2,63}$',cDomain:=self.domainBox.text()): self.inputError.setText("Improper Domain Format")
        elif self.ipBox.text() == "": self.inputError.setText("Please add an IP to resolve to")
        else:
            if self.ip6.isChecked():
                if not re.match(r'(?:[\da-f]{,4}\:){7}[\da-f]{,4}$',cIP:=self.ipBox.text().lower()): self.inputError.setText("Improper IPv6 Format")
                else:
                    with open('files/output.csv','r') as cit:
                        for row in csv.reader(cit):
                            if row[1].casefold() ==  self.domainBox.text().casefold(): #Multiple domains can go to one IP, not vice-versa
                                print(row[1])
                                self.inputError.setText("Domain resolution already stored")
                                break
                        else:
                            with open('files/output.csv','a') as ciw: csv.writer(ciw).writerow(['6',cDomain,cIP])
            elif self.ip4.isChecked():
                if not re.match(r'(?:(?:(?:1?\d{,2})|(?:2[01234]?\d?)|(?:25[012345]?))\.){3}(?:(?:1?\d{,2})|(?:2[01234]?\d?)|(?:25[012345]?))$',cIP:=self.ipBox.text()): self.inputError.setText("Improper IPv4 Format")
                else:
                    with open('files/output.csv','r') as cit:
                        for row in csv.reader(cit):
                            if row[1].casefold() ==  self.domainBox.text().casefold(): #Multiple domains can go to one IP, not vice-versa
                                self.inputError.setText("Domain resolution already stored")
                                break
                        else: 
                            with open('files/output.csv','a') as ciw: csv.writer(ciw).writerow(['4',cDomain,cIP])
            else: self.inputError.setText("Please select an IP version")
                    
                
                
        
        
        
    def search(self,ip,domain):
        self.inputError.setText("")
        try:
            with open('files/output.csv','r') as cit:
                csi=csv.reader(cit)
                if self.domainBox.text() != "" and self.ipBox.text() != "": self.inputError.setText("Too many fields filled to resolve")
                elif self.domainBox.text() != "":
                    for row in csi:
                        if row[1].casefold() == self.domainBox.text().casefold():
                            if self.ip6.isChecked() and row[0] == '4': self.ip4.setChecked(True)
                            elif self.ip4.isChecked() and row[0] == '6': self.ip6.setChecked(True)
                            self.ipBox.setText(row[2])
                            break
                    else: self.inputError.setText("No IP found")
                    
                elif self.ipBox.text() != "":
                    for row in csi:
                        if row[2].lower() == self.ipBox.text().lower():
                            self.domainBox.setText(row[1])
                            break
                    else: self.inputError.setText("No domain found")
                
                else: self.inputError.setText("Please fill out a field to search")
        except FileNotFoundError: self.inputError.setText("Could not find 'files/output.csv'")
        except: self.inputError.setText("An unknown error has occured")
            
        
        
    def setupUi(self, pocketDNSresolver):
        if not pocketDNSresolver.objectName():
            pocketDNSresolver.setObjectName(u"pocketDNSresolver")
        pocketDNSresolver.resize(800, 400)
        pocketDNSresolver.setMinimumSize(QSize(800, 400))
        pocketDNSresolver.setMaximumSize(QSize(800, 400))
        self.interactArea = QWidget(pocketDNSresolver)
        self.interactArea.setObjectName(u"interactArea")
        self.interactArea.setEnabled(True)
        self.windowHeader = QLabel(self.interactArea)
        self.windowHeader.setObjectName(u"windowHeader")
        self.windowHeader.setGeometry(QRect(0, 0, 800, 75))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.windowHeader.sizePolicy().hasHeightForWidth())
        self.windowHeader.setSizePolicy(sizePolicy)
        bold = QFont()
        bold.setFamily(u"Noto Sans Mono")
        bold.setPointSize(24)
        bold.setBold(True)
        bold.setWeight(100)
        self.windowHeader.setFont(bold)
        self.windowHeader.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(self.interactArea)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 100, 800, 100))
        self.body = QHBoxLayout(self.layoutWidget)
        self.body.setSpacing(25)
        self.body.setObjectName(u"body")
        self.body.setContentsMargins(25, 0, 25, 0)
        self.domain = QVBoxLayout()
        self.domain.setObjectName(u"domain")
        self.domain.setContentsMargins(-1, -1, -1, 0)
        self.domainLabel = QLabel(self.layoutWidget)
        self.domainLabel.setObjectName(u"domainLabel")
        entryLabel = QFont()
        entryLabel.setFamily(u"Noto Sans Mono")
        entryLabel.setPointSize(12)
        self.domainLabel.setFont(entryLabel)
        self.domainLabel.setAlignment(Qt.AlignCenter)

        self.domain.addWidget(self.domainLabel)

        self.domainBox = QLineEdit(self.layoutWidget)
        self.domainBox.setObjectName(u"domainBox")
        font = QFont()
        font.setFamily(u"Noto Sans Mono")
        self.domainBox.setFont(font)
        self.domainBox.setAutoFillBackground(True)
        self.domainBox.setAlignment(Qt.AlignCenter)

        self.domain.addWidget(self.domainBox)


        self.body.addLayout(self.domain)

        self.ip = QVBoxLayout()
        self.ip.setObjectName(u"ip")
        self.ip.setContentsMargins(-1, 0, -1, -1)
        self.ipLabel = QLabel(self.layoutWidget)
        self.ipLabel.setObjectName(u"ipLabel")
        self.ipLabel.setFont(entryLabel)
        self.ipLabel.setAlignment(Qt.AlignCenter)

        self.ip.addWidget(self.ipLabel)

        self.ipBox = QLineEdit(self.layoutWidget)
        self.ipBox.setObjectName(u"ipBox")
        self.ipBox.setFont(font)
        self.ipBox.setAlignment(Qt.AlignCenter)

        self.ip.addWidget(self.ipBox)


        self.body.addLayout(self.ip)

        self.layoutWidget1 = QWidget(self.interactArea)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 300, 800, 100))
        self.layoutWidget1.setFont(font)
        self.buttonSelection = QHBoxLayout(self.layoutWidget1)
        self.buttonSelection.setSpacing(100)
        self.buttonSelection.setObjectName(u"buttonSelection")
        self.buttonSelection.setContentsMargins(100, 0, 100, 0)
        self.clearButton = QPushButton(self.layoutWidget1)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setFont(font)

        self.buttonSelection.addWidget(self.clearButton)

        self.addButton = QPushButton(self.layoutWidget1)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setFont(font)

        self.buttonSelection.addWidget(self.addButton)

        self.searchButton = QPushButton(self.layoutWidget1)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setFont(font)
        self.searchButton.setCheckable(False)
        self.searchButton.setChecked(False)

        self.buttonSelection.addWidget(self.searchButton)

        self.widget = QWidget(self.interactArea)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(450, 200, 350, 32))
        self.ipVersion = QHBoxLayout(self.widget)
        self.ipVersion.setSpacing(50)
        self.ipVersion.setObjectName(u"ipVersion")
        self.ipVersion.setContentsMargins(30, 0, 25, 0)
        self.ip4 = QRadioButton(self.widget)
        self.ip4.setObjectName(u"ip4")
        self.ip4.setFont(font)
        self.ip4.setChecked(True)

        self.ipVersion.addWidget(self.ip4)

        self.ip6 = QRadioButton(self.widget)
        self.ip6.setObjectName(u"ip6")
        self.ip6.setFont(font)

        self.ipVersion.addWidget(self.ip6)
        
        
        self.inputError = QLabel(self.interactArea)
        self.inputError.setObjectName(u"inputError")
        self.inputError.setGeometry(QRect(0, 60, 800, 50))
        self.inputError.setFont(entryLabel)
        self.inputError.setAlignment(Qt.AlignCenter)

        pocketDNSresolver.setCentralWidget(self.interactArea)
        QWidget.setTabOrder(self.domainBox, self.ipBox)
        QWidget.setTabOrder(self.ipBox, self.ip4)
        QWidget.setTabOrder(self.ip4, self.clearButton)
        QWidget.setTabOrder(self.clearButton, self.addButton)
        QWidget.setTabOrder(self.addButton, self.searchButton)

        self.retranslateUi(pocketDNSresolver)
        self.clearButton.clicked.connect(self.domainBox.clear)
        self.clearButton.clicked.connect(self.ipBox.clear)
        self.clearButton.clicked.connect(lambda:self.inputError.setText(""))
        self.ip6.toggled.connect(lambda:self.ipBox.setPlaceholderText("XXXX:XXXX:XXXX:XXXX:XXXX:XXXX"))
        self.ip4.toggled.connect(lambda:self.ipBox.setPlaceholderText("###.###.###.###"))
        self.ip6.toggled.connect(self.ipBox.clear)
        self.ip4.toggled.connect(self.ipBox.clear)
        self.ipBox.textEdited.connect(lambda:self.InputCheck(pocketDNSresolver,1))
        self.domainBox.textEdited.connect(lambda:self.InputCheck(pocketDNSresolver))
        self.addButton.clicked.connect(lambda:self.add(self.ipBox.text(),self.domainBox.text()))
        self.searchButton.clicked.connect(lambda:self.search(self.ipBox.text(),self.domainBox.text()))

        QMetaObject.connectSlotsByName(pocketDNSresolver)
    # setupUi

    def retranslateUi(self, pocketDNSresolver):
        pocketDNSresolver.setWindowTitle("Pocket DNS resolver")
        self.windowHeader.setText("Pocket DNS Resolver")
        self.domainLabel.setText("Domain")
        self.domainBox.setPlaceholderText("example.com")
        self.ipLabel.setText("IP")
        self.ipBox.setPlaceholderText("###.###.###.###")
        self.ip4.setText("IPv4")
        self.ip6.setText("IPv6")
        self.clearButton.setText("Clear entries")
        self.addButton.setText("Add entry")
        self.searchButton.setText("Search Data")
    # retranslateUi







def main():
    import sys
    app = QApplication(sys.argv)
    pocketDNSresolver = QMainWindow()
    ui = Ui_pocketDNSresolver()
    ui.setupUi(pocketDNSresolver)
    pocketDNSresolver.show()
    sys.exit(app.exec_())
    return ui

if __name__=='__main__': main()
