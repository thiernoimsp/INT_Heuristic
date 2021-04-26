import os
import sys
import time
import random
import itertools
from collections import defaultdict
from mip import Model, xsum, maximize, BINARY, ConstrsGenerator, CutPool
from instance_heuristic import Instance
from int_knapsack import Int_Knapsack

from arguments_heuristic import Arguments


class Int_Heuristic:
	""" 
	This class implement the new proposed model using gurobi 
	"""


	def __init__(self, inst):
		Sol = list()
		Flows_Crossing_Device  = defaultdict(list)
		Candidate_List = defaultdict(list)
		All_Cases_List = list()
		Restricted_Candidate_List = list()
		rcl_nb = int()
		CollectedItems = defaultdict(list)
		Spati = list()
		Tempo = list()
		#seed = [[],float("inf")]
		#seed1 = [[],float("inf")]

		self.Sol = Sol
		self.Flows_Crossing_Device = Flows_Crossing_Device
		self.Candidate_List = Candidate_List
		self.Restricted_Candidate_List = Restricted_Candidate_List
		self.rcl_nb = rcl_nb
		self.CollectedItems = CollectedItems
		self.Spati = Spati
		self.Tempo = Tempo
		self.All_Cases_List = All_Cases_List
		#self.seed = seed





	def restricted_candidate_list(self, greediness_value = 0.5):
		seed = [[],float("inf")]
		seed1 = [[],float("inf"), [],float("inf")]

		for d in inst.D:
			for f in inst.F :
				if d in inst.path[f]:
					self.Flows_Crossing_Device[d].append(f)

		print(inst.V_d)
		for d in inst.D:
			for i in range(len(inst.R)):
				self.Candidate_List[d].append([d, inst.R[i], sum([inst.V_d[k] for k in inst.R[i]])])
		self.Candidate_List = sorted(self.Candidate_List.values(), reverse=True)
		#self.Candidate_List.sort(key=lambda x:[x[0][2]])

		for i in range(len(self.Candidate_List)):
			for j in range(len(self.Candidate_List[i])):
				self.All_Cases_List.append(self.Candidate_List[i][j])

		self.All_Cases_List.sort(key=lambda x:[x[2]])
		#seed = [[],float("inf")]
		#rest_list = []
		for i in inst.D:
			rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
			if (rand > greediness_value):
				#rest_list = self.All_Cases_List[:4] # grab the first five elements
				####
				while len(self.All_Cases_List) > 0:
					rest_list = self.All_Cases_List[:4] # grab the first five elements
					s = random.choice(rest_list)
					#for t in range(len(s)):
					for v in s[1]:
						for f in self.Flows_Crossing_Device[s[0]]:
							#if v in s[t][1] and f in self.Flows_Crossing_Device[s[t][0]]:
							if inst.V_d[v] <= inst.Kf[f]:
								self.Sol.append([s[0],v,f])
								#seed[0].append([s[0],v,f])
								self.CollectedItems[s[0]].append(v)
								n_cap = inst.Kf[f] - inst.V_d[v]
								n_Kf = {f:n_cap}
								inst.Kf.update(n_Kf)
								#print(inst.Kf[f])
								break
					self.All_Cases_List.pop(self.All_Cases_List.index(s))


				#####
			elif (rand <= greediness_value):
				#rest_list = random.sample(self.All_Cases_List, 4)   # select randomly four element
				####
				while len(self.All_Cases_List) > 4:
					rest_list = random.sample(self.All_Cases_List, 4)   # select randomly four element
					s = random.choice(rest_list)
					#for t in range(len(s)):
					for v in s[1]:
						for f in self.Flows_Crossing_Device[s[0]]:
							#if v in s[t][1] and f in self.Flows_Crossing_Device[s[t][0]]:
							if inst.V_d[v] <= inst.Kf[f]:
								self.Sol.append([s[0],v,f])
								self.CollectedItems[s[0]].append(v)
								n_cap = inst.Kf[f] - inst.V_d[v]
								n_Kf = {f:n_cap}
								inst.Kf.update(n_Kf)
								#print(inst.Kf[f])
								break
					self.All_Cases_List.pop(self.All_Cases_List.index(s))
					####
		seed[0] = self.Sol
		seed[1] = len(self.Sol)

		# the spatial dependencies 
		for m in inst.M:
			for d in inst.D:
				for P in range(len(inst.Rs[m])):
					if set(inst.Rs[m][P]).issubset(self.CollectedItems[d]):
						ss = (m,d,P, inst.Rs[m][P])
						self.Spati.append(ss)


		for m in inst.M:
			for P in range(len(inst.Rt[m])):
				if inst.HH[P] > inst.TT[P]:
					tt = (m,P,inst.Rt[m][P])
					self.Tempo.append(tt)


		seed1[0] = self.Spati
		seed1[1] = len(self.Spati)
		seed1[2] = self.Tempo
		seed1[3] = len(self.Tempo)
		return seed, seed1
		





if __name__ == "__main__":
	arg = Arguments(sys.argv)

	start_time = time.time()
	inst = Instance(path_data = arg.instance, num_nodes = arg.num_nodes, edges_to_attach = arg.edges_to_attach, num_flows = arg.num_flows, min_size = arg.min_size, max_size = arg.max_size, num_items = arg.num_items, num_mon_app = arg.num_mon_app)
	heuristic = Int_Heuristic(inst)
	#heuristic.Int_Greedy_Constructive()
	seed, seed1 = heuristic.restricted_candidate_list(greediness_value = 0.5)
	print("------------------------------")
	#print("Collected Items :", seed[0])
	print("------------------------------")
	print("Number of Collected Items : ", seed[1])
	print("------------------------------")
	#print("Satisfied Spatials Dependencies :", seed1[0])
	#print("------------------------------")
	print("Number of Satisfied Spatial Dependencies : ", seed1[1])
	print("------------------------------")
	#print("Satisfied Temporal Dependencies :", seed1[2])
	#print("------------------------------")
	print("Number of Satisfied Temporal Dependencies : ", seed1[3])
	print("------------------------------")
	print("Value of the Objecrive Function : ", seed1[1] + seed1[3])


	print("------------------------------")
	print("Total runtime: %.2f seconds" % (time.time() - start_time))




