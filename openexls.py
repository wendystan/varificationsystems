import xlrd

excelopen=xlrd.open_workbook(r'C:\Users\wendy stan\Desktop\建亲190103\enh785\209.xls')
table=excelopen.sheets()[0]
name=table.cell_value(1,1)
print(name)
for i in range(3,table.nrows):
    date=table.cell_value(i,0)
    date=str(xlrd.xldate.xldate_as_datetime(date,0)).replace('-','').replace(':','').replace(' ','')
    value=table.cell_value(i,1)
    print(date,value)

