# import os
# os.getcwd()
import sys
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import scipy
import csv
import subprocess
import os

# find counter
count1=int(len(os.listdir('/home/Desktop/tests1/Results'))/2)
print(f'CONFIRM {count1}')

# try:
#     ingress1=sys.argv[1]
#     hhj=sys.argv[2]
# except:
#     ingress1=input('server side firewall if on, drop attack packets in ingress or input?')
#     hhj=input('whether rst syn ack dropped by attacker or not')

list1=[] #holds time period labels
list2=[] #holds load average values for last 1 min
list3=[] #holds load average values for last 5 mins
list4=[] #holds idle time
list5=[] #holds sum of %cpu for top 5 processes

# with open('/Users/subi/Downloads/top.txt','r') as file11:
file11= open('./top.txt','r')
# lines11=file11.readlines()
# print('Done')

yuyu=file11.readline().split(',')
print(yuyu[0])
print(yuyu[1][:-1])

durr1=int(yuyu[0]) #duration of attack
pott1=yuyu[1][:-1]
print(f'READ DURATION IS {durr1},{pott1}')

res111=subprocess.run(['sudo','systemctl','status','nftables'],stdout=subprocess.PIPE,text=True)
# inde1=res111.stdout.find('Active: ')
inde1=res111.stdout[135:145]
print(f"CONFIRM PLISS {inde1}")
if inde1.startswith('active'):

    filename1='active'+str(durr1)+'_'+pott1
    ingress1='ingress'
    hhj='nodrop'
else:
    filename1='inactive'+str(durr1)+'_'+pott1
    ingress1='nofire'
    hhj='nofire'

glogo1=0
for line in file11:
    if line[:3]=='top':
        glogo1=glogo1+1
        # print(line)
        # print('OKAY')
        # print(line[6:15])
        if 'load average' in line:
            pos1=line.find('load average: ')
            # print(pos1)
            list1.append(line[6:15])
            list2.append(float(line[pos1+14:pos1+18]))
            list3.append(float(line[pos1+20:pos1+24]))
    if line[:8]=='%Cpu(s):':
        # print(line)
        pos2=line.find('id,')
        # print(pos2)
        list4.append(float(line[pos2-6:pos2-1]))
        # list4.append(line[pos2-6:pos2-1])

    if line[:7]=='    PID':
#        print(line)
        pos3=line.find('')
#        print(pos3)
        tempsum=0

        for _ in range(5):
            newl=next(file11)
            line222=newl.split()[8]
            tempsum=tempsum+float(line222)

        list5.append(tempsum)            
    if line.startswith('ENDEXP'):
        print('BABA')
        print(line[6:])
        alldrt=line[6:].split(',')
        ab1,ab2,ab3,ab4,ab5,ab6,ab7=alldrt[0],alldrt[1],alldrt[2],alldrt[3],alldrt[4],alldrt[5],alldrt[6]
        #time for which experiment run, time for which system unavailable,globalsum,# of requests that failed, # of requests sent out

print(f'# of tops captured is! {glogo1}')    
# print(list2)    
# print(list3)    
#print(list4)    




aa3=[]
for aa in list1:
    # print(f'WW{aa}WW',type(aa))
    aa2=datetime.strptime(aa.strip(),'%H:%M:%S')
    # print(aa2)
    seconds=(aa2.time().hour*3600)+(aa2.time().minute*60)+(aa2.time().second)
    aa3.append(seconds)

aa4=[aa-aa3[0] for aa in aa3]
aa5=[aa/aa4[-1] for aa in aa4] #this now holds percentages of total time the experiment ran for. 
#plt.plot(aa5,bba,marker='x')

#from aa4, we find max time for which top didnt report results
aa41=[aa4[i+1]-aa4[i] for i in range(len(aa4)-1)]
tottime=aa4[-1]-aa4[0]



notop=sum(x for x in aa41 if x!=1)
# ENABLE!
print(f'Max no top reported is {max(aa41)}')
print(f'experiment ran for {aa4[-1]-aa4[0]}')
print(f'total time for which top not reported {notop}')
# print(aa41)
print(f'New downtime is {   notop / (aa4[-1]-aa4[0])    }')
print('Max 1 min load, max 5 min load, min idle cpu, max cpu load below')
print(max(list2),max(list3),min(list4),max(list5))

