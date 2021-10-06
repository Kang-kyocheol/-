# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 01:22:37 2021

@author: Kangkyocheol , kng430@naver.com ,https://github.com/Kang-kyocheol
MIT License


Easyocr
     Apache License
 Version 2.0, January 2004

Jamo
     Apache License
 Version 2.0, January 2004
"""
"""
이 모듈은 롤토체스의 하단부의 글자인식을 도와주는 기능으로
csv 파일을 용도에 맞게 변경할 경우
특정 단어들을 쉽게 인식하게 도와준다.
사용설명서
1 범위지정1 =>x1,y1
2 범위지정2 =>x2,y2  => x1~x2 y1~y2 사각박스 형성
0  글자인식시작
- 사각박스 스크린샷이 보임
= 초기화
esc종료
"""
"""
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
오류발생시 실행코드
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'  

import pyautogui
from PIL import Image 



import cv2
from jamo import h2j, j2hcj
import csv
import easyocr 

reader = easyocr.Reader(['ko'], gpu=True,recog_network='korean_g2') 

"""
자모분리 모듈 적용+ 리스트와 오차비교
"""
def calculate_hangul(a,b):
    per_=list()
    origin_text = a
    origin_jamo=j2hcj(h2j(origin_text))
    new_text = b
    new_jamo=j2hcj(h2j(new_text))
    
        
    if len(new_jamo)==len(origin_jamo) :
     for i in range(0,len(new_jamo)):
         if new_jamo[i-1]== origin_jamo[i-1] :
             per_.append(1)
         else:
             per_.append(0)
    if per_ ==[]:
       per_.append(0.5)
    return sum(per_)/len(per_)
"""
자모분리 모듈 적용+ 리스트와 오차비교
"""

"""
이미지 인식 기술+ 자모분리 적용파트 
"""
def image_to_text():
    image = cv2.imread('my_screenshot_cut.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    with open('C:/Users/82109/.spyder-py3/tft.csv') as csv_File:   #경로를 정해주세요
        csv_Reader = csv.reader(csv_File)
        list_csv = list( csv_Reader)
        list_csv2=[i[1]for i in list_csv][1:]
        
        
    
   # reader = easyocr.Reader(['ko'], gpu=True,recog_network='korean_g2') 
    result = reader.readtext(image,detail = 0) 
    print(result)
    
    name=list_csv2
    
    name_black=set(['리븐','리신','직스','럭스','잭스','베인'])
    aa=list()
    #자모 모듈을 이용한 list 단어와 ocr인식 단어 오차율 비교 
    for i in result:
      for g in name:
        if len(i)==len(g) :
            if calculate_hangul(g,i)>=0.6 and i!=g :
             if list(name_black.intersection(set([g])))!=[]:
               if list(name_black.intersection(set([g])))[0]!=g:
                   {aa.append(g)}
                  
                   
             else:
               aa.append(g)
               
            if  i==g :
              aa.append(g)
              
            if calculate_hangul(g,i) >=0.8 and i!=g :
              if list(name_black.intersection(set([g])))!=[] and i!='직스':
               
                   aa.append(g)
            
    print(aa)
    ##저장파트 
    with open('C:/Users/82109/.spyder-py3/tft_Result.csv') as csv_File2:   #경로를 정해주세요
      csv_Reader2 = csv.reader(csv_File2)
      list_csv_ = list( csv_Reader2)
      chess_number_=[ii[6]for (ii) in list_csv_][1:]
      chess_number=list()
      for i in chess_number_:
          chess_number.append(int(i))
      if chess_number==[]:
           for i in range(0,len(list_csv)):
             chess_number.append(0)
    f = open("tft_Result.csv", "w")
    aaa=list()
  
    for i in aa:
        aaa.append(list_csv2.index(i))
    
       
        #chess_number=list()
        
        

    
    for i in aaa:
        chess_number[i]+=1
    
    for a in range(0,len(list_csv)) :
           for b in range(0,7) :
                 
                
                 if a==0:
                  if b<6:
                   f.write( (list_csv[a][b])+',')
                  if b==6:
                     f.write('\n')  
                 if a>0 :
                     if b<6:
                      f.write( (list_csv[a][b])+',')
                     if b==6 and a<len(list_csv):
                      f.write( str(chess_number[a-1]))
                      f.write('\n')
       
    f.close()
    
"""
이미지 인식 기술+ 자모분리 적용파트 
"""


#키보드 인식담당    
from pynput import keyboard
sx=0
sy=0
ex=0
ey=0
def on_press(key):
    print('Key %s pressed' % key)
 

def on_release(key):
    print('Key %s released' %key)
     #인식범위 지정 1번키와 2번키로 사각박스 인식을 형성한다.
    if key == keyboard.KeyCode(char='1') :
        global sx
        sx=list(pyautogui.position())[0]
        global sy
        sy=list(pyautogui.position())[1]
    if key == keyboard.KeyCode(char='2') :
        global ex
        ex=list(pyautogui.position())[0]
        global ey
        ey=list(pyautogui.position())[1]
    if key == keyboard.KeyCode(char='0') :
     print("wow")
     pyautogui.screenshot('my_screenshot.png')#region=(sx,sy,ex,ey)
     
     image3=Image.open('my_screenshot.png')
     image4=image3.crop((sx,sy,ex,ey))
     image4.save('my_screenshot_cut.png')
     image_to_text()
    if key == keyboard.KeyCode(char='-') :
     image5=Image.open('my_screenshot_cut.png')   
     image5.show()
     
    
        
    if key == keyboard.Key.esc: #esc 키가 입력되면 종료
        return False
    if key == keyboard.KeyCode(char='=') :   
     """
        초기화파트
     """
     with open('C:/Users/82109/.spyder-py3/tft.csv') as csv_File:   #Comma separated values (csv)
        csv_Reader = csv.reader(csv_File)
        list_csv = list( csv_Reader)
        list_csv2=[i[1]for i in list_csv][1:]
        f = open("tft_Result.csv", "w")
        for a in range(0,len(list_csv)) :
            for b in range(0,7) :
                 
                
                 if a==0:
                  if b<6:
                   f.write( (list_csv[a][b])+',')
                  if b==6:
                     f.write('\n')  
                 if a>0 :
                     if b<6:
                      f.write( (list_csv[a][b])+',')
                     if b==6:
                      f.write( repr(0))
                      f.write('\n')
                 """    
                 if b == 6 and  a>0 :
                  f.write( repr(list_csv[a][0])  +','+repr(list_csv[a][1]) +','+repr(list_csv[a][2]) +','+repr(list_csv[a][3])
                          +','+repr(list_csv[a][4]) +','+repr(list_csv[a][5])+','+repr(chess_number[b-1])+'\n')
                 """ 
        f.close() 

 # 리스너 등록방법1
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()







  