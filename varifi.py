import csv
import xlrd
import sqlite3
import tkinter
from tkinter import filedialog
import xlwt
import time
from datetime import datetime
from tkinter import ttk
import threading
import queue

rootsql=sqlite3.connect(database='varification.db')
cusors=rootsql.cursor()
print("SQLITE CONNECT SUCCESS")
def checkfile():
    filename=filedialog.askopenfilenames(title='请选择你需要的验证原始文件',filetypes=[('csv文件','*csv'),('excel文件','*xls'),('all','*.*')])
    for i in filename:
        listbox.insert('end',i)

    lenoff = '目前文件数：' + str(listbox.size()-1) + ' ' + '目前数据库包含：'
    dateinfo = cusors.execute('''PRAGMA table_info(VARIFI)''')
    j = 0
    for i in dateinfo:
        j = j + 1
        if j > 2:
            lenoff = lenoff + str(i[1]) + ','
    try:
        listbox.delete(0)
    finally:
        listbox.insert(0, lenoff)

def opencsv():
    begaintime=entrybegain.get()
    endtime=entryend.get()
    if begaintime!='' and endtime!='':
        try:
            cusors.execute(
                '''CREATE TABLE IF NOT EXISTS VARIFI(ID INTEGER PRIMARY KEY ,TIMES CHAR(20))''')
        except Exception as e:
            print(e)
        print(listbox.size())
        num=listbox.size()
        for k in range(1,num):
            print(listbox.get(k))
            csvopen=csv.DictReader(open(listbox.get(k)))
            j=0
            idset=0
            for i in csvopen:
                j+=1
                if j==9:
                    print(i['设备信息'])
                    name=i['设备信息'].replace('备注信息:','')
                    print(name)
                    try:
                        cusors.execute('''ALTER TABLE VARIFI ADD COLUMN '%s' CHAR(10)'''%name)
                    except Exception as e:
                        print(e)
                elif j>13 and i['设备信息']!=' ':
                    timeint=i['设备信息'].replace('/','').replace(':','').replace(' ','')
                    try:
                        timeint = int(timeint[4:6]+timeint[0:4]+timeint[6:10])
                    except Exception as e:
                        print(e)
                    if timeint>=int(begaintime) and timeint<=int(endtime):
                        idset=idset+1
                        print(idset)
                        # cusors.execute('''REPLACE INTO VARIFI (ID,TIMES,'%s')VALUES('%s','%s,'%s')'''%(name,idset,i['设备信息'],i['记录结果']))
                        #cusors.execute('''INSERT INTO VARIFI(ID,TIMES,'%s')VALUES('%s','%s','%s')'''%(name,idset,i['设备信息'],i['记录结果']))
                        try:
                            cusors.execute('''INSERT OR IGNORE INTO VARIFI(ID,TIMES)VALUES('%d','%s');'''%(idset,i['设备信息']))
                        except Exception as e:
                            print(e)
                        cusors.execute('''UPDATE VARIFI SET '%s'='%s'WHERE ID='%d';'''%(name,i['记录结果'],idset))
            rootsql.commit()
    else:
        entrybegain.insert(0,'请输入开始时间')
        entryend.insert(0,'请输入结束时间')