# print(f'OOOOOO{10/tottime}')

fig, axs=plt.subplots(4,1,figsize=(10,10),sharex=True)
#fig, axs=plt.subplots(4,1,figsize=(10,8))
axs[0].plot(aa5,list2,marker='o')
axs[0].set_title('1 min load average')
#axs[0].text(10/tottime,.015,'Attack starts')
axs[0].text(10/tottime,0,'X',va='center',color='y',size='x-large')
#axs[0].text((10+durr1)/tottime,.015,'Attack ends')
axs[0].text((10+durr1)/tottime,0,'X',va='center',color='m',size='x-large')


axs[1].plot(aa5,list3,marker='o')
axs[1].set_title('5 min load average')
#axs[1].text(10/tottime,.015,'Attack starts')
axs[1].text(10/tottime,0,'X',va='center',color='y',size='x-large')
#axs[1].text((10+durr1)/tottime,.015,'Attack ends')
axs[1].text((10+durr1)/tottime,0,'X',va='center',color='m',size='x-large')

axs[2].plot(aa5,list4,marker='o')
axs[2].set_title('Idle cpu %')
#axs[2].text(10/tottime,.015,'Attack starts')
axs[2].text(10/tottime,0,'X',ha='center',color='y',size='x-large')
#axs[2].text((10+durr1)/tottime,.015,'Attack ends')
axs[2].text((10+durr1)/tottime,0,'X',ha='center',color='m',size='x-large')

axs[3].plot(aa5,list5,marker='o')
axs[3].set_title('Cpu load%, top 5 pids')
#axs[3].text(10/tottime,.015,'Attack starts')
axs[3].text(10/tottime,0,'X',va='center',color='y',size='x-large')
#axs[3].text((10+durr1)/tottime,.015,'Attack ends')
axs[3].text((10+durr1)/tottime,0,'X',va='center',color='m',size='x-large')

plt.tight_layout()
plt.savefig(f'./Results/{filename1}_{ingress1}_all_{count1}.png')
# plt.subplots_adjust(hspace=1)
# plt.show()







#find areas under curves.
#print(list2)
# print(aa3)
# print('GAWKKKKKK\n')
# print(list5)
# print('GAWKKKKKK\n')
# print(aa4)
# print(np.round(aa5,2))
#list44=np.array(list1)
#print(type(list44[0]),list44[0])
#for val in list44:
#	print(type(val))

#print(aa4)
#print('PPP')
#print(aa5)

Nsum11=np.trapezoid(list5,x=aa5) #average cpu load% over entire duration. :-)
Nsum11a=np.trapezoid(list5,x=aa4)
sum12=scipy.integrate.simpson(y=list5,x=aa4) #WE USE THIS! is the sum of cpu loads over entire duration
sum12a=scipy.integrate.simpson(y=list5,x=aa5)

sum13=scipy.integrate.simpson(y=list4,x=aa4) #is the sum idle cpu over entire experiment duration
sum14=scipy.integrate.simpson(y=list4,x=aa5) #is the avg idle cpu over entire experiment duration
Nsum13a=np.trapezoid(list4,x=aa5)
Nsum14a=np.trapezoid(list4,x=aa4)
# ENABLE
print(f'avg,auc for cpuload is {round(Nsum11,2)}, {round(Nsum11a,2)}')
print(f'auc,avg for idle cpu is {round(Nsum13a,2)},{round(Nsum14a,2)}')




# plt.figure(figsize=(20,10))
# # xxxw1=[a for a in range(len(list2))]
# # print(xxxw1)
# plt.plot(aa5,list2,marker='o')
# plt.show()

# plt.figure(figsize=(20,10))
# # xxxw1=[a for a in range(len(list2))]
# # print(xxxw1)
# plt.plot(aa5,list3,marker='o')
# plt.show()

# now we fit an exponential decay curve, find time to hit .1 load average value

blaba=list3
newy2=blaba[blaba.index(max(blaba)):]
# newx2=[xx for xx in range(len(newy2))]
newx2=aa5[blaba.index(max(blaba)):]


