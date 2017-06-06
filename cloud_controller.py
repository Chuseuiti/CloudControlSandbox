## Script Developed by:
#
# Jesus Alejandro Cardenes 
#

#Cloud Controller

import docker
import time
import os
import re
import requests
import sys

sys.path.insert(0,'central_unit/')

from fuzzy_logic_rl import fl_class

global server1, server2, servers_on, ram_state



server1=0
server2=0

servers_on=1
ram_state=100

def init_container():

	global server1, server2, client_lowlevel
	
	#Init Docker clients
	client=docker.from_env()
	client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')

	## Servers ##
	#Init 1st Rubis container with CPU and RAM limit (/bin/bash ensure that the container is not closed on start)
	server1 = client.containers.run("chuseuiti/rubos","/bin/bash -c 'service apache2 start; vi /bin/bash'", detach=True, cpuset_cpus=("0"), mem_limit=("100m"), name="server1") 

	#Init 2st Rubis container with CPU and RAM limit but stop server
	server2 = client.containers.run("chuseuiti/rubos","/bin/bash -c 'service apache2 stop; vi /bin/bash '", detach=True, cpuset_cpus=("0"), mem_limit=("100m"), name="server2")


	## Load Balancer ##
	
	os.system('sudo docker run --memory=500m --cpus=1 -d -p 80:80 --link server1:server1 --link server2:server2 tutum/haproxy')


	

