
import datetime
times1='1912301230'
times2='2001021211'
times1=datetime.datetime.strptime(times1,'%y%m%d%H%M')
times2=datetime.datetime.strptime(times2,'%y%m%d%H%M')
timeblank=times2-times1
print(timeblank.seconds)
arr=[]
arr.append(1)
arr.append(2)
print(arr)
arr=[]
arr.append(3)
arr.append(4)
print(arr[1])