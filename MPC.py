import cvxpy as opt
from MPC_config import Params as P
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
		timeHorizon,
		Q = None,
		R = None,
		verbose = False,
	):

		if Q==None or R==None:
			Q = self.stateCost
			R = self.actionCost

		X = opt.Variable((self.stateLen, timeHorizon+1),name='states')
		U = opt.Variable((self.actionLen, timeHorizon),name='actions')

		costFunc = []

		for t in range(timeHorizon):
			_cost = opt.quad_form(refTraj[:,t+1]-X[:,t+1],Q) + opt.quad_form(U[:,t],R)

			_constraints = [
				X[:,t+1] == A@X[:,t] + B@U[:,t] + C,
				U[0,t] >= -2,
				U[0,t] <= 2,
			]

			if t < (timeHorizon - 1):
				_cost += opt.quad_form(U[:,t+1]-U[:,t],R*1)
				_constraints += [opt.abs(U[0,t+1]-U[0,t]) <= 0.01]

			if t == 0:
				_constraints += [ X[:,0]==initState[:,0] ]

			costFunc.append(opt.Problem(opt.Minimize(_cost),constraints = _constraints))

		problem = sum(costFunc)

		problem.solve(verbose=verbose, solver=opt.OSQP)

		return X,U