# check list2 and 3, which is isotonically decreasing.
trp1=all(newy2[i+1]<=newy2[i] for i in range(len(newy2)-1))
trp2=all(newx2[i+1]<=newx2[i] for i in range(len(newx2)-1))
print('KALAKALAKALA')
print(trp1,trp2,len(list2),len(list3),len(newy2),len(newx2))
# print(list2)


def exp_dec(x,a,b,c):
    return a*np.exp(-b*x)+c



#plot data so we can debug curvefit.
plt.figure(figsize=(20,10))
plt.title('LALA')
plt.plot(newx2,newy2,marker='.')
plt.show()

try:
    popt_exp, _ = scipy.optimize.curve_fit(exp_dec, newx2, newy2)
    at=popt_exp[0]
    bt=popt_exp[1]
    ct=popt_exp[2]

    y2t=[]
    for xx in newx2:
        y=exp_dec(xx,at,bt,ct)
        y2t.append(y)

    # plot decay curve
    plt.figure(figsize=(20,10))
    plt.plot(newx2,y2t)
    plt.plot(newx2,newy2,marker='.')
    plt.savefig(f'./Results/{filename1}_{ingress1}_decay_{count1}.png')
    plt.show()

    # time to hit predefined asymptote value
    def tta1(y,a,b,c):
        return -(np.log((y-c)/a)/b)

    time35=tta1(.35,at,bt,ct)
    print(f'Time to hit .35 load average 1 min is {time35}')

except Exception as e:
    print(f'ISSUE {e}')
    time35=-0

finally:

    print(f'Time to hit .35 load average 1 min is {time35}')

# print('GAWKKKKKK')
# print(y2t)
# print('GAWKKKKKK')
# print(newy2)
# print('GAWKKKKKK')
# print(newx2)


pcksize=77

# get file size, compute number of packets. 
rala=subprocess.run(['du','-h','/home/Desktop/tests1/tcpdump.pcap'],capture_output=True,text=True)
vall1=str(rala.stdout).split('\t')[0]
print(vall1)
if 'M' in vall1:
    vall2=float(vall1[:-1])
    ans1=round(vall2*1024*1024/pcksize,2)
    print(ans1)
    print('B1')
elif 'K' in vall1:
    vall2=float(vall1[:-1])
    ans1=round(vall2*1024/pcksize,2)
    print(ans1)
    print('B2')
elif 'G' in vall1:
	vall2=float(vall1[:-1])
	ans1=round(vall2*1024*1024*1024/pcksize,2)
	print(ans1)
	print('B4')
else:
    vall2=float(vall1)
    ans1=round(vall2/pcksize,2)
    print(ans1)
    print('B3')


columns2=['type','#packets','.35 load avg time','avg cpuload%','auc cpuload%','avg idle cpu%','auc idle cpu','max no top reported','experiment time','time top not reported','new downtime','max 1 min load','max 5 min load','min idle cpu','max cpu load','time for which exp run','time for which sys unavailable','globalsum','# reqs failed','# reqs sent','attackdurr','pps','downtime2','downtime3','packets sent hping3','packets server side tcpdump']
dataall=[filename1+'_'+ingress1+'_'+hhj,ans1,time35,round(Nsum11,2),round(Nsum11a,2),round(Nsum14a,2),round(Nsum13a,2),max(aa41),aa4[-1]-aa4[0],notop,notop / (aa4[-1]-aa4[0]),max(list2),max(list3),min(list4),max(list5),float(ab1),float(ab2),float(ab3),int(ab4),int(ab5),durr1,round(ans1/durr1,3),round(int(ab4)/int(ab5),2),round(float(ab2)/float(ab1),2),int(ab6),int(ab7)]
newdaa=pd.DataFrame([dataall],columns=columns2)

# newdaa.to_csv('ala6.csv',index=False)
newdaa.to_csv('ala6.csv',mode='a',index=False,header=False)


plop=pd.read_csv('ala6.csv')
plop2=plop.drop_duplicates()
print(plop2)

# now lets move the tcpdump and top output files for safekeeping, further deepdives

os.rename('/home/Desktop/tests1/tcpdump.pcap',f'/home/Desktop/tests1/Results/tcpdump_{filename1}_{count1}.pcap')
os.rename('/home/Desktop/tests1/top.txt',f'/home/Desktop/tests1/Results/top_{filename1}_{count1}.txt')
