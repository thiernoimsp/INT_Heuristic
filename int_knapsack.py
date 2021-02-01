import numpy as np
from mip import Model, xsum, maximize, BINARY

#V_d = {0:11,1:15,2:20,3:35,4:10,5:33}
#p = [1, 1, 1, 1, 1, 1]
#w = [11, 15, 20, 35, 10, 33]
#Kf = {1:47,2:30,3:56}
#f=1
#d=1


def Int_Knapsack(f,d, V_d, Kf):
	p = list(np.ones((len(V_d),),dtype=int))
	m = Model("knapsack")
	#x = [m.add_var(var_type=BINARY) for i in list(V_d.keys())]
	x = [(i,m.add_var(var_type=BINARY)) for i in list(V_d.keys())]
	m.objective = maximize(xsum(p[i] * x[i][1] for i in range(len(x))))
	m += xsum(V_d[x[i][0]] * x[i][1] for i in range(len(x))) <= Kf[f]
	m.optimize()
	#selected = [i for i in list(V_d.keys()) if x[i].x >= 0.99]
	selected = [x[i][0] for i in range(len(x)) if x[i][1].x >= 0.99]
	#print("selected items: {}".format(selected))
	y=(d,selected,f)
	return y



#sol = Int_Knapsack(f,d,V_d, Kf)