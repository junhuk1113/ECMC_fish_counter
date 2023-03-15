import sys
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox

from grade_loader import *

import ctypes   

import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
main_ui_path = BASE_DIR + '\main.ui'

start_class = uic.loadUiType(main_ui_path)[0]

counter_run = 1

class logLoadThread(QThread):
    
    fish_log = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.power = True 
        
    def run(self):
        global counter_run
        path = BASE_DIR+'\logLoader.dll'

        c_module = ctypes.windll.LoadLibrary(path)

        print(c_module)

        filesizeLoad = c_module.filesizeLoad
        filesizeLoad.argtypes = [ctypes.c_char_p]
        filesizeLoad.restype = ctypes.c_long

        tempst = "C:/Users/" + os.getlogin() + "/AppData/Roaming/.minecraft/logs/latest.log"
        filepath = tempst.encode("euc-kr")
        outparam = filesizeLoad(filepath)
        filesize = outparam

        readFish = c_module.readFish
        rp = ctypes.c_long()
        readFish.argtypes = (ctypes.c_char_p,ctypes.c_long,ctypes.POINTER(ctypes.c_long))
        readFish.restype = ctypes.c_char_p

        while self.power:
            if counter_run == 0:
                break
            cppsize = filesizeLoad(filepath)
            if cppsize < filesize :
                print("file?")
                time.sleep(0.5)
                filesize = cppsize
                
            outparam=readFish(filepath,filesize,rp)
            result = outparam.decode('euc-kr',errors='ignore')
            filesize=rp.value
            if result ==' ':
                continue
            self.fish_log.emit(result)
        self.stop()
        
    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        self.power = False
        self.quit()
        self.wait(1000)  # 3초 대기 (바로 안꺼질수도)    
        
        
        

class MyWindow(QMainWindow,start_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR+'\\fish_icon.png'))
        self.fish_grade_list = fish_grade_load()
        self.fish_type = ['커먼','언커먼','레어','에픽','레전더리','신화']
        self.fish_count_method = [self.common, self.uncommon, self.rare, self.epic, self.legendary, self.myth]
        self.fish_percent_method = [self.common_percent, self.uncommon_percent, self.rare_percent, self.epic_percent, self.legendary_percent, self.myth_percent]
        
        self.loadSavedata()
        self.reset_btn.clicked.connect(self.reset_fish_count)
        self.pause_btn.clicked.connect(self.pause_thread)
        #ss = sub_main
        #c=ss.add_func(1,2)
        #print("덧셈의 결과는 {}".format(c))

        self.start_thread_func()
    
    def start_thread_func(self):
        self.thread_start = logLoadThread()
        self.thread_start.fish_log.connect(self.printLog)
        self.thread_start.start()
    
    def pause_thread(self):
        global counter_run
        if counter_run == 1:#쓰레드 중단
            counter_run = 0
            self.pause_btn.setText("카운트 시작")
        else:
            counter_run = 1
            self.start_thread_func()
            self.pause_btn.setText("카운트 중단")
        
    def reset_fish_count(self):
        for i in range(len(self.fish_type)):
            self.fish_count_method[i].setText("0")
            self.fish_percent_method[i].setText("0.0")
        self.sum.setText("0")
        with open("fishdata.dat","w") as f:
            for i in range(6):
                f.write("0")
                f.write("\n")
    
    def count_up(self,g): #물고기 등급 정보를 입력 받고 입력된 등급의 물고기 마리수 1씩 증가
        
        temp=self.fish_count_method[g].text()
        temp = int(temp) + 1
        self.fish_count_method[g].setText(str(temp))
        
        temp = self.sum.text()
        temp = int(temp) + 1
        self.sum.setText(str(temp))
    
    def calc_percentage(self):
        sum = int(self.sum.text())
        if sum == 0 :
            return
        
        for i in range(6):
            fish_temp=int(self.fish_count_method[i].text())
            fish_percent = fish_temp / sum * 100
            fish_percent = round(fish_percent,2)
            self.fish_percent_method[i].setText(str(fish_percent))
    def saveCurrentstat(self):
        with open("fishdata.dat","w") as f:
            for i in range(6):
                fish_temp=self.fish_count_method[i].text()
                f.write(fish_temp)
                f.write("\n")
    def loadSavedata(self):
        sum = 0
        try:
            with open("fishdata.dat","r") as f:
                savedData = f.readlines()               
        except:
            return
        for i in range(6):
            c=savedData[i].strip()
            sum += int(c)
            self.fish_count_method[i].setText(c)
        self.sum.setText(str(sum)) 
        self.calc_percentage()
    
    @pyqtSlot(str)
    def printLog(self,result):
        fish_count = [0 for i in range(6)]
        fish_list=result.split(",")
        for i in range(0,len(fish_list)-1):
            g=self.fish_grade_list[fish_list[i]]
            fish_count[g] += 1
            self.count_up(g)
        self.calc_percentage()
        self.saveCurrentstat()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()