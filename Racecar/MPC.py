import cvxpy as opt
#from MPC_config import Params as P
import numpy as np

class MPC:
	def __init__(self, N, M, Q, R):
		self.stateLen = N
		self.actionLen = M
		self.stateCost = Q
		self.actionCost = R

	def optimizeLinearModel(self,
			A,B,C,
			initState,
			refTraj,
			T
		):

			X = opt.Variable((self.stateLen, T+1),name='states')
			U = opt.Variable((self.actionLen, T),name='actions')

			costFunc = []

			for t in range(T):
				_cost = opt.quad_form(refTraj[:,t+1]-X[:,t+1],self.stateCost) + opt.quad_form(U[:,t],self.actionCost)

				_constraints = [
					X[:,t+1] == A@X[:,t] + B@U[:,t] + C,
					U[0,t] >= -5,
					U[0,t] <= 5,
				]

				if t < (T - 1):
					_cost += opt.quad_form(U[:,t+1]-U[:,t],self.actionCost*1)
					_constraints += [opt.abs(U[0,t+1]-U[0,t]) <= 0.1]

				if t == 0:
					_constraints += [ X[:,0]==initState[:,0] ]

				costFunc.append(opt.Problem(opt.Minimize(_cost),constraints = _constraints))

			problem = sum(costFunc)

			problem.solve(verbose=False, solver=opt.OSQP)

			return X,U