def createexcle():
    vexcel=xlwt.Workbook(encoding='utf-8')
    sheet=vexcel.add_sheet("varification",cell_overwrite_ok=True)
    begaintime = entrybegain.get()
    endtime = entryend.get()
    if begaintime != '' and endtime != '':
        sheet.write(0, 0, '时间')
        num = listbox.size()
        for k in range(1, num):
            filenames=listbox.get(k)[-3:]
            if filenames=='csv':
                csvopen = csv.DictReader(open(listbox.get(k)))

                j = 0
                idset = 0
                for i in csvopen:
                    j += 1
                    if j == 9:
                        name = i['设备信息'].replace('备注信息:', '')
                        sheet.write(0,k,name)
                    elif j > 13 and i['设备信息'] != ' ':
                        timeint = i['设备信息'].replace('/', '').replace(':', '').replace(' ', '')
                        timeint = int(timeint[4:6]+timeint[0:4]+timeint[6:10])

                        if timeint >= int(begaintime) and timeint <= int(endtime):
                            idset = idset + 1
                            sheet.write(idset,0, i['设备信息'])
                            sheet.write(idset,k,float(i['记录结果']))
            elif filenames=='xls':
                varitable=xlrd.open_workbook(listbox.get(k)).sheets()[0]
                name=varitable.cell_value(1,1).replace('备注：','')
                sheet.write(0,k,name)
                idset=0
                for i in range(3,varitable.nrows):
                    timeint=varitable.cell_value(i,0)
                    timeints=str(xlrd.xldate.xldate_as_datetime(timeint,0))
                    timeint=int(timeints.replace('-','').replace(':','').replace(' ','')[2:12])

                    if timeint >= int(begaintime) and timeint <= int(endtime):
                        idset=idset+1
                        sheet.write(idset,0,timeints)
                        sheet.write(idset,k,varitable.cell_value(i,1))




        urls=str(time.time())
        vexcel.save(r"D:\360MoveData\Users\WENDY'S STAN\Desktop\验证导出文件\\"+urls+"varifi.xls")
    else:
        entrybegain.insert(0, '请输入开始时间')
        entryend.insert(0, '请输入结束时间')



def creatlines():
    global varilines,linesmax,linesmin,linesave
    xmax = datetime.strptime(entryend.get(),'%y%m%d%H%M')
    xmin = datetime.strptime(entrybegain.get(),'%y%m%d%H%M')
    ymax = 30
    ymin = 0
    xblank = float(entryxblank.get())*60
    yblank = int(entryyblank.get())
    xpoint = xblank * 1660 /((xmax - xmin).total_seconds())
    ypoint = yblank * 560 /(ymax - ymin)
    xpointd=1660 /((xmax - xmin).total_seconds())
    ypointd=560 /(ymax - ymin)
    xpointlen = (xmax - xmin).total_seconds() /xblank
    ypointlen = (ymax - ymin) /yblank
    for i in range(int(xpointlen) + 1):
        canvass.create_line(20 + xpoint * i, 580, 20 + xpoint * i, 585, fill='white')
    for i in range(int(ypointlen) + 1):
        canvass.create_line(20, 20 + ypoint * i, 15, 20 + ypoint * i, fill='white')


    if entrybegain.get() != '' and entryend.get() != '':
        num = listbox.size()
        varilines={}

        linesmax={}
        linesmin={}
        linesave={}
        names=[]
        for k in range(1, num):
            csvopen = csv.DictReader(open(listbox.get(k)))
            j = 0
            pointfirst=[]
            linesall = []
            for i in csvopen:
                j += 1
                if j == 9:
                    name = i['设备信息'].replace('备注信息:', '')
                    names.append(name)

                if j > 13 and i['设备信息'] != ' ':
                    timeint = i['设备信息'].replace('/', '').replace(':', '').replace(' ', '')
                    timeint = timeint[4:6] + timeint[0:4] + timeint[6:10]
                    timeint = datetime.strptime(timeint,'%y%m%d%H%M')

                    if timeint >= xmin  and timeint <= xmax:
                        pointx=(timeint-xmin).total_seconds()
                        pointx=pointx*xpointd+20
                        pointfirst.append(pointx)
                        pointy=float(i['记录结果'])-ymin
                        pointy=580-(pointy*ypointd)
                        pointfirst.append(pointy)
                        linesall.append(pointy)


            sum=0
            for i in range(len(linesall)):
                sum=sum+linesall[i]
            linesave.update({name:sum/len(linesall)})
            linesmax.update({name: max(linesall)})
            linesmin.update({name:min(linesall)})
            variline=canvass.create_line(pointfirst, fill=goodcolors[k])
            varilines.update({name:variline})
            linecombo['values'] = names


    else:
        entrybegain.insert(0, '请输入开始时间')
        entryend.insert(0, '请输入结束时间')

def changelines():
        for i in goodlines:
            canvass.delete(i)
            goodlines=[]
        for key in varilines:
            canvass.itemconfig(varilines[key],fill='black')
        linesnames=linecombo.get()
        colorsname=colorentry.get()
        for i in range(len(varilines)):
            canvass.tag_raise(varilines[linesnames])
        canvass.itemconfig(varilines[linesnames],fill=colorsname)
        maxlines=canvass.create_line(20,linesmax[linesnames],1660,linesmax[linesnames],fill=colorsname)
        minlines=canvass.create_line(20,linesmin[linesnames],1660,linesmin[linesnames],fill=colorsname)
        avelines=canvass.create_line(20,linesave[linesnames],1660,linesave[linesnames],fill=colorsname)
        goodlines.append([maxlines,minlines,avelines])


