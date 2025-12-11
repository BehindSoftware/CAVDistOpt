import pyomo.environ as pyo
from pyomo.opt import SolverFactory

import time

def get_optimized_acceleration(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, x_pos, parameters):
    acceleration={}
    model = pyo.AbstractModel()

    print(parameters)
    #Constants:
    model.t = pyo.Param(default=parameters[0]) #time scale: t is the measurement frequency, it can be 1 second for now. (constant)
    epsilon_prime = parameters[1]*1000/3600 #km/h to m/s conversion for desired velocity
    alfa = parameters[2] #m/sec2 
    alfa_prime = parameters[3] #m/sec2
    model.gamma = pyo.Param(default=parameters[4]) #Gamma is Speed-Location Conversion Factor (constant) 0.4 is balance

    #Crashless constraints
    model.R = pyo.Param(default=parameters[5]) #CAV's reaction (s)
    model.D = pyo.Param(default=parameters[6]) #Safety Distance (m)
    model.lv = pyo.Param(default=parameters[7]) #Length of vehicle (m)
    model.F = pyo.Param(default=495) #Intersection point

    #I is the set of lanes
    #J is the set of vehicles
    model.I = pyo.RangeSet(1, number_of_lane)
    model.J = pyo.RangeSet(1, number_of_vehicle)
    model.lane = pyo.RangeSet(2, 4)

    #v is the current velocity parameter which comes from simulation
    #x is the current distance traveled parameter which comes from simulation
    model.v0 = pyo.Param(model.I, model.J, within=pyo.NonNegativeReals,initialize=v_input)
    model.x0 = pyo.Param(model.I, model.J, within=pyo.NonNegativeReals,initialize=x_input)
    model.xr = pyo.Param(model.I, model.J, within=pyo.NonNegativeReals, initialize=xr_cons) #Desired distance traveled
    model.x_p = pyo.Param(model.I, model.J, within=pyo.NonNegativeReals, initialize=x_pos)

    model.v = pyo.Var(model.I, model.J, domain=pyo.NonNegativeReals, bounds=(0, epsilon_prime), initialize=(0)) #nonnegative and lower than epsilonprime!
    model.x = pyo.Var(model.I, model.J, domain=pyo.NonNegativeReals, initialize=(0)) #nonnegative
    model.a = pyo.Var(model.I, model.J, bounds=(alfa, alfa_prime), initialize=(0)) #between alfa and alfaprime!
    model.w = pyo.Var(model.I, model.J, within=pyo.NonNegativeReals, initialize=(0))  # Additional variable for abs
    model.z = pyo.Var(model.I, model.J, within=pyo.NonNegativeReals, initialize=(0))  # Additional variable for safety abs

    def abs_constraint_rule(m, i, j):
        return m.w[i, j] >= m.v[i, j] - m.v0[i, j]
    model.abs_constraint1 = pyo.Constraint(model.I, model.J, rule=abs_constraint_rule)

    def abs_constraint_rule2(m, i, j):
        return m.w[i, j] >= -(m.v[i, j] - m.v0[i, j])
    model.abs_constraint2 = pyo.Constraint(model.I, model.J, rule=abs_constraint_rule2)

    def obj_expression(m):
        return sum(sum((m.xr[i,j] - m.x[i, j]) + m.gamma * m.w[i, j] 
                    for j in m.J if m.xr[i,j] != 0) 
                for i in m.I)

    #Assigning objective function
    model.OBJ = pyo.Objective(rule=obj_expression)
    model.name = "Optimization of Acceleration"

    def x_constraint_rule(m, i, j):
        if (m.xr[i,j] != 0):
            return m.x[i,j]==(((m.a[i,j]*m.t**2)/2)+m.v0[i,j]*m.t+m.x0[i,j])# return the expression for the constraint for i and j
        return pyo.Constraint.Skip

    # the next line creates one constraint for each member of the set model.I
    model.x1Constraint = pyo.Constraint(model.I, model.J, rule=x_constraint_rule) #model.x[model.I, model.J] = is correct for constraints ?

    def v_constraint_rule(m, i, j):
        if (m.xr[i,j] != 0):
            return m.v[i,j]==(m.a[i,j]*m.t+m.v0[i,j])# return the expression for the constraint for i and j, equation ?
        return pyo.Constraint.Skip
        
    # the next line creates one constraint for each member of the set model.I
    model.v1Constraint = pyo.Constraint(model.I, model.J, rule=v_constraint_rule)

    if(number_of_vehicle>2):
        def safe_distance_constraint_rule(m, i, j):
            #TO DO:if statement for x>500 which means check after the intersection, distance travelled is not same with x_pos
            if j<number_of_vehicle:
                if (m.xr[i,j] == 0 or m.xr[i,j+1] == 0): #Skip zeros
                    print("zeros") 
                    return pyo.Constraint.Skip
                print("m.x_p[i,j]:",m.x_p[i,j])
                print("m.x_p[i,j+1]:",m.x_p[i,j+1])
                return m.x[i, j] - m.x[i, j+1]>=((m.lv+m.D)+m.R*m.v[i,j+1])
            return pyo.Constraint.Skip

        # the next line creates one constraint for each member of the set model.I
        model.s1Constraint = pyo.Constraint(model.I, model.J, rule=safe_distance_constraint_rule)
    
        def lane_crossing_constraint_rule(m, lane, i, j): #lane should be 2, vehicles will be the first one which is close to the intersection
            if (m.xr[i,j] == 0 or m.xr[lane,j] == 0 or (i >= lane)): #eliminate the points which have not car and we want 1,2 ones not 2,1 again
                return pyo.Constraint.Skip
            if(m.x_p[i,j]<m.F-epsilon_prime or m.x_p[lane,j]<m.F-epsilon_prime): #not both in the intersection
                return pyo.Constraint.Skip
            #check x_p and make a decision it comes to intersection or goes from the intersection
            #if it comes return this one if it comes to second intersection multiply F with 2 and so on
            #CAUTION: DONE FOR ONLY 2 intersection passed cars NOT MORE
            if(m.x_p[i,j]<m.F and m.x_p[lane,j]<m.F): #Checks this is the first intersection for cars, if not m.F will be increased because of usage distance travelled X^t+1
                check_for_will_pass_inters = m.x_p[i,j]+m.v0[i,j]-m.F
                check_for_will_pass_inters_lane2 = m.x_p[lane,j]+m.v0[lane,j]-7-m.F
                if(check_for_will_pass_inters<0 and check_for_will_pass_inters_lane2<0): #This checks for absolute between F and X^t+1
                    return (m.F-m.x[i,j])+(m.F-m.x[lane,j])>=(m.lv+m.D)
                elif(check_for_will_pass_inters>0 and check_for_will_pass_inters_lane2<0):
                    return (m.x[i,j]-m.F)+(m.F-m.x[lane,j])>=(m.lv+m.D)
                elif(check_for_will_pass_inters<0 and check_for_will_pass_inters_lane2>0):
                    return (m.F-m.x[i,j])+(m.x[lane,j]-m.F)>=(m.lv+m.D)
                else:
                    return (m.x[i,j]-m.F)+(m.x[lane,j]-m.F)>=(m.lv+m.D)
                return pyo.Constraint.Skip
            elif(m.x0[i,j]>m.F and m.x0[lane,j]<m.F):
                return (2*m.F-m.x[i,j])+(m.F-m.x[lane,j])>=(m.lv+m.D)
            elif(m.x0[i,j]<m.F and m.x0[lane,j]>m.F):
                return (m.F-m.x[i,j])+(2*m.F-m.x[lane,j])>=(m.lv+m.D)
            elif(m.x0[i,j]>m.F and m.x0[lane,j]>m.F):
                return (2*m.F-m.x[i,j])+(2*m.F-m.x[lane,j])>=(m.lv+m.D)
            elif(m.x0[i,j]>2*m.F and m.x0[lane,j]>2*m.F):
                return (3*m.F-m.x[i,j])+(3*m.F-m.x[lane,j])>=(m.lv+m.D)
            else:
                return pyo.Constraint.Skip
            return pyo.Constraint.Skip

        model.l1Constraint = pyo.Constraint(model.lane, model.I, model.J, rule=lane_crossing_constraint_rule)
    
    # Create a solver
    #glpk, gurobi_persistent
    #opt = pyo.SolverFactory('glpk')
    opt = pyo.SolverFactory("gurobi_persistent", solver_io="python", verbose=True)

    # Create a model instance and optimize
    instance = model.create_instance()

    # Set the instance for the solver
    opt.set_instance(instance)

    # Measure the start time
    start_time = time.time()

    results = opt.solve(instance,tee=True)
    #print(results) #RUN

    # Measure the end time
    end_time = time.time()

    #instance.display() #Deeply Variable Knowledge
    #results.write() #License Briefly Output
    if(pyo.value(instance.OBJ)!=0):
        instance.pprint() #More deeply knowledge, it can be used to solve the problem as well
        # Print objective value
        print("\nObjective value:", pyo.value(instance.OBJ))

    # Print variable values
    #print("\nVariable values:")
    for var in instance.component_objects(pyo.Var):
        #print(var)
        if var.name == 'a':
            for index in var:
                #print(index, pyo.value(var[index]))
                acceleration[index]=pyo.value(var[index]) #Acceleration is populating

    # Calculate the optimization time
    optimization_time = end_time - start_time
    print(f"Optimization Time: {optimization_time} seconds")

    return acceleration