
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import time
import os
from datetime import datetime


class Ui_Form(QWidget):
    def setupUi(self, Form):
        self.select_time = True
        self.file_dir = ""
        self.log_file = os.getcwd()+"/log.text"
        self.now_time = str(datetime.now())
        self.co=1
        self.cotrue = 0

        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.folder_select_button = QtWidgets.QPushButton(Form)
        self.folder_select_button.setGeometry(QtCore.QRect(110, 10, 30, 30))
        self.folder_select_button.setText("")
        self.folder_select_button.setObjectName("folder_select_button")
        self.start_button = QtWidgets.QPushButton(Form)
        self.start_button.setGeometry(QtCore.QRect(150, 10, 90, 30))
        self.start_button.setText("Start")
        self.start_button.setObjectName("start_button")
        self.select_name = QtWidgets.QComboBox(Form)
        self.select_name.setGeometry(QtCore.QRect(10, 10, 90, 30))
        self.select_name.setObjectName("select_name")
        self.select_name.addItem("")
        self.select_name.addItem("")
        self.dir_name = QtWidgets.QTextEdit(Form)
        self.dir_name.setGeometry(QtCore.QRect(10, 50, 380, 60))
        self.dir_name.setObjectName("dir_name")
        self.result_status = QtWidgets.QTextEdit(Form)
        self.result_status.setGeometry(QtCore.QRect(10, 120, 100, 30))
        self.result_status.setObjectName("result_status")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.select_name.activated[str].connect(self.select_True_False)
        self.folder_select_button.clicked.connect(self.pushButtonClicked)
        self.start_button.clicked.connect(self.start_name_change)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Folder File name Change"))
        self.select_name.setItemText(0, _translate("Form", "수정일자"))
        self.select_name.setItemText(1, _translate("Form", "생성일자"))

    def select_True_False(self, text):
        if text =="수정일자":
            self.select_time = True
        elif text == "생성일자":
            self.select_time = False

    def pushButtonClicked(self):
        self.file_dir= QFileDialog.getExistingDirectory(self)+"/"
        self.dir_name.setText(self.file_dir)


    def start_name_change(self):
        if self.file_dir == "":
            print("no dap ")
        else :
            if os.path.exists(self.log_file):
                with open(self.log_file, "a+") as f:
                    f.write("\n\n\n")
                    f.write(self.now_time)
                    f.write("\n\n")
            else:
                with open(self.log_file, "w") as f:
                    f.write(self.now_time)
                    f.write("\n\n")

            for root, dirs, files in os.walk(self.file_dir):  # 파일의 위치를 가지고 옴 / 리눅스
                # 지정한 폴더 안에 있는 추가적인 폴더도 포함한다.
                for fname in files:
                    full_fname = os.path.join(root, fname)

                    if self.select_time:
                        second_time = os.path.getmtime(full_fname)  # getmtime = 최근 수정날짜를 가지고옴
                    else:
                        second_time = os.path.getctime(full_fname)  # getctime = 최초 생성일짜를 가지고옴

                    ttt = time.gmtime(second_time)
                    date_year = str(ttt[0]) + '년 '
                    date_month = str(ttt[1]) + '월 '
                    date_day = str(ttt[2]) + '일 '
                    date_hour = str(ttt[3] + 9) + ':'
                    date_minute = str(ttt[4]) + '.'
                    date_second = str(ttt[5])

                    _, ext = os.path.splitext(full_fname)  # _ = 파일의 이름만 , ext = 파일의 확장자만
                    Dtm = (date_year + date_month + date_day + date_hour + date_minute + date_second + ext)  # 이게형식

                    while True:
                        test_txt = os.path.exists(root + Dtm)

                        if test_txt == True:
                            zco = "_" + str(self.co).zfill(2)
                            Dtm = (date_year + date_month + date_day + date_hour + date_minute + date_second + zco + ext)  # 이게형식

                            self.co = self.co + 1
                            self.cotrue = self.cotrue + 1

                        elif test_txt == False:
                            with open(self.log_file, "a+") as f:
                                f.write(fname + " -> " + Dtm + "\n")
                            os.rename(full_fname, root + '/' + Dtm)  # 현재 파일의 이름을 정의한 형식 Dtm 으로 변경한다.

                            print("총 몇번의 true가 발생했습니까? : " + str(self.cotrue))
                            self.co = 1
                            self.cotrue = 0
                            break

                    print('=' * 60)

            self.result_status.setText("Sucess")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
