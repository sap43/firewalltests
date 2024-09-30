import datetime,time
from datetime import timedelta
from flask import Flask
import json
import subprocess
import multiprocessing

ip1='0.0.0.0'
port1=53221

app = Flask(__name__)


@app.before_request
def flr2():
    #app.logger.info('URLHIT{} {} '.format(request.remote_addr,request.url))
    rt=datetime.datetime.now()
    print(f'Request received {rt}')
#    print(request.remote_addr,request.url)

q1=multiprocessing.Queue()

@app.route('/look2/<durr12>/<ports12>',methods=['GET'])
def fl5(durr12,ports12):
	global proc23,proc24,file11
	# with open('top.txt','w') as file11:
	# 	file11.write(f'{durr12,ports12}\n')
	# 	proc23=subprocess.Popen(['top','-b','-d','1'],stdout=file11)

	file11=open('top.txt','w')
	# print('AA')
	file11.write(f'{durr12},{ports12}\n')
	# print('AA2')
	file11.flush()
	proc23=subprocess.Popen(['top','-b','-d','1'],stdout=file11)
	# print('AA3')

	# proc24=subprocess.Popen(['sudo', 'tcpdump', '-n', '-vvv', '-i', 'any', 'tcp', 'port', '53221', 'or', 'port', '53222', 'and', 'host', '192.168.0.108', '-w', 'tcpdump.pcap'],stdout=subprocess.PIPE)
	proc24=subprocess.Popen(['sudo', 'tcpdump', '-n', '-vvv', '-i', 'any', 'tcp', 'port', '53221', 'or', 'port', '53222', 'and', 'host', '192.168.0.108', '-w', 'tcpdump.pcap'],stderr=subprocess.PIPE,text=True)

	print('VOKAY')
	# time.sleep(1)
	proc25.start()
		
	return('Started top')


def floo1(q1):
	global proc24
	# try:
	for line in proc24.stderr:
		try:
			packre1=int(line[4:-1])
			q1.put(packre1)
			print(f'R{packre1}R')
		except:
			pass
	# except:
	# 	break
proc25=multiprocessing.Process(target=floo1,args=(q1,))

@app.route('/look3/<ab1>/<ab2>/<ab3>/<ab4>/<ab5>/<ab6>',methods=['GET'])
def fl6(ab1,ab2,ab3,ab4,ab5,ab6):
	global proc23,proc24,file11,proc25
	proc23.terminate()
	proc24.terminate()
	proc25.terminate()
	while not q1.empty():
		packre2=q1.get()
	file11.write(f'\nENDEXP{ab1},{ab2},{ab3},{ab4},{ab5},{ab6},{packre2}\n')
	file11.close()
	print('ALL DONE OK')
	# stdo,stde=proc24.communicate()
	# print(stde,stdo)
	return('Stopped')

@app.route('/look1',methods=['GET'])
def fl3():

	aa=datetime.datetime.now()
#print(a)
#	time.sleep(5)
	bb=datetime.datetime.now()
	print(bb-aa)
	cc=bb-aa
#	bala1.append(cc)
	mean1=cc
	return json.dumps(f'{mean1}')

#app.run(ssl_context='adhoc',port=port1)
app.run(host=ip1,port=port1)
