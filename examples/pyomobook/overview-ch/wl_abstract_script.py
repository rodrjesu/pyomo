# wl_abstract_script.py: Scripting using an AbstractModel
import pyomo.environ as pyo

model = pyo.AbstractModel(name="(WL)")

model.N = pyo.Set()
model.M = pyo.Set()

model.d = pyo.Param(model.N, model.M)
model.P = pyo.Param()

model.x = pyo.Var(model.N, model.M, bounds=(0, 1))
model.y = pyo.Var(model.N, within=pyo.Binary)


def obj_rule(model):
    return sum(model.d[n, m] * model.x[n, m] for n in model.N for m in model.M)


model.obj = pyo.Objective(rule=obj_rule)


def one_per_cust_rule(model, m):
    return sum(model.x[n, m] for n in model.N) == 1


model.one_per_cust = pyo.Constraint(model.M, rule=one_per_cust_rule)


def warehouse_active_rule(model, n, m):
    return model.x[n, m] <= model.y[n]


model.warehouse_active = pyo.Constraint(model.N, model.M, rule=warehouse_active_rule)


def num_warehouses_rule(model):
    return sum(model.y[n] for n in model.N) <= model.P


model.num_warehouses = pyo.Constraint(rule=num_warehouses_rule)

# @abstractsolve:
instance = model.create_instance('wl_data.dat')
solver = pyo.SolverFactory('glpk')
solver.solve(instance)
instance.y.pprint()
# @:abstractsolve
