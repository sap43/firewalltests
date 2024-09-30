#calculate everything! 1s of dos results in how many seconds overall of downtime, how much incremental time of downtime over and above duration of attack for which the system is obviously hanging, measure aftereffects of dos attack
# do we need a flood attack? Find reln between speed of attack and load on system

import datetime,time
from datetime import timedelta
from flask import Flask
import json
import requests
import multiprocessing
import subprocess
import matplotlib.pyplot as plt
import sys
import os

q=multiprocessing.Queue()

# print('ATTACJ DISAVKED!')

ip1='192.168.0.2'
port1='53221' #for server, is not dropped by firewall
port2='53222' #for dos attack, is dropped by firewall

dura1=5 #for how long does the dos attack last
dura2=100 #how many requests we send
start1=10 # at what request number should the attack start

# Enable to accept duration of attack as user input
# try:
# 	dura1=int(sys.argv[1])
# except:
# 	dura1=int(input('Enter duration of time for which attack runs'))


#os.system('sudo timeout 10s hping3 --flood -b -d .5 -p 53221 192.168.0.101')

res111=subprocess.run(['sudo','systemctl','status','nftables'],stdout=subprocess.PIPE,text=True)
# inde1=res111.stdout.find('Active: ')
inde1=res111.stdout[129:145]
if inde1.startswith('active'):
    filename1='active'+str(dura1)+'_'
else:
    filename1='inactive'+str(dura1)+'_'

# now we get the file counter from disc. urgh
counter111=int((len(os.listdir('/home/Desktop/tests1/Results'))/3))

# print(filename1)

# exit()

bb=[] #this holds request numbers when system was unavailable. Req 1 may be served, 2 not served, 3 served, then 4 to 10 not served.
bb2=[] #this holds duration of time, and whether available or not. Is contiguous. Positive means available
def fl2(q):
	# uuy1=datetime.datetime.now()
	# print('Sending attack now {}'.format(uuy1))
	poli=subprocess.run(['sudo','timeout',f'{dura1}s','hping3','--flood','-S','-b','-d','.5','-p',port2,ip1],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
	# uuy2=datetime.datetime.now()
	# print(poli.stdout)
	# print('1')
	# print(poli.stderr)
	# print('1')
	# print(poli)
	# print('1')
	try:
		if poli.stdout.index('packets transmitted'):
			poli2=poli.stdout
	except:
		poli2=poli.stderr

	# poli2=poli.stdout
	# poli3=poli.stderr

	for line in poli2.splitlines():
		# print('TTT')
		# print(line)
		if 'packets transmitted' in line:
			poli4=int(line[:line.index('packets transmitted')].strip())

	q.put(poli4)
	print(f'DONE {poli4}')
	# exit()
	# print(uuy2-uuy1)

proc2=multiprocessing.Process(target=fl2,args=(q,))

tt1=datetime.datetime.now() #starting time
print('Starting sending requests now'.format(tt1))

#start top printout
lolo1=requests.get(f'http://{ip1}:{port1}/look2/{dura1}/{port2}')
print(lolo1)

def fl33(i):
	yu1=datetime.datetime.now()
	try:
		# aloo=requests.get('http://192.168.0.101:53221/look1')
		aloo=requests.get(f'http://{ip1}:{port1}/look1',timeout=1)
	except Exception as e:
		yu2=datetime.datetime.now()
#		if i-1 in bb:
#		print('Failed')
		bb2.append(-((yu2-yu1).total_seconds()))
		bb.append(i)
	else:
		yu2=datetime.datetime.now()
		print(i, aloo, yu1, yu2)
		bb2.append((yu2-yu1).total_seconds())


for i in range(dura2):
	time.sleep(1)
	if i==start1:
		proc2.start() #we start the attack at a predefined point in time
	fl33(i)


print('DONe')
print(len(bb))
print(len(bb2))
print(len(bb)/dura2) #prop of all requests that failed #WORKS ONLY WITH TIMEOUT DEFINED!, smaller the timeout the better this data point!
print(len(bb)/len(bb2))
print(bb2)
print('GAWHAGAHAGA')
print(bb)
#app.run(host=ip1,port=port1)


# now lets build the time series chart of availability
fig,ax=plt.subplots()
globalsum1=0
for val in bb2:
    # print(ind)
    # print(val)
    color2='red' if val<0 else 'green'
    if val<0:
        val=val+1
    ax.plot([globalsum1,globalsum1+abs(val)],[0,0],color=color2,linewidth=2)
    ax.grid(True)
    globalsum1=globalsum1+abs(val)

ax.text(start1*globalsum1/dura2,.015,'Attack starts')
ax.text(start1*globalsum1/dura2,-.002,'X')

ax.text((start1+dura1)*globalsum1/dura2,.015,'Attack ends')
ax.text((start1+dura1)*globalsum1/dura2,-.002,'X')

print(f'globalsum is {globalsum1}')

# now calculate excess impact of the dos attack

#below is old, incorrect method
#sum2=sum(abs(x) for x in bb2) #test ran for this duration of time
#sum3=sum(abs(x) for x in bb2 if x<0) #time for which system unavailable
#SILLY
sum2=sum(x if x >0 else (abs(x)-1) for x in bb2) #test ran for this duration of time, adjusted for timeout 1 but non failing requests completed ver quickly
sum3=sum(abs(x)-1 for x in bb2 if x<0)
print(f'downtime is {sum3/sum2*100:.2f}%')
print(f'ratio of downtime to attack duration is {sum3/dura1}')


# print('OMG')

fig.suptitle('Normalized plot 1')
# plt.show()
plt.savefig(f'./Results/{filename1}_1_{counter111}.png')

#now show second plot, downtime only, but as a square wave LOL
fig,ax=plt.subplots()
fig.suptitle('Normalized plot 2') 
bb33=[min(x+1,1) for x in bb2]
ax.plot(bb33)
ax.text(start1,.015,'Attack starts')
ax.text(start1,-.015,'X')
ax.text(start1+dura1,.015,'Attack ends')
ax.text(start1+dura1,-.015,'X')
# plt.show()
plt.savefig(f'./Results/{filename1}_2_{counter111}.png')

fig,ax=plt.subplots()
fig.suptitle('Normalized plot 3') #we were getting spikes, square wave then hits some weird ass 1.6 load average peak, then stabilizes around 1 again. 
bb334=[x+1 for x in bb2]
ax.plot(bb334)
ax.text(start1,.015,'Attack starts')
ax.text(start1,-.015,'X')
ax.text(start1+dura1,.015,'Attack ends')
ax.text(start1+dura1,-.015,'X')

# plt.show()
plt.savefig(f'./Results/{filename1}_3_{counter111}.png')

#now lets stop top output and send stats to target
omg1=q.get()
# omg1=0

def rec1():
	try:
		lolo2=requests.get(f'http://{ip1}:{port1}/look3/{round(sum2,2)}/{round(sum3,2)}/{globalsum1}/{len(bb)}/{len(bb2)}/{omg1}')
	except requests.exceptions.ConnectionError as e:
		print('failed, system still down')
		time.sleep(2)
		rec1()
	finally:
		return lolo2


lolo2=rec1()

print(lolo2)
