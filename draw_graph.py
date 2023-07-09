from dataclasses import replace
from tkinter import *
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
#import time as t
from tkinter import ttk
import re


global fx,gx,hx

#콤보박스의 선택에 따라 2-2-1의 화면을 바꾸는 함수
def on_combobox_select(event):
    selected_item = combobox.get()
    if selected_item=='f(x)':
        frame_fx.tkraise()
    elif selected_item=='g(x)':
        frame_gx.tkraise()
    elif selected_item=='h(x)':
        frame_hx.tkraise()

#그래프를 그리는 함수
def draw_graph():
    fig.clear()
    start,end=map(float, entry_range.get().split(','))
    x=np.linspace(start, end, 1000000)
    subplot=fig.add_subplot(1,1,1)
    subplot.axvline(x=0, color='black', linestyle='--') # x 축 표시
    subplot.axhline(y=0, color='black', linestyle='--') # y 축 표시
    check=[var_fx.get(),var_gx.get(),var_hx.get()]
    if check[0]:
        subplot.plot(x,f(x),label='f(x)',color='violet')
    if check[1]:
        subplot.plot(x,g(x),label='g(x)',color='cyan')
    if check[2]:
        subplot.plot(x,h(x),label='h(x)',color='red')
    
    subplot.legend(loc='upper right')

    try:
        miny,maxy=map(float, entry_yrange.get().split(','))
        if miny!=None and maxy!=None:
            subplot.set_ylim(miny,maxy)
    except:
        pass
    canvas.draw()
    
#현재 커서가 가 있는 엔트리 이름과 인덱스를 반환
def insert_text(data):
    focused_widget = root.focus_get()
    if isinstance(focused_widget, tk.Entry):
        focused_widget.insert(tk.INSERT, data)

#log(x,y)가 포함된 문자열을 받아 log(x)/log(y)로 바꿔주는 함수
def make_log(data):
    pattern = r'log\((.+?),(.+?)\)' # 수정된 정규 표현식 패턴
    replacement = r'((np.log(\2))/(np.log(\1)))' # 치환할 패턴
    return re.sub(pattern, replacement, data)

#root(x,y)가 포함된 문자열을 받아 y**(1/x)로 바꿔주는 함수
def make_root(data):
    pattern = r'root\((.+?),(.+?)\)' # 수정된 정규 표현식 패턴
    replacement = r'((\2)**(1/\1))' # 치환할 패턴
    return re.sub(pattern, replacement, data)

#상수함수를 만드는 함수
def make_constant(data):
    if "x" not in str(data):
        data = "0*x+" + str(data)
    return data

#절댓값을 만드는 함수
def make_abs(data):
    pattern = r'\|(.+?)\|' # 수정된 정규 표현식 패턴
    replacement = r'np.abs(\1)' # 치환할 패턴
    return re.sub(pattern, replacement, data)

def make_multi(data):
    pattern = r'(\d+)\((.+)\)' # (숫자)(괄호로 묶인 데이터)
    replacement = r'\1*(\2)' # 치환할 패턴
    data=re.sub(pattern, replacement, data)
    pattern = r'(\d+)([x|sin|cos|tan|pi|root|log]+)'  # (숫자)(특정 문자열)
    replacement = r'\1*\2'  # 선택된 패턴을 숫자와 문자 사이에 '*'를 추가하여 치환합니다.
    return re.sub(pattern, replacement, data)
    


#사용자가 입력한 값을 명령어에 맞게 전처리하는 함수
def preprocessing(data):              
    data=data.replace('^','**')
    data=data.replace('sin','np.sin')
    data=data.replace('cos','np.cos')
    data=data.replace('tan','np.tan')
    data=data.replace('pi','np.pi')
    data=make_log(data)
    data=make_root(data)
    data=make_constant(data)
    data=make_abs(data)
    data=make_multi(data) 
    return data

#전역변수 fx, gx, hx에 실행가능한 문자열을 대입
def make_fx():
    global fx
    str_fx=entry_fx.get()
    fx=preprocessing(str_fx)
    print(fx)

def make_gx():
    global gx
    str_gx=entry_gx.get()
    gx=preprocessing(str_gx)

def make_hx():
    global hx
    str_hx=entry_hx.get()
    hx=preprocessing(str_hx)

#f(x), g(x), h(x)
def f(x):
    global fx
    with np.errstate(divide='ignore'):
        return eval(fx)
def g(x):
    global gx
    with np.errstate(divide='ignore'):
        return eval(gx)
def h(x):
    global hx
    with np.errstate(divide='ignore'):
        return eval(hx)


root=Tk()
root.geometry("1000x750+250+10")

fig = Figure(figsize=(7,4.5), dpi=100) #그리프 그릴 창 생성
#첫 번째 Frame=>그래프가 그려지는 프레임
f_1=Frame(root, width=700, height=500, bd=2, relief="groove")
f_1.pack()
canvas = FigureCanvasTkAgg(fig, master=f_1)
canvas.get_tk_widget().pack()


#두 번째 Frame=>2-1과 2-2를 포함하는 그래프
f_2=Frame(root, width=1000, height=250, bd=2, relief="groove",bg='green')
f_2.pack()



#2-1 Frame=>함수를 설정하는 변수 입력(2-2의 버튼에 따라 달라짐)
f_2_1=Frame(f_2,bd=2, width=700, height=280,relief="groove",bg='pink')
f_2_1.grid()

frame_fx=Frame(f_2_1, bd=2, width=700, height=80, relief="groove",bg='yellow')
lab_fx=Label(frame_fx,text='f(x)=',bd=0)
entry_fx=Entry(frame_fx,width=95)
apply_fx=Button(frame_fx,text='완료',command=make_fx)

