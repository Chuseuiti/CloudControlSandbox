#
# Fuzzy Logic ALgorithm
# Developed by Jesus Cardenes
#

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import time
from random import *

file=open("rewards.csv","a",0)
file_fuzzy=open("fuzzyevolution.csv","a",0)

class fl_class:

	def __init__(self):
		self.state_mod=0
		self.increase=0
		self.increase_state0=0
		self.variability=0
		self.file_q_table=open("qtable.txt",'a')
		self.last_action=[[[],[],[]],[]]
		self.last_trigger=(0,0, 0, 0, 0)
		self.step=0
		#self.reward=[0,0]
		self.reward=0
		self.q=[[],[],[]]
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
		ram=np.arange(100,400,1)

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
		self.memory_antecedent=ctrl.Antecedent(memory, 'memory_antecedent' )
		self.memory_antecedent['memory_lo']=memory_lo=fuzz.trimf(memory,[0,0,50])
		self.memory_antecedent['memory_md']=memory_md=fuzz.trimf(memory,[0,70,100])
		self.memory_antecedent['memory_hi']=memory_hi=fuzz.trimf(memory,[50,100,100])#33 ans self.increase was not there

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
		self.servers_antecedent=ctrl.Antecedent(servers, 'servers_antecedent' )
		self.servers_antecedent['servers_1']=servers_1=fuzz.trapmf(servers,[1,1,1.001,1.001])
		self.servers_antecedent['servers_2']=servers_2=fuzz.trapmf(servers,[2,2,2.001,2.001]) #Square

		ax6.plot(servers, servers_1, 'b', linewidth=1.5, label= "1 Server")
		ax6.plot(servers, servers_2, 'g', linewidth=1.5, label= "2 Server")
		ax6.set_title(' Servers ')
		ax6.legend()

		self.servers_consequent=ctrl.Consequent(servers, 'servers_consequent' )
		self.servers_consequent['servers_1']=servers_1
		self.servers_consequent['servers_2']=servers_2


		# Ram low, medium,  high 
		ram_antecedent=ctrl.Antecedent(ram, 'ram_antecedent' )
		self.array_ram_lo=[99,150,200]
		self.array_ram_med=[200,250,300]
		self.array_ram_hi=[300,350,400]
		ram_antecedent['ram_lo']=ram_lo=fuzz.trimf(ram,self.array_ram_lo)
		ram_antecedent['ram_md']=ram_md=fuzz.trimf(ram,self.array_ram_med)
		ram_antecedent['ram_hi']=ram_hi=fuzz.trimf(ram,self.array_ram_hi)

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
	

		self.rule1r= ctrl.Rule(self.memory_antecedent['memory_hi'] & ram_antecedent['ram_lo'] , self.ram_consequent['ram_md'])

		self.rule2r= ctrl.Rule(self.memory_antecedent['memory_hi'] & (ram_antecedent['ram_md'] | ram_antecedent['ram_hi']) , self.ram_consequent['ram_hi'])

		self.rule1s= ctrl.Rule(self.memory_antecedent['memory_hi'] & ram_antecedent['ram_hi'] & self.servers_antecedent['servers_1'], self.servers_consequent['servers_2'])

		self.rule3r= ctrl.Rule(self.memory_antecedent['memory_lo'] & ram_antecedent['ram_hi'], self.ram_consequent['ram_md'])

		self.rule4r= ctrl.Rule(self.memory_antecedent['memory_lo'] & (ram_antecedent['ram_md'] | ram_antecedent['ram_lo']), self.ram_consequent['ram_lo'])

		self.rule2s= ctrl.Rule((self.memory_antecedent['memory_lo'] | self.memory_antecedent['memory_md']) & ram_antecedent['ram_lo'] & ~ ram_antecedent['ram_hi'] & ~ ram_antecedent['ram_md'] & self.servers_antecedent['servers_2'], self.servers_consequent['servers_1'])	


		

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

		self.scalability_ram_ctrl=ctrl.ControlSystem([self.rule1r,self.rule2r,self.rule3r,self.rule4r])	

		self.scalability_server_ctrl=ctrl.ControlSystem([self.rule1s,self.rule2s])	

	def adjustment_ctrl(self,new_state,status,latency,servers, ram,memory):
		ram_state=int(ram)
		print("RAM STATE (ram):" + str(ram_state))
		#The reward calculation is based on scoring the previous action with the reward of the new state, also I should take into consideration all the moments that there is no new regard to add then to the reward
		print("Reinforcement Learning Fine Tunning")
		if self.step==0:
			#Copy previous value of self not the pointer!!!!
			self.last_action=[[[self.array_ram_lo],[self.array_ram_med],[self.array_ram_hi]],new_state]	
			print(self.last_action)
			self.step+=1		
		else:

			print(self.last_action)
			
			#Reward Calculus
			value_reward=0
			#I have to consider also minimum RAM and CPU allocated gives maximum reward 
			if status>=500:
				value_reward-=status
			elif status>=200 and status <300:
				value_reward+=200
			value_reward+=(-ram+400)*2#None
			value_reward+=(100 if servers == 1 else 0)
			value_reward+=int(-(latency*10)+200)
			temp=(300 - np.abs(70-memory)*(30 if memory>70 else 30))
			ref=((memory-70)/20 if memory>70 else (memory-70)/50)#50
			value_reward+=temp
			self.reward=value_reward #+randint(-25,25)#Adding to reward for testing proposes
			print("################")
			file.write(str(status)+","+str((-ram+400)*4)+","+str((100 if servers == 1 else 0))+","+str(int(-latency+200))+","+str(self.reward)+"\n")
			print("RAM Value:" + str(ram))
			print("Reward RAM: "+str((-ram+400)*4))
			print("Reward Latency: "+str(int(-latency+200)))
			print("Reward Memory: "+str(300 - (np.abs(70-memory)*(30 if memory>70 else 4)) ))
			print("################")

			self.step+=1

			if 1:#self.step==2:

				#self.step=0

				#State is a number from 0 to 2 referencing to the possible action taken
				#Instead of taking into consideration the rule, I take into consideration the action every time that is performed as each action should be possible  


				#Aggregation of overall reward after action
				#rewards=np.median(self.reward)
				rewards=self.reward

				#Action
				array_parameters_actions=self.last_action[0]
				state=self.last_action[1]
				action=[array_parameters_actions[state],servers]
				#Look for used action
				actions_table=[e[0] == action for e in self.q[state]]
				actions_table_1=[e[0] == [array_parameters_actions[1],servers] for e in self.q[1]]
				actions_table_0=[e[0] == [array_parameters_actions[0],servers] for e in self.q[0]]
				actions_table_2=[e[0] == [array_parameters_actions[2],servers] for e in self.q[2]]
				if any(actions_table):
					#Update reward
					self.q[state][actions_table.index(True)][1]=np.median([self.q[state][actions_table.index(True)][1],rewards])
				else:
					#Create new state with new reward
					#print("Table")
					#print(self.q[state])	
					(self.q[state]).append([action,rewards])
			
				if self.increase>=10:
					if any(actions_table_1):
						#Update reward
						self.q[1][actions_table_1.index(True)][1]=np.median([self.q[1][actions_table_1.index(True)][1],rewards])
					else:
						#Create new state with new reward
						#print("Table")
						#print(self.q[state])	
						(self.q[1]).append([[array_parameters_actions[1],servers],rewards])

				if self.increase_state0>=10:
					if any(actions_table_0):
						#Update reward
						self.q[0][actions_table_0.index(True)][1]=np.median([self.q[0][actions_table_0.index(True)][1],rewards])
					else:
						#Create new state with new reward
						#print("Table")
						#print(self.q[state])	
						(self.q[0]).append([[array_parameters_actions[0],servers],rewards])

					if any(actions_table_2):
						#Update reward
						self.q[2][actions_table_2.index(True)][1]=np.median([self.q[2][actions_table_2.index(True)][1],rewards])
					else:
						#Create new state with new reward
						#print("Table")
						#print(self.q[state])	
						(self.q[2]).append([[array_parameters_actions[2],servers],rewards])

				print("Previous State Comprobation: "+ str(state))
				#Based on overrall performance on the Q table pick the best seed and update the system
				position_reward=-1
				#For loop best performance
				factor=1.2
				state_base=int(state)
				#state=0
				if state==0:
					self.increase+=1
					self.increase_state0=0
					print("Update State 0")
					if len(self.q[state])<3 :
						print("IN-RANDOM 5" if (len(self.q[state]) % 5==0) else "" )
						print("Random Search")
						if new_state!=4:
							self.array_ram_lo=[99,150+randint(-50,50),200]
						else:
							print("Random Search on Neutral")
							self.array_ram_hi=[100,150+randint(-45,45),200]	
					else:
						print("Random Optimizer based on Reward")

						highest_reward=0
						position_reward=0
						for enum,rew_state in enumerate(self.q[state]):
							if enum==0:
								highest_reward=rew_state[1]*(enum/len(self.q[state]) if enum>15 else 1)

							else:
								if highest_reward<rew_state[1]:
									highest_reward=rew_state[1]*(enum/len(self.q[state]) if enum>15 else 1)
									position_reward=enum
						if (self.step % 100!=0):
							#discount=(1 if float(len(self.q[state]))/float(factor)<=1 else float(len(self.q[state]))/float(factor))

							#if new_state!=4:
							#State Modify 
							#self.array_ram_lo=[self.q[state][position_reward][0][0][0][0]+randint(int(-10)+int(50*ref),int(10)+int(50*ref)),self.q[state][position_reward][0][0][0][1]+(50*ref),self.q[state][position_reward][0][0][0][2]+int(50*ref)]
							self.array_ram_lo=[self.q[state][position_reward][0][0][0][0],self.q[state][position_reward][0][0][0][1]+randint(int(-10)+int(50*ref),int(10)+int(50*ref)),self.q[state][position_reward][0][0][0][2]]

							if self.increase>10:
								#print("Decreasing")
								#print(len(self.q[1]))
								#print(self.q[1])
								for enum,rew_state in enumerate(self.q[1]):
									if enum==0:
										highest_reward=rew_state[1]*(enum/len(self.q[1]) if enum>15 else 1) #Memory lose
										position_reward=0

									else:
										#print(rew_state[1])
										if highest_reward<rew_state[1]:
											highest_reward=rew_state[1]*(enum/len(self.q[1]) if enum>15 else 1)  # Memory lose
											position_reward=enum
								#print(self.q[1][position_reward][0][0][0][0])
								self.array_ram_med=[self.q[1][position_reward][0][0][0][0],self.q[1][position_reward][0][0][0][1]+randint(-10+int(50*ref),10+int(50*ref)),self.q[1][position_reward][0][0][0][2]]
						
						
							
						
				#state=1		
				elif state==1:
					self.increase=0
					self.increase_state0+=1
					print("Update State 1")
					if len(self.q[state])<3:
						print("IN-RANDOM 5" if (len(self.q[state]) % 5==0) else "" )
						print("Random Search")
						if new_state!=4:
							self.array_ram_med=[200,250+randint(-50,50),300]
						else:
							print("Random Search on Neutral")
							self.array_ram_hi=[200,250+randint(-45,45),300]	
					else:
						print("///////////////")
						print("Random Optimizer based on Reward 1")
						highest_reward=0
						position_reward=0

						print("Reward")
						for enum,rew_state in enumerate(self.q[state]):
							if enum==0:
								highest_reward=rew_state[1]*(enum/len(self.q[state]) if enum>15 else 1) #Memory lose

							else:
								#print(rew_state[1])
								if highest_reward<rew_state[1]:
									highest_reward=rew_state[1]*(enum/len(self.q[state]) if enum>15 else 1)  # Memory lose
									position_reward=enum
						print(highest_reward)
						#if (self.step % 100!=0):
							#discount= (1 if float(len(self.q[state]))/float(factor)<=1 else float(len(self.q[state]))/float(factor))
							#if new_state!=4:
						print("Random Add: "+ str(ref))
						print(randint(int(-10)+int(50*ref),int(10)+int(50*ref)))
						#if new_state==2:
						#	ref=-ref
						if self.increase_state0>13 and self.increase_state0 % 3==1:
							self.array_ram_med=[self.q[state][position_reward][0][0][0][0],self.q[state][position_reward][0][0][0][1]+randint(int(-10)+int(50*ref),int(10)+int(50*ref)),self.q[state][position_reward][0][0][0][2]]

						else:
							self.array_ram_med=[self.q[state][position_reward][0][0][0][0],self.q[state][position_reward][0][0][0][1]+randint(0,int(100)),self.q[state][position_reward][0][0][0][2]]

						if self.increase_state0>10:
								print("Decreasing")
								for enum,rew_state in enumerate(self.q[0]):
									if enum==0:
										highest_reward=rew_state[1]*(enum/len(self.q[0]) if enum>15 else 1) #Memory lose
										position_reward=0

									else:

										if highest_reward<rew_state[1]:
											highest_reward=rew_state[1]*(enum/len(self.q[0]) if enum>15 else 1)  # Memory lose
											position_reward=enum

								self.array_ram_lo=[self.q[0][position_reward][0][0][0][0],self.q[0][position_reward][0][0][0][1]+randint(-10+int(50*ref),10+int(50*ref)),self.q[0][position_reward][0][0][0][2]]

								for enum,rew_state in enumerate(self.q[2]):
									if enum==0:
										highest_reward=rew_state[1]*(enum/len(self.q[2]) if enum>15 else 1) #Memory lose
										position_reward=0

									else:

										if highest_reward<rew_state[1]:
											highest_reward=rew_state[1]*(enum/len(self.q[2]) if enum>15 else 1)  # Memory lose
											position_reward=enum

								self.array_ram_hi=[self.q[2][position_reward][0][0][0][0],self.q[2][position_reward][0][0][0][1]+randint(-10+int(50*ref),10+int(50*ref)),self.q[2][position_reward][0][0][0][2]]

						
							
				
						


				#state=2
				elif state==2:
					print("Update State 2")
					self.increase_state0=0
					if len(self.q[state])<3:
						print("IN-RANDOM 5" if (len(self.q[state]) % 5==0) else "" )
						print("Random Search")
						if new_state!=4:
							self.array_ram_hi=[300,350+randint(-50,50),400]	
						else:
							print("Random Search on Neutral")
							self.array_ram_hi=[300,350+randint(-45,45),400]	
					else:
						print("Random Optimizer based on Reward")
						highest_reward=0
						position_reward=0
						self.increase+=1
						for enum,rew_state in enumerate(self.q[state]):
							if enum==0:
								highest_reward=rew_state[1]*(enum/len(self.q[state]) if enum>15 else 1)

							else:
								if highest_reward<rew_state[1]:
									highest_reward=rew_state[1]*(enum/len(self.q[state]) if enum>15 else 1)
									position_reward=enum
						if (self.step % 100!=0):
							discount=(1 if float(len(self.q[state]))/float(factor)<=1 else float(len(self.q[state]))/float(factor))
							print("Exploit")
							print(self.q[state][position_reward][0][0][0])
							print(self.q[state][position_reward][0][0][0][0]+randint(int(-50/discount),int(25/discount)))
							
							self.array_ram_hi=[self.q[state][position_reward][0][0][0][0],self.q[state][position_reward][0][0][0][1]+randint(int(-10)+int(50*ref),int(10)+int(50*ref)),self.q[state][position_reward][0][0][0][2]]
						
							if self.increase>10:
								print("Increasing")
								for enum,rew_state in enumerate(self.q[1]):
									if enum==0:
										highest_reward=rew_state[1]*(enum/len(self.q[1]) if enum>15 else 1) #Memory lose
										position_reward=0

									else:

										if highest_reward<rew_state[1]:
											highest_reward=rew_state[1]*(enum/len(self.q[1]) if enum>15 else 1)  # Memory lose
											position_reward=enum

								self.array_ram_med=[self.q[1][position_reward][0][0][0][0],self.q[1][position_reward][0][0][0][1]+randint(-10+int(50*ref),10+int(50*ref)),self.q[1][position_reward][0][0][0][2]]

				#For this first test Im only going to record the results without trying to work around the explore-exploit problem, as first I would like to see if the logic is already working.

				state=int(state_base)
				print("Previous State COmprobation: "+ str(state))
				#print("Q-table")
				#print(self.q)

				self.file_q_table.write('%s \n' % self.q)
				ram=np.arange(100,351,1)
				print("Variability: "+ str(self.variability))
				print("State: "+ str(state)+ ", New State: "+ str(new_state))		


				print("New Parameters Before Rules")
				print(self.array_ram_lo)
				print(self.array_ram_med)
				print(self.array_ram_hi)
				print("##############")



				if self.array_ram_hi[1]>self.array_ram_hi[2]:
					self.array_ram_hi[1]=self.array_ram_hi[2]
				if self.array_ram_hi[0]>self.array_ram_hi[1]:
					self.array_ram_hi[1]=self.array_ram_hi[0]

				if self.array_ram_med[0]>self.array_ram_med[1]:
					self.array_ram_med[1]=self.array_ram_med[0]
				if self.array_ram_med[1]>self.array_ram_med[2]:
					self.array_ram_med[1]=self.array_ram_med[2]
				if self.array_ram_lo[1]>self.array_ram_lo[2]:
					self.array_ram_lo[1]=self.array_ram_lo[2]
				if self.array_ram_lo[0]>self.array_ram_lo[1]:
					self.array_ram_lo[1]=self.array_ram_lo[0]

				print("New Parameters After Rules")
				print(self.array_ram_lo)
				print(self.array_ram_med)
				print(self.array_ram_hi)
				print("##############")
				file_fuzzy.write(str(self.array_ram_lo[0])+","+str(self.array_ram_lo[1])+","+str(self.array_ram_lo[2])+","+str(self.array_ram_med[0])+","+str(self.array_ram_med[1])+","+str(self.array_ram_med[2])+","+str(self.array_ram_hi[0])+","+str(self.array_ram_hi[1])+","+str(self.array_ram_hi[2])+"\n")
				ram_lo=fuzz.trimf(ram,self.array_ram_lo)
				ram_md=fuzz.trimf(ram,self.array_ram_med)
				ram_hi=fuzz.trimf(ram,self.array_ram_hi)
				ram_antecedent=ctrl.Antecedent(ram, 'ram_antecedent' )

				self.ram_consequent=ctrl.Consequent(ram, 'ram_consequent' )
				self.ram_consequent['ram_lo']=ram_antecedent['ram_lo']=ram_lo
				self.ram_consequent['ram_md']=ram_antecedent['ram_md']=ram_md
				self.ram_consequent['ram_hi']=ram_antecedent['ram_hi']=ram_hi
		
				self.rule1r= ctrl.Rule(self.memory_antecedent['memory_hi'] & ram_antecedent['ram_lo'] , self.ram_consequent['ram_md'])

				self.rule2r= ctrl.Rule(self.memory_antecedent['memory_hi'] & (ram_antecedent['ram_md'] | ram_antecedent['ram_hi']), self.ram_consequent['ram_hi'])

			

				self.rule3r= ctrl.Rule(self.memory_antecedent['memory_lo'] & ram_antecedent['ram_hi'], self.ram_consequent['ram_md'])

				self.rule4r= ctrl.Rule(self.memory_antecedent['memory_lo'] & (ram_antecedent['ram_md'] | ram_antecedent['ram_lo']), self.ram_consequent['ram_lo'])

				
	
				#Update system
				self.scalability_ram_ctrl=ctrl.ControlSystem([self.rule1r,self.rule2r,self.rule3r,self.rule4r])

				#### 	SERVER RELATED RULES ####

				self.rule1s= ctrl.Rule(self.memory_antecedent['memory_hi'] & ram_antecedent['ram_hi'] & self.servers_antecedent['servers_1'], self.servers_consequent['servers_2'])

				self.rule2s= ctrl.Rule((self.memory_antecedent['memory_lo'] | self.memory_antecedent['memory_md']) & ram_antecedent['ram_lo'] & ~  ram_antecedent['ram_hi'] & self.servers_antecedent['servers_2'], self.servers_consequent['servers_1'])

				self.scalability_server_ctrl=ctrl.ControlSystem([self.rule1s,self.rule2s])	

				#Updating State for New Iteration
				if new_state !=4:
					self.last_action=[[[self.array_ram_lo],[self.array_ram_med],[self.array_ram_hi]],new_state]
				else:	
					self.last_action=[[[self.array_ram_lo],[self.array_ram_med],[self.array_ram_hi]],self.last_action[1]]
				print("Update action")
				print(self.last_action)

	def adjustment_ctrl_neutral(status, latency, servers_on, memory1):
		current_state_ram=self.last_action[1]
		
		
	def verify_act_states(self, memory, ram_state ):

		#Obtain state to append
		states=[]


		memory_low=[0,0,50]
		memory_medium=[0,70,100]
		memory_high=[50,100,100]

		print('State')
		print(memory)
		print(ram_state)

		if (memory<=memory_high[2] and memory>=memory_high[0] and ram_state>=self.array_ram_lo[0] and ram_state<=self.array_ram_lo[2]) or (memory<=memory_low[2] and memory>=memory_low[0] and ram_state>=self.array_ram_hi[0] and ram_state<=self.array_ram_hi[2]):
			
			states.append(1)	

		elif memory<=memory_high[2] and memory>=memory_high[0] and ((ram_state>=self.array_ram_med[0] and ram_state<=self.array_ram_med[2]) or (ram_state>=self.array_ram_hi[0] and ram_state<=self.array_ram_hi[2])):
		
			states.append(2)
		
		elif memory<=memory_low[2] and memory>=memory_low[0] and ((ram_state>=self.array_ram_med[0] and ram_state<=self.array_ram_med[2]) or (ram_state>=self.array_ram_lo[0] and ram_state<=self.array_ram_lo[2])):
			
			states.append(0)

		#State modfication correction, if increase has not happened yet
		if states[0]==1 and  ram_state>self.array_ram_med[2]:
			if self.state_mod>=5 or self.state_mod % 2 !=1:
				print("correction state")
				states[0]=2
			self.state_mod+=1
		elif states[0]==1 and  ram_state<self.array_ram_med[0]:
			if self.state_mod>=5 or self.state_mod % 2 !=1:
				print("correction state")
				states[0]=0
			self.state_mod+=1
		elif states[0]==2 and  ram_state<self.array_ram_hi[0]:
			if self.state_mod>=5 or self.state_mod % 2 !=1:
				print("correction state")
				states[0]=1
			self.state_mod+=1
		else:
			self.state_mod=0

			

		return states

			

	##################### Scalability Controller ###############

	def fl_ctrl(self,cpu1, memory1, cpu2, memory2,connections1, connections2, latency, status, servers_on, ram_state ):

		#Option 1:  Fine tune RAM
		#Save status as old status
		#Comute reward and assign it to previous status and action taken -> Score the action 
		#Explore more with negative actions and less with positive actions 
		#Explore new RAM thresholds
		act_states=self.verify_act_states(memory1,ram_state)
		print("Estados Activados")
		print(act_states)
		state=0
		if len(act_states)!=0:
			[self.adjustment_ctrl(state,status, latency, servers_on, ram_state,memory1) for state in act_states]
			self.last_trigger=(state,status, latency, servers_on, memory1, ram_state)
			self.variability=0

		else:
			if self.step==1:
				self.variability+=1
				state=4
				self.adjustment_ctrl(state,status, latency, servers_on, ram_state,memory1)
		
		
		print("Memory used: "+ str(memory1))
		print("Ram state: " + str(ram_state))
		print("Servers: "+ str(servers_on))
		scalling_ram=ctrl.ControlSystemSimulation(self.scalability_ram_ctrl)


		scalling_server=ctrl.ControlSystemSimulation(self.scalability_server_ctrl)

		scalling_server.input['memory_antecedent']=scalling_ram.input['memory_antecedent']=memory1
		
		scalling_server.input['ram_antecedent']=scalling_ram.input['ram_antecedent']=ram_state
		
		try:
			scalling_ram.compute()
			
			print('RAM')


			self.ram_output=int(scalling_ram.output['ram_consequent'])
			
			print(scalling_ram.output['ram_consequent'])
		except:
			try:
				self.ram_output=0
				print("Fine tunning neutral state with new parameters Fuzzy Logic")
				print(self.last_trigger[4])
				scalling_server.input['memory_antecedent']=scalling_ram.input['memory_antecedent']=self.last_trigger[4]
				scalling_server.input['servers_antecedent']=self.last_trigger[3]
				scalling_server.input['ram_antecedent']=scalling_ram.input['ram_antecedent']=self.last_trigger[5]
				scalling_ram.compute()
				print("Fine Tunning: "+str(scalling_ram.output['ram_consequent']))
			
				self.ram_output=int(scalling_ram.output['ram_consequent'])
			except:
				print("RAM No changes")
		try:
			scalling_server.compute()
			print('Servers')
			print(scalling_server.output['servers_consequent'])
			server_output=int(scalling_server.output['servers_consequent'])
			

		except Exception, e:
			server_output=0

			print("No number of SERVERS changes.")
			print(e)
			if memory1 >90 and ram_state > self.array_ram_hi[0]:
				server_output=2

		return self.ram_output, server_output

#if __name__ == "__main__":

#	controller=fl_class()
#	ram_output, server_output=controller.fl_ctrl()

#	print("Output")
#	print(ram_output, server_output)
 