def cleardate():
    cusors.execute('''DROP TABLE IF EXISTS VARIFI''')
    listbox.delete(0, 'end')
    for key in varilines:
        canvass.delete(varilines[key])
    linecombo['values']=[]
    print('清除成功')
    listbox.insert(0, '清除成功，请重新选择文件')

global goodcolors
goodcolors=['pink','crimson','thistle','purple','blue','blueviolet','dodgerblue','lightblue','lightcyan','gold',\
            'navy','indigo','green','slateblue','white','aliceblue','cyan','teal','deepskyblue','royalblue',\
            'darkmagenta','aquamarine','lime','lawngreen','yellow','olive','lemonchiffon','ivory','khaki',\
            'orange','coral','linen','salmon','silver','rosybrown','indianred','silenna','peachpuff','mistyrose','oldlace']
global goodlines
goodlines=[]
window=tkinter.Tk()
window.title("VARIFICATION SYSTEM")
window.geometry('1800x1000')

forms=tkinter.Frame(window)

forms2=tkinter.Frame(window)

forms3=tkinter.Frame(window)

listbox=tkinter.Listbox(forms,width=140)
yscroll=tkinter.Scrollbar(forms,command=listbox.yview)
listbox.config(yscrollcommand=yscroll.set)
listbox.insert(0,'目前无文件，请选择csv文件')
checkbutton=tkinter.Button(forms2,width=8,text='上传文件',command=checkfile)

csvopenbutton=tkinter.Button(forms2,width=8,text='上传数据库',command=opencsv)

cleardatebutton=tkinter.Button(forms2,width=8,text='清除数据库',command=cleardate)

createexbutton=tkinter.Button(forms2,width=8,text='创建excel',command=createexcle)



entrybegain=tkinter.Entry(forms2,width=20,bd=5)
entryend=tkinter.Entry(forms2,width=20,bd=5)
entryxblank=tkinter.Entry(forms2,width=20,bd=5)
entryyblank=tkinter.Entry(forms2,width=20,bd=5)
label1=tkinter.Label(forms2,text='请输入开始时间')
label2=tkinter.Label(forms2,text='请输入结束时间')
label3=tkinter.Label(forms2,text='请输入时间间隔')
label4=tkinter.Label(forms2,text='请输入数据间隔')


canvass=tkinter.Canvas(forms3,width=1700,bg='black',height=600,bd=5,relief='groove')
canvass.create_line(20,580,1680,580,fill='red',arrow='last',arrowshape=(5,15,5))
canvass.create_line(20,580,20,20,fill='red',arrow='last',arrowshape=(5,15,5))
linesbutton=tkinter.Button(forms3,width=8,text='创建曲线',command=creatlines)
changecolor=tkinter.Button(forms3,width=8,text='修改颜色',command=changelines)
linesnumber=tkinter.StringVar()
linecombo=ttk.Combobox(forms3,width=8,textvariable=linesnumber,state='readonly')
colorentry=tkinter.Entry(forms3,width=8,bd=5)


forms.grid(row=0,column=0)
forms2.grid(row=0,column=1)
forms3.grid(row=1,column=0,columnspan=2)

listbox.pack(side='left')
yscroll.pack(side='right',fill='y')

checkbutton.grid(row=1,column=0)
csvopenbutton.grid(row=1,column=1)
cleardatebutton.grid(row=2,column=0)
createexbutton.grid(row=2,column=1)
entrybegain.grid(row=3,column=0)
entryend.grid(row=3,column=1)
label1.grid(row=4,column=0)
label2.grid(row=4,column=1)
entryxblank.grid(row=5,column=0)
entryyblank.grid(row=5,column=1)
label3.grid(row=6,column=0)
label4.grid(row=6,column=1)

canvass.grid(row=0,column=0,columnspan=2)

linesbutton.grid(row=1,column=0)
changecolor.grid(row=1,column=1)
linecombo.grid(row=2,column=0)
colorentry.grid(row=2,column=1)

window.mainloop()