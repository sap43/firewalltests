from scapy.all import *
from scapy.all import rdpcap
import matplotlib.pyplot as plt
import pandas as pd

packets=PcapReader('/home/Desktop/tcp11.pcap')

count11=0

ind=0
lala=[]
for packet in packets:
    # print(packet.summary())
    newdict={}
    
    # print()
    # print(packet.src)
    # print(packet.dst)
    try:
        newdict['Src']=packet['IP'].src
        newdict['Dst']=packet['IP'].dst
        newdict['Sport']=packet['TCP'].sport
        newdict['Dport']=packet['TCP'].dport
        newdict['Time']=packet.time
        newdict['Seq No.']=packet['TCP'].seq
        lala.append(newdict)
    except:
        print('Failed')
        # pass
    # break

df1=pd.DataFrame(lala,columns=['Src','Dst','Sport','Dport','Time','Seq No.'])
print('hello')
# df1


#     if packet['IP'].src==f'192.168.0.{key}':
#         lala.append(packet.time)

# create stevens graph, hist of seq numbers

df22=df1[df1['Src']==f'192.168.0.2']     
# df22=df1
print(len(df22))
stev1=df22['Seq No.'].values
time1=df22['Time'].values
plt.figure(figsize=(20,10))
plt.plot(time1,stev1,marker='x',linestyle='None')

alla1=df1['Seq No.'].values
c,be,_=plt.hist(alla1,bins=500)

# generate pps traces
df2=df1
lala3A=df2['Time'].values
lala2A=[a-lala3A[0] for a in lala3A]
plt.figure()
# plt.hist(lala3A,bins=[a for a in range(0,31,1)],edgecolor='black')
plt.hist(lala2A,bins=[a for a in range(0,31,1)],edgecolor='black')
plt.title(f'I/O, pps')
plt.xlabel('Elapsed time since first packet capture')