frame_gx=Frame(f_2_1, bd=2, width=700, height=80, relief="groove")
lab_gx=Label(frame_gx,text='g(x)=',bd=0)
entry_gx=Entry(frame_gx,width=95)
apply_gx=Button(frame_gx,text='완료',command=make_gx)

frame_hx=Frame(f_2_1, bd=2, width=700, height=80, relief="groove")
lab_hx=Label(frame_hx,text='h(x)=',bd=0)
entry_hx=Entry(frame_hx,width=95)
apply_hx=Button(frame_hx,text='완료',command=make_hx)

frame_prohibit=Frame(f_2_1, bd=2, width=700, height=80) #이상하게 모든 프레임에 위젯을 배치하면 프레임의 크기가 위젯에 맞춰 자동 조절되는 오류가 있어서 그 오류를 방지하기 위한 코드

frame_operator=Frame(f_2_1,bd=2,width=700,height=50,relief="groove",bg='red')
btn_abs=Button(frame_operator,text='절댓값',command=lambda:[insert_text('||')])
btn_root=Button(frame_operator,text='√',command=lambda:[insert_text('root()')])
btn_log=Button(frame_operator,text='log',command=lambda:[insert_text('log()')])
btn_sin=Button(frame_operator,text='sin',command=lambda:[insert_text('sin()')])
btn_cos=Button(frame_operator,text='cos',command=lambda:[insert_text('cos()')])
btn_tan=Button(frame_operator,text='tan',command=lambda:[insert_text('tan()')])

                 
frame_operator.grid(row=1,column=0)
btn_abs.pack(side='left')
btn_root.pack(side='left')
btn_log.pack(side='left')
btn_sin.pack(side='left')
btn_cos.pack(side='left')
btn_tan.pack(side='left')


msg='\n1.f(x),g(x),h(x) 중 설정할 함수를 선택합니다.\n2.해당 함수의 수식을 입력합니다\n사용가능 연산: 사칙연산(+-*/), 절댓값(|수식|), 삼각함수 일부(sin(a),cos(a),tan(a)), 제곱근(3제곱근2=root(3,2), 로그(log(밑,진수)),\n 거듭제곱(밑^지수), 곱하기 기호(*) 생략 지원\n 3. 확인 버튼을 누른다(필수!!!!)\n 4. 정의역의 범위를 설정한다\n 5. 치역 범위를 설정한다(선택)\n6. 원하는 함수에 체크하고 그리기 버튼을 누른다'
frame_manual=Frame(f_2_1,bd=2,width=700,height=50,relief="groove",bg='blue')
lab_manual=Label(frame_manual,bg='yellow',width=100,height=9,text='사용법'+msg,justify='left')
frame_manual.grid(row=2,column=0)
lab_manual.grid()



lab_fx.grid(sticky='w')
lab_gx.grid(sticky='w')
lab_hx.grid(sticky='w')

entry_fx.grid(row=1)
entry_gx.grid(row=1)
entry_hx.grid(row=1)

frame_fx.grid(row=0,column=0)
frame_gx.grid(row=0,column=0)
frame_hx.grid(row=0,column=0)
frame_prohibit.grid(row=0,column=0)

apply_fx.grid(row=3,sticky='e')
apply_gx.grid(row=3,sticky='e')
apply_hx.grid(row=3,sticky='e')


#2-2 Frame=>설정할 함수를 선택하는 2-2-1과 그래프의 범위와 그릴 그래프를 선택하고 그리기 버튼이 있는 2-2-2
f_2_2=Frame(f_2, bd=2, width=260, height=280, relief="groove",bg='violet')
f_2_2.grid(row=0,column=1)

f_2_2_1=Frame(f_2_2, bd=2, width=260, height=40, relief="groove")
f_2_2_1.grid()
lab_setting=Label(f_2_2_1, text='<설정할 함수 선택>',width=20,bd=0)
lab_setting.grid()
combobox = ttk.Combobox(f_2_2_1, values=['f(x)', 'g(x)', 'h(x)'],width=10)
combobox.grid(row=1)
combobox.bind("<<ComboboxSelected>>", on_combobox_select)



f_2_2_2=Frame(f_2_2, bd=2, width=260, height=250, relief="groove")
f_2_2_2.grid(row=1)

lab_range=Label(f_2_2_2, text='<정의역 범위 설정>\n"형식: 시작 수,끝 수 " ',width=20,bd=0)
lab_range.grid()
entry_range=Entry(f_2_2_2)
entry_range.grid(row=1)

lab_yrange=Label(f_2_2_2, text='<치역 설정>\n"형식: 최소, 최대 " ',width=20,bd=0)
lab_yrange.grid(row=2)
entry_yrange=Entry(f_2_2_2)
entry_yrange.grid(row=3)

lab_setting=Label(f_2_2_2, text='<그릴 함수 선택>',width=20,bd=0)
lab_setting.grid(row=4)

var_fx=IntVar()
var_gx=IntVar()
var_hx=IntVar()

check_fx=Checkbutton(f_2_2_2,text="f(x)",variable=var_fx)
check_gx=Checkbutton(f_2_2_2,text="g(x)",variable=var_gx)
check_hx=Checkbutton(f_2_2_2,text="h(x)",variable=var_hx)

check_fx.grid(row=5,sticky='w')
check_gx.grid(row=6,sticky='w')
check_hx.grid(row=7,sticky='w')

btn_draw=Button(f_2_2_2,text='그리기', command=draw_graph)
btn_draw.grid(row=8,sticky='e',pady=(10,0))


root.mainloop()