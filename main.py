import sys
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QThread,pyqtSignal,pyqtSlot,Qt
from PyQt5.QtWidgets import QMainWindow,QApplication


from grade_loader import *

import ctypes   

import os
import time
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
main_ui_path = BASE_DIR + '\main.ui'
setting_ui_path = BASE_DIR + '\\augmentSetting.ui'

start_class = uic.loadUiType(main_ui_path)[0]
setting_class = uic.loadUiType(setting_ui_path)[0]

counter_run = 1

class logLoadThread(QThread):
    
    fish_log = pyqtSignal(str,int,int)
    
    def __init__(self):
        super().__init__()
        self.power = True 
        
    def run(self):
        global counter_run
        path = BASE_DIR+'\logLoader.dll'
        #path = "C:\\Users\\PMKJun\\source\\repos\\logLoader\\x64\\Release\\logLoader.dll"

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
        money = ctypes.c_int()
        entropy = ctypes.c_int()
        readFish.argtypes = (ctypes.c_char_p,ctypes.c_long,ctypes.POINTER(ctypes.c_long),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int))
        readFish.restype = ctypes.c_char_p

        while self.power:
            if counter_run == 0:
                break
            cppsize = filesizeLoad(filepath)
            if cppsize < filesize :
                print("file?")
                time.sleep(0.5)
                filesize = cppsize
                
            outparam=readFish(filepath,filesize,rp,money,entropy)
            result = outparam.decode('euc-kr',errors='ignore')
            filesize=rp.value
            if money.value > 0 or result != ' ' or entropy.value > 0:
                self.fish_log.emit(result,money.value,entropy.value)
            
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
        self.setFixedSize(556, 362)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR+'\\fish_icon.png'))
        
        self.fontDB = QtGui.QFontDatabase()
        fontId=self.fontDB.addApplicationFont(":/fonts/NanumSquareR.ttf")
        families = QtGui.QFontDatabase.applicationFontFamilies(fontId)
        print(families)
        self.userfont = families[0]
        self.switch_btn.setIcon(QtGui.QIcon(BASE_DIR+'\\circle arrow.svg'))
        
        self.fish_grade_list = fish_grade_load()
        self.fish_count_method = [self.common, self.uncommon, self.rare, self.epic, self.legendary, self.myth, self.crab]
        self.fish_percent_method = [self.common_percent, self.uncommon_percent, self.rare_percent, self.epic_percent, self.legendary_percent, self.myth_percent, self.crab_percent]
        self.fish_type_method = [self.common_text, self.uncommon_text, self.rare_text, self.epic_text, self.legendary_text, self.myth_text, self.crab_text]
        self.percent_text_method = [self.percent0,self.percent1,self.percent2,self.percent3,self.percent4,self.percent5,self.percent6]
        self.fish_ea_method = [self.common_ea, self.uncommon_ea, self.rare_ea, self.epic_ea, self.legendary_ea, self.myth_ea, self.crab_ea]
        self.me_method = [self.money_text,self.label_gold,self.gold_ea,self.entropy_text,self.entropy_label,
                          self.entropy_ea,self.estimate_text,self.estimate_income,self.estimate_ea]
        self.btn_method = [self.reset_btn,self.pause_btn,self.augset_btn]
        self.sum_method = [self.sum_text,self.sum, self.sum_ea,self.sum_2]
        
        self.solar_aug = 0
        self.precision_aug = 0
        self.estimate_mode = 0 #돈 예상 모드 값
        self.solarPercent_list=[1,1.06, 1.11, 1.15, 1.19, 1.25]
        self.precisionPercent_list=[1,1.08, 1.11, 1.15, 1.2, 1.3, 1.45, 1.6, 1.7]
        
        self.setFonttext()
        
        self.loadSavedata()
        self.estimate_func()
        
        self.reset_btn.clicked.connect(self.reset_fish_count)
        self.pause_btn.clicked.connect(self.pause_thread)
        self.augset_btn.clicked.connect(self.openSettingWindow)
        self.switch_btn.clicked.connect(self.estimate_switch)
        #ss = sub_main
        #c=ss.add_func(1,2)
        #print("덧셈의 결과는 {}".format(c))

        self.start_thread_func()
    
    def setFonttext(self):
        for i in range(len(self.fish_count_method)):
            self.fish_count_method[i].setFont(QtGui.QFont(self.userfont,14))
            
        for i in range(len(self.fish_percent_method)):
            self.fish_percent_method[i].setFont(QtGui.QFont(self.userfont,14))
            
        for i in range(len(self.fish_type_method)):
            self.fish_type_method[i].setFont(QtGui.QFont(self.userfont,14))
            
        for i in range(len(self.percent_text_method)):
            self.percent_text_method[i].setFont(QtGui.QFont(self.userfont,14))
            
        for i in range(len(self.fish_ea_method)):
            self.fish_ea_method[i].setFont(QtGui.QFont(self.userfont,14))
        
        for i in range(len(self.me_method)):
            self.me_method[i].setFont(QtGui.QFont(self.userfont,14))
        
        for i in range(len(self.sum_method)):
            self.sum_method[i].setFont(QtGui.QFont(self.userfont,14))
        
        for i in range(len(self.btn_method)):
            self.btn_method[i].setFont(QtGui.QFont(self.userfont,12))
            
        self.version.setFont(QtGui.QFont(self.userfont,11))
        
        
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
        for i in range(len(self.fish_count_method)):
            self.fish_count_method[i].setText("0")
            self.fish_percent_method[i].setText("0.0")
        self.sum.setText("0")
        self.sum_2.setText("(0)")
        self.label_gold.setText("0")
        self.entropy_label.setText("0")
        self.estimate_income.setText("0")
        self.saveCurrentstat()
    
    def count_up(self,g): #물고기 등급 정보를 입력 받고 입력된 등급의 물고기 마리수 1씩 증가
        temp=self.fish_count_method[g].text()
        temp = int(temp) + 1
        self.fish_count_method[g].setText(str(temp))
        
        temp = self.sum.text()
        temp = int(temp) + 1

        self.sum.setText(str(temp))
        self.setsum_2()
           
    def getsum_2(self):
        sum2 = self.sum_2.text()
        sum2 = sum2.replace('(',"")
        sum2 = sum2.replace(')',"")
        sum2 = int(sum2)
        return sum2
    
    def setsum_2(self):
        csum = int(self.sum.text())
        crabtp = int(self.crab.text())
        self.sum_2.setText("("+str(csum-crabtp)+")")
        
    def calc_percentage(self):
        sum = int(self.sum.text())
        sum_2 = self.getsum_2()
        if sum == 0 :
            return
        for i in range(6):
            fish_temp=int(self.fish_count_method[i].text())
            fish_percent = fish_temp / sum_2 * 100
            fish_percent = round(fish_percent,2)
            self.fish_percent_method[i].setText(str(fish_percent))
            
        fish_temp=int(self.fish_count_method[6].text()) # 꽃게 확률 개별 계산
        fish_percent = fish_temp / sum * 100
        fish_percent = round(fish_percent,2)
        self.fish_percent_method[6].setText(str(fish_percent))
        
            
    def saveCurrentstat(self):
        with open("fishmedata.dat","w") as f:
            for i in range(7):
                fish_temp=self.fish_count_method[i].text()
                f.write(fish_temp)
                f.write("\n")
            fish_temp=self.label_gold.text()
            f.write(fish_temp)
            f.write("\n")
            fish_temp=self.entropy_label.text()
            f.write(fish_temp)
            f.write("\n")
            f.write(str(self.solar_aug))
            f.write("\n")
            f.write(str(self.precision_aug))
            f.write("\n")
                
    def loadSavedata(self):
        sum = 0
        try:
            with open("fishmedata.dat","r") as f:
                savedData = f.readlines()               
        except:
            return
        for i in range(7):
            c=savedData[i].strip()
            sum += int(c)
            self.fish_count_method[i].setText(c)
        c=savedData[7].strip()
        self.label_gold.setText(c)
        c=savedData[8].strip()
        self.entropy_label.setText(c)
        self.sum.setText(str(sum)) 
        self.setsum_2()
        self.calc_percentage()
        
        if len(savedData) <= 9:     #이전 버전 세이브 지원
            print("이전 버전의 세이브 파일이 감지되었습니다")
            return
        c=savedData[9].strip()      #솔라레이지 데이터 로드
        self.solar_aug = int(c)
        c=savedData[10].strip()     #정밀절단 데이터 로드
        self.precision_aug = int(c)
        
        
        
    def addMoney(self,money):
        currentMoney=int(self.label_gold.text())
        money = currentMoney + money
        self.label_gold.setText(str(money))
        
    def addEntropy(self,entropy):
        currentEntropy = int(self.entropy_label.text())
        entropy = currentEntropy + entropy
        self.entropy_label.setText(str(entropy))
        
    def openSettingWindow(self):
        self.setwin=settingWindow()
        self.setwin.show()
        
    def estimate_switch(self):
        if self.estimate_mode == 0:
            self.estimate_text.setText("예상 엔트로피")
            self.estimate_ea.setText("엔트로피")
            self.estimate_mode = 1
            self.estimate_func()
        else:
            self.estimate_text.setText("예상 수익")
            self.estimate_ea.setText("원")
            self.estimate_mode = 0
            self.estimate_func()
    
    def estimate_func(self):
        if self.estimate_mode:
            self.estimate_entropy()
        else:
            self.estimate_money()

    def estimate_money(self):
        estimate_sum = 0
        bal_list = [40,270,900,2700]
        for i in range(4):
            fish_temp=self.fish_count_method[i].text()
            estimate_sum += int(fish_temp) * bal_list[i]
        estimate_sum = estimate_sum * self.solarPercent_list[self.solar_aug]
        estimate_temp_sum = math.trunc(estimate_sum)
        self.estimate_income.setText(str(estimate_temp_sum))
    def estimate_entropy(self):
        estimate_sum = 0
        bal_list = [40,120,200,500]
        for i in range(4):
            fish_temp=self.fish_count_method[i].text()
            estimate_sum += int(fish_temp) * bal_list[i]
        estimate_sum = estimate_sum * self.precisionPercent_list[self.precision_aug]
        estimate_temp_sum = math.trunc(estimate_sum)
        self.estimate_income.setText(str(estimate_temp_sum))
    
    @pyqtSlot(str,int,int)
    def printLog(self,result,money,entropy):
        if result != ' ': #물고기 처리
            fish_count = [0 for i in range(7)]
            fish_list=result.split(",")
            for i in range(0,len(fish_list)-1):
                try:
                    g=self.fish_grade_list[fish_list[i]]
                    fish_count[g] += 1
                    self.count_up(g)
                except:
                    pass
            self.calc_percentage()
            self.saveCurrentstat()
            self.estimate_func()
        if money > 0 : #돈 처리
            self.addMoney(money)
            self.saveCurrentstat()
        if entropy > 0 : #엔트로피 처리
            self.addEntropy(entropy)
            self.saveCurrentstat()
        

