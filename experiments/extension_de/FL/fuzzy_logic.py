#
# Fuzzy Logic ALgorithm
# Developed by Jesus Cardenes
#

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import time

class fl_class:

	def __init__(self):

		#Crisp values are the entries to the system
		# cpu 0 to 100
		cpu= np.arange(0,101,1)
		# memory 0 to 100
		memory= np.arange(0,101,1)
		# variability_memory 0 to 100
		variability_memory= np.arange(0,101,1)
		# connections 0 - ? 
		connections=np.arange(0,1001,1)
		# latency 0 - ?
		latency= np.arange(0,101,1)
		# status 200 or 500
		status=np.arange(199,600,1)

		# Feedback loop
		# servers one - two
		servers=np.arange(1,3,0.0001)
		# Ram 100 to 400 M 
		ram=np.arange(100,351,1)

		#The membership function defines the correspondency between the crisp values and the fuzzy value

		fig, (ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(nrows=8, figsize=(8,9))

		#Fuzzy set are the fuzzy values 
		# cpu low-usage, medium-usage, high-usage
		cpu_antecedent=ctrl.Antecedent(cpu, 'cpu_antecedent' )
		cpu_antecedent['cpu_lo']=cpu_lo=fuzz.trimf(cpu,[0,0,33])
		cpu_antecedent['cpu_md']=cpu_md=fuzz.trimf(cpu,[0,50,100])
		cpu_antecedent['cpu_hi']=cpu_hi=fuzz.trimf(cpu,[33,100,100])

		ax0.plot(cpu, cpu_lo, 'b', linewidth=1.5, label= "Low")
		ax0.plot(cpu, cpu_md, 'g', linewidth=1.5, label= "Medium")
		ax0.plot(cpu, cpu_hi, 'r', linewidth=1.5, label= "High")
		ax0.set_title(' % CPU ')
		ax0.legend()

		# memory low-usage, medium-usage, high-usage, too-high-usage
		memory_antecedent=ctrl.Antecedent(memory, 'memory_antecedent' )
		memory_antecedent['memory_lo']=memory_lo=fuzz.trimf(memory,[0,0,50])
		memory_antecedent['memory_md']=memory_md=fuzz.trimf(memory,[0,50,100])
		memory_antecedent['memory_hi']=memory_hi=fuzz.trimf(memory,[33,100,100])

		ax1.plot(memory, memory_lo, 'b', linewidth=1.5, label= "Low")
		ax1.plot(memory, memory_md, 'g', linewidth=1.5, label= "Medium")
		ax1.plot(memory, memory_hi, 'r', linewidth=1.5, label= "High")
		ax1.set_title(' % Memory ')
		ax1.legend()

		# variability-memory low, high
		variability_memory_antecedent=ctrl.Antecedent(variability_memory, 'variability_memory_antecedent' )
		variability_memory_antecedent['variability_memory_lo']=variability_memory_lo=fuzz.trimf(variability_memory,[0,5,33])
		variability_memory_antecedent['variability_memory_hi']=variability_memory_hi=fuzz.trimf(variability_memory,[33,100,100])

		ax2.plot(variability_memory, variability_memory_lo, 'b', linewidth=1.5, label= "Low")
		ax2.plot(variability_memory, variability_memory_hi, 'g', linewidth=1.5, label= "High")
		ax2.set_title(' Variability-Memory ')
		ax2.legend()

		# connections low-connections, medium-connections, high-connections, very-high-connections
		connections_antecedent=ctrl.Antecedent(connections, 'connections_antecedent' )
		connections_antecedent['connections_lo']=connections_lo=fuzz.trimf(connections,[0,0,20])
		connections_antecedent['connections_md']=connections_md=fuzz.trimf(connections,[20,100,200])
		connections_antecedent['connections_hi']=connections_hi=fuzz.trimf(connections,[200,275,350])
		connections_antecedent['connections_vhi']=connections_vhi=fuzz.trimf(connections,[350,1000,1000])

		ax3.plot(connections, connections_lo, 'b', linewidth=1.5, label= "Low")
		ax3.plot(connections, connections_md, 'g', linewidth=1.5, label= "Medium")
		ax3.plot(connections, connections_hi, 'r', linewidth=1.5, label= "High")
		ax3.plot(connections, connections_vhi, 'c', linewidth=1.5, label= "Very-High")
		ax3.set_title(' Connections ')
		ax3.legend()

		# latency good, okay, bad, very-bad
		latency_antecedent=ctrl.Antecedent(latency, 'latency_antecedent' )
		latency_antecedent['latency_g']=latency_g=fuzz.trimf(latency,[0,0,1])
		latency_antecedent['latency_o']=latency_o=fuzz.trimf(latency,[1,2,3])
		latency_antecedent['latency_b']=latency_b=fuzz.trimf(latency,[3,4,5])
		latency_antecedent['latency_vb']=latency_vb=fuzz.trapmf(latency,[5,5,100,100]) #Square

		ax4.plot(latency, latency_g, 'b', linewidth=1.5, label= "Good")
		ax4.plot(latency, latency_o, 'g', linewidth=1.5, label= "Okay")
		ax4.plot(latency, latency_b, 'r', linewidth=1.5, label= "Bad")
		ax4.plot(latency, latency_vb, 'c', linewidth=1.5, label= "Very-Bad")
		ax4.set_title(' Latency ')
		ax4.legend()

		# status good - bad
		status_antecedent=ctrl.Antecedent(status, 'status_antecedent' )
		status_antecedent['status_g']=status_g=fuzz.trapmf(status,[200,200,210,210])
		status_antecedent['status_b']=status_b=fuzz.trapmf(status,[500,500,510,510])

		ax5.plot(status, status_g, 'b', linewidth=1.5, label= "Good")
		ax5.plot(status, status_b, 'g', linewidth=1.5, label= "Bad")
		ax5.set_title(' Status')
		ax5.legend()

		# Feedback loop
		# servers one - two
		servers_antecedent=ctrl.Antecedent(servers, 'servers_antecedent' )
		servers_antecedent['servers_1']=servers_1=fuzz.trapmf(servers,[1,1,1.001,1.001])
		servers_antecedent['servers_2']=servers_2=fuzz.trapmf(servers,[2,2,2.001,2.001]) #Square

		ax6.plot(servers, servers_1, 'b', linewidth=1.5, label= "1 Server")
		ax6.plot(servers, servers_2, 'g', linewidth=1.5, label= "2 Server")
		ax6.set_title(' Servers ')
		ax6.legend()

		self.servers_consequent=ctrl.Consequent(servers, 'servers_consequent' )
		self.servers_consequent['servers_1']=servers_1
		self.servers_consequent['servers_2']=servers_2


		# Ram low, medium,  high 
		ram_antecedent=ctrl.Antecedent(ram, 'ram_antecedent' )
		ram_antecedent['ram_lo']=ram_lo=fuzz.trimf(ram,[99,150,200])
		ram_antecedent['ram_md']=ram_md=fuzz.trimf(ram,[200,250,300])
		ram_antecedent['ram_hi']=ram_hi=fuzz.trimf(ram,[300,350,400])

		self.ram_consequent=ctrl.Consequent(ram, 'ram_consequent' )
		self.ram_consequent['ram_lo']=ram_lo
		self.ram_consequent['ram_md']=ram_md
		self.ram_consequent['ram_hi']=ram_hi

		ax7.plot(ram, ram_lo, 'b', linewidth=1.5, label= "Low")
		ax7.plot(ram, ram_md, 'g', linewidth=1.5, label= "Medium")
		ax7.plot(ram, ram_hi, 'r', linewidth=1.5, label= "High")
		ax7.set_title(' RAM ')
		ax7.legend()

		import time
		for ax in (ax0,ax1,ax2,ax3,ax4,ax5,ax6,ax7):

			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
			ax.get_xaxis().tick_bottom()
			ax.get_yaxis().tick_left()


		plt.tight_layout()
		#plt.show()
		#Consequences
		# How many resources should we allocate
		# servers 1 or 2
		# RAM 100 to 300m
		# These values should be also given back as a feedback loop



		#Fuzzy control system are the rules that will consider the fuzzy values and take actions 
		#Mamdami multi-input and multi-output system
		#Based on the test done we can constraint the space

		# IF the memory's low-usage,   latengy good, status good, servers 1, ram medium then RAM LOW 
	

		rule1r= ctrl.Rule(memory_antecedent['memory_hi'] & ram_antecedent['ram_lo'] , self.ram_consequent['ram_md'])

		rule2r= ctrl.Rule(memory_antecedent['memory_hi'] & (ram_antecedent['ram_md'] | ram_antecedent['ram_hi']), self.ram_consequent['ram_hi'])

		rule1s= ctrl.Rule(memory_antecedent['memory_hi'] & ram_antecedent['ram_hi'] & servers_antecedent['servers_1'], self.servers_consequent['servers_2'])

		rule3r= ctrl.Rule(memory_antecedent['memory_lo'] & ram_antecedent['ram_hi'], self.ram_consequent['ram_md'])

		rule4r= ctrl.Rule(memory_antecedent['memory_lo'] & (ram_antecedent['ram_md'] | ram_antecedent['ram_lo']), self.ram_consequent['ram_lo'])
		#I added an OR with memory medium as when memory as it should down scale the number of servers
		#rule2s= ctrl.Rule((memory_antecedent['memory_lo'] | memory_antecedent['memory_md']) & ram_antecedent['ram_lo'] & servers_antecedent['servers_2'], self.servers_consequent['servers_1'])	


		rule2s= ctrl.Rule((memory_antecedent['memory_lo'] | memory_antecedent['memory_md']) & ram_antecedent['ram_lo'] & ~ ram_antecedent['ram_hi'] & ~ ram_antecedent['ram_md'] & servers_antecedent['servers_2'], self.servers_consequent['servers_1'])	
		

	############################ COMMENTS ######################
	#	#ORDER OF MAGNITUD OF THE PROBLEM BASED ON Fuzzy set, number of possible combinations.
	#
	#	#By applyng the Rule of Product: 
	#
	#	# CPU(3) x Memory(4) x Variability-Memory(2) x Connections(4) x Latency(4) x Status(2) x #Servers(2) x RAM(3)= 4608 !!!! Way too much to do it by hand :S -> No worries RL will rescue us
	#
	#	#However I will have to fix the membership function because otherwise things will get #nasty
	#	#Also the real space is not that big as there are only 5 possible actions
	############################################################

		self.scalability_ram_ctrl=ctrl.ControlSystem([rule1r,rule2r,rule3r,rule4r])	

		self.scalability_server_ctrl=ctrl.ControlSystem([rule1s,rule2s])	


	##################### Scalability Controller ###############

	def fl_ctrl(self,cpu1, memory1, cpu2, memory2,connections1, connections2, latency, status, servers_on, ram_state ):
		print("Memory used: "+ str(memory1))
		print("Ram state: " + str(ram_state))
		print("Servers: "+ str(servers_on))
		scalling_ram=ctrl.ControlSystemSimulation(self.scalability_ram_ctrl)
		scalling_server=ctrl.ControlSystemSimulation(self.scalability_server_ctrl)
		scalling_server.input['memory_antecedent']=scalling_ram.input['memory_antecedent']=memory1
		#print(scalling_ram.input['memory_antecedent'])
		#scalling_server.input['latency_antecedent']=scalling_ram.input['latency_antecedent']=latency
		#scalling_server.input['status_antecedent']=scalling_ram.input['status_antecedent']=status
		scalling_server.input['servers_antecedent']=servers_on
		scalling_server.input['ram_antecedent']=scalling_ram.input['ram_antecedent']=ram_state
		try:
			scalling_ram.compute()
			
			print('RAM')
			print(scalling_ram.output['ram_consequent'])

			ram_output=int(scalling_ram.output['ram_consequent'])
			#self.ram_consequent.view(sim=scalling_ram)
			#time.sleep(5)

		except:
			ram_output=0
			print("No RAM changes.")

		try:
			scalling_server.compute()
			print('Servers')
			print(scalling_server.output['servers_consequent'])
			server_output=int(scalling_server.output['servers_consequent'])
			#self.servers_consequent.view(sim=scalling_server)
			#time.sleep(5)

		except:
			server_output=0
			print("No number of SERVERS changes.")

		return ram_output, server_output

#if __name__ == "__main__":

#	controller=fl_class()
#	ram_output, server_output=controller.fl_ctrl()

#	print("Output")
#	print(ram_output, server_output)
 