## Monitoring 
def monitor(algorithm_controller):
	global server1, server2, client_lowlevel,ram_state, servers_on
	num=0
	cpu1=cpu2=0
	memory1=memory2=0
	
	f=open("simulation_results/server.csv","a")
	time.sleep(2) #Gives time for servers to settle down
	while 1:
		try:

			print "Monitoring Stats"
			client1_stats=client_lowlevel.stats(container="server1",decode=True, stream=False)
			client2_stats=client_lowlevel.stats(container="server2",decode=True, stream=False)

			if num==1:

				cpuDelta1=client1_stats[u'cpu_stats'][u'cpu_usage'][u'total_usage']-pre1[u'cpu_stats'][u'cpu_usage'][u'total_usage']
				systemDelta1=client1_stats[u'cpu_stats'][u'system_cpu_usage']-pre1[u'cpu_stats'][u'system_cpu_usage']
				cpu1=( (float(cpuDelta1)/float(systemDelta1))*float(len(client1_stats[u'cpu_stats'][u'cpu_usage'][u'percpu_usage']))*100)

				####################

				cpuDelta2=client2_stats[u'cpu_stats'][u'cpu_usage'][u'total_usage']-pre2[u'cpu_stats'][u'cpu_usage'][u'total_usage']
				systemDelta2=client2_stats[u'cpu_stats'][u'system_cpu_usage']-pre2[u'cpu_stats'][u'system_cpu_usage']
				cpu2= (float(cpuDelta2)/float(systemDelta2))*float(len(client2_stats[u'cpu_stats'][u'cpu_usage'][u'percpu_usage']))*100

			pre1=client1_stats 

			memory1=( float(float(client1_stats[u'memory_stats'][u'usage'])/float(client1_stats[u'memory_stats'][u'limit']))*100)

			####################

			pre2=client2_stats

			memory2= float(float(client2_stats[u'memory_stats'][u'usage'])/float(client2_stats[u'memory_stats'][u'limit']))*100

			num=1
			# Get latency from the client side
			start=time.time()
			resp=requests.get("http://localhost/PHP/index.html")
			status=resp.status_code
			end=time.time()
			latency=end-start
		
			# Get latency from the system side -> Time to serve the website and it does not take into account the TCP connection time neither the time to pass the data of the website - I can take a look to the username and get only the reference of my client request
			# Serve Page Time is the last Parameter %T seconds and %D microseconds
			# LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" **%T/%D**" combined
			# To obtain the last line is needed to write and parse this line
			s=os.popen('sudo docker exec server1 tail --lines=1 /var/log/apache2/access.log').read()
			
			try:
				microseconds1=re.search("(\d+)\/(\d+)",s).group(2)
	

			except:
				microseconds1=0


			s= os.popen('sudo docker exec server2 tail --lines=1 /var/log/apache2/access.log').read()

			try:
				microseconds2=re.search("(\d+)\/(\d+)",s).group(2)
	

			except:
				microseconds2=0


			# Connections to the containers
			values1= os.popen("sudo docker exec server1 netstat -tn 2>/dev/null | grep :80 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head").read().lstrip().split()
			values2= os.popen("sudo docker exec server2 netstat -tn 2>/dev/null | grep :80 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head").read().lstrip().split()
			out_time=time.time()

			#Call to the Algorithm
			if len(values1)==2 and len(values2)==2:
		
				f.write(str(out_time)+","+str(cpu1)+","+str(memory1)+","+str(cpu2)+","+str(memory2)+","+str(int(values1[0]))+","+str(values1[1])+","+str(int(values2[0]))+","+str(values2[1])+","+str(int(microseconds1))+","+str(microseconds2)+","+str(latency)+","+str(status)+","+str(ram_state)+","+str(servers_on)+" \n ")
				f.flush()
				ram_ouput, servers_output=algorithm_controller.fl_ctrl(cpu1, memory1, cpu2, memory2,values1[0], values2[0], latency, status, servers_on, ram_state )
			elif len(values1)==2 and len(values2)!=2:
				f.write(str(out_time)+","+str(cpu1)+","+str(memory1)+","+str(cpu2)+","+str(memory2)+","+str(int(values1[0]))+","+str(values1[1])+","+str(0)+","+str(0)+","+str(int(microseconds1))+","+str(microseconds2)+","+str(latency)+","+str(status)+","+str(ram_state)+","+str(servers_on)+" \n ")
				f.flush()
				ram_ouput, servers_output=algorithm_controller.fl_ctrl(cpu1, memory1, cpu2, memory2,values1[0], 0, latency, status, servers_on, ram_state )		
			elif len(values1)!=2 and len(values2)==2:
				f.write(str(out_time)+","+str(cpu1)+","+str(memory1)+","+str(cpu2)+","+str(memory2)+","+str(0)+","+str(0)+","+str(int(values2[0]))+","+str(values2[1])+","+str(int(microseconds1))+","+str(microseconds2)+","+str(latency)+","+str(status)+","+str(ram_state)+","+str(servers_on)+" \n ")
				f.flush()
				ram_ouput, servers_output=algorithm_controller.fl_ctrl(cpu1, memory1, cpu2, memory2,0, values2[0], latency, status, servers_on, ram_state )
			else:
				f.write(str(out_time)+","+str(cpu1)+","+str(memory1)+","+str(cpu2)+","+str(memory2)+","+str(0)+","+str(0)+","+str(0)+","+str(0)+","+str(int(microseconds1))+","+str(microseconds2)+","+str(latency)+","+str(status)+","+str(ram_state)+","+str(servers_on)+" \n ")
				f.flush()
				ram_ouput, servers_output=algorithm_controller.fl_ctrl(cpu1, memory1, cpu2, memory2,0, 0, latency, status, servers_on, ram_state )

			controller(ram_ouput, servers_output)

		except:
			print("Exception Connection")

## Controller 

def controller(ram, servers ):
	
	global server1, server2, servers_on, ram_state
	#Logic
	if servers!=0:
		if servers==2:
			try:
				server2.exec_run("service apache2 start")
				servers_on=2
			except:
				print("Crash2 start")
		elif servers==1:
			try:
				server2.exec_run("service apache2 stop")
				servers_on=1
			except:
				print("Crash2 stop")			
	#Update container limits
	if ram!=0:
		try:
			server1.update(mem_limit=(str(ram)+"m"))
			server2.update(mem_limit=(str(ram)+"m"))
			ram_state=ram
		except:
			print("Ram Update Crash")


def main_function():


	os.system("sudo docker stop $(sudo docker ps -a -q)")
	os.system("sudo docker rm $(sudo docker ps -a -q) ")
	#Init Limited Rubbos Container
	container=init_container();

	#Start Httpmon - Streaming of Rubis application
	algorithm_controller=fl_class()
	#Start Monitoring
	monitor(algorithm_controller)
	

if __name__ == "__main__":

	main_function()