class settingWindow(QMainWindow,setting_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR+'\\fish_icon.png'))
        self.setFixedSize(178, 174)
        self.move(myWindow.x()+560, myWindow.y()+188)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint) #최소화 최대화 버튼 제거
        self.setFont()
        
        self.solarup_btn.clicked.connect(self.increase_solar)
        self.solarDown_btn.clicked.connect(self.decrease_solar)
        self.precisionUP_btn.clicked.connect(self.increase_precision)
        self.precisionDown_btn.clicked.connect(self.decrease_precision)
        
        self.solarR.setText(str(myWindow.solar_aug))
        self.precisionC.setText(str(myWindow.precision_aug))
    
    def setFont(self):
        self.text_method = [self.solarR_text,self.solarR,self.precisionC_text,self.precisionC]
        self.btn_method = [self.solarup_btn,self.solarDown_btn,self.precisionUP_btn,self.precisionDown_btn]
        
        for i in range(len(self.text_method)):
            self.text_method[i].setFont(QtGui.QFont(myWindow.userfont,13))
            
        for i in range(len(self.btn_method)):
            self.btn_method[i].setFont(QtGui.QFont(myWindow.userfont,11))
    
    def increase_solar(self):
        if(myWindow.solar_aug < 5):
            myWindow.solar_aug += 1
            self.solarR.setText(str(myWindow.solar_aug))
            myWindow.estimate_func()
            myWindow.saveCurrentstat()
            
    
    def decrease_solar(self):
        if(myWindow.solar_aug > 0):
            myWindow.solar_aug -= 1
            self.solarR.setText(str(myWindow.solar_aug))
            myWindow.estimate_func()
            myWindow.saveCurrentstat()
    
    def increase_precision(self):
        if(myWindow.precision_aug < 8):
            myWindow.precision_aug += 1
            self.precisionC.setText(str(myWindow.precision_aug))
            myWindow.estimate_func()
            myWindow.saveCurrentstat()
    
    def decrease_precision(self):
        if(myWindow.precision_aug > 0):
            myWindow.precision_aug -= 1
            self.precisionC.setText(str(myWindow.precision_aug))
            myWindow.estimate_func()
            myWindow.saveCurrentstat()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()