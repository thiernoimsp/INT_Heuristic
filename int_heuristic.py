import os
import sys
import time
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
		Spati = list()
		Tempo = list()
		#Sols = list()
		ProceededNodes = list()
		FinishedNodes = list()
		CollectedItems = defaultdict(list)

		self.inst = inst
		self.Sol = Sol
		self.Spati = Spati
		self.Tempo = Tempo
		#self.Sols = Sols
		self.ProceededNodes = ProceededNodes
		self.FinishedNodes = FinishedNodes
		self.CollectedItems = CollectedItems
		#print(inst.path)
		#print(inst.V_d)
		#print(inst.Kf)


	def Int_Collecte_Heuristic(self):
		#for d in inst.D:
		#	self.CollectedItems[d] = []

		for f in inst.F:
			for d in inst.path[f]:
				if len(self.CollectedItems[d]) == len(inst.V_d):
					self.FinishedNodes.append(d)
				if d in self.FinishedNodes:
					continue
				elif d in self.ProceededNodes:
					V_dd = dict(inst.V_d)

					for key in self.CollectedItems[d]:
						V_dd.pop(key)

					y = Int_Knapsack(f,d, V_dd, inst.Kf)
					if len(y[1]) != 0:
						self.Sol.append(y)

					for item in y[1]:
						self.CollectedItems[d].append(item)
				else:
					y = Int_Knapsack(f,d, inst.V_d, inst.Kf)
					if len(y[1]) != 0:
						self.Sol.append(y)

					for item in y[1]:
						self.CollectedItems[d].append(item)
					self.ProceededNodes.append(d)

				size_col_items = list()
				for item in y[1] :
					size_col_items.append(inst.V_d[item])

				n_cap = inst.Kf[f] - sum(size_col_items)
				n_Kf = {f:n_cap}
				inst.Kf.update(n_Kf)
				#print(inst.Kf[f])

				size_not_col_items = list()
				for item in list(inst.V_d.keys()):
					if item not in y[1]:
						size_not_col_items.append(inst.V_d[item])

				#print(size_not_col_items)
				#print(size_col_items)

				if len(size_not_col_items) == 0:
					break
				elif len(size_not_col_items) >= 1:
					if inst.Kf[f] < min(size_not_col_items):
						break




				#if inst.Kf[f] < min(size_not_col_items):
				#	break

			#self.Sol.append(y)

		#print(self.ProceededNodes)
		#print(self.FinishedNodes)
		print(self.CollectedItems)
		#print(inst.V_d)
		#for i,j in enumerate(self.Sol):
		#	print(i,j)
		#print(self.Sol)


		for m in inst.M:
			for d in inst.D:
				for P in range(len(inst.Rs[m])):
					if set(inst.Rs[m][P]).issubset(self.CollectedItems[d]):
						ss = (m,d,P, inst.Rs[m][P])
						self.Spati.append(ss)
						#print(ss)

		for m in inst.M:
			for P in range(len(inst.Rt[m])):
				if inst.HH[P] > inst.TT[P]:
					tt = (m,P,inst.Rt[m][P])
					self.Tempo.append(tt)



		print(len(inst.Rs[m]))
		print(inst.R)
		for i,j in enumerate(self.Spati):
			print(i,j)
		#print(self.Sols)

		sum_col = []
		for d in inst.D:
			sum_col.append(len(self.CollectedItems[d]))

		#print(sum_col)
		print("Collected items :", sum(sum_col))
		print("temporal req", len(self.Tempo))
		print("spatial req", len(self.Spati))
		print("objective", len(self.Tempo) + len(self.Spati))
		#print(len(sum_col))





if __name__ == "__main__":
	arg = Arguments(sys.argv)
	inst = Instance(path_data = arg.instance, num_nodes = arg.num_nodes, edges_to_attach = arg.edges_to_attach, num_flows = arg.num_flows, min_size = arg.min_size, max_size = arg.max_size, num_items = arg.num_items, num_mon_app = arg.num_mon_app)
	heuristic = Int_Heuristic(inst)
	heuristic.Int_Collecte_Heuristic()










	#inst = Instance('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/New_Implememntation/INT_Gurobi/INT_Class', 50, 50, 9, 8, 4)
	##inst = Instance('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/New_Implememntation/INT_Gurobi/INT_Class', 9, 8, 4)
	##heuristic = Int_Heuristic(inst)
	##heuristic.Int_Collecte_Heuristic()
