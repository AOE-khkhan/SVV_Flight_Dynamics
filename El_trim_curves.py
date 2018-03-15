#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 09:34:38 2018

@author: MatsKlijn
"""

g = 9.81
rho0 = 1.225    
Ws = 60500                                                      #Standard aircraft weight (N)
W_empty = 3364                                                  #kg
W_fuel_start = 4100*0.45359237                                  #kg
gamma = 1.4
R = 287.05

from numpy import *
from CLCD_calc import V_tas, lift_stationary
from Cit_par import Cm0, Cma, CmTc, Cmde
from rho import rho1

#DATA

W_passengers = sum(array([82, 92, 60, 60, 77, 69, 67, 95, 84]))             #Weight in N
hp = array([7030, 7270, 7500, 7740, 7020, 6680, 6050])*0.3048                  #altitude in m
V_ias = array([165, 155, 145, 136, 175, 186, 196])*0.51444444444               #m/s
alpha = array([5.1, 5.9, 6.9, 7.9, 4.4, 3.8, 3.3])                             #deg
delta_e = array([0, -0.4, -0.8, -1.3, 0.4, 0.7, 1])                            #deg
delta_e_trim = array([2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.8])                      #deg
stick_force = array([0, -21, -26, -44, 26, 55, 78])                            #N
fuel_flow_left = array([466, 462, 458, 453, 470, 479, 489])*0.000125997881     #kg/s
fuel_flow_right = array([490, 486, 483,478, 493, 500, 510])*0.000125997881     #kg/s
fuel_used = array([632, 646, 666, 686, 707, 726, 760])*0.45359237              #kg
total_air_temp = array([-0.2, -1.2, -2.2, -3, 0.2, 1.5, 2.8]) + 273.15         #Kelvin

#Weights at start tests
W_start = []
for i in range(len(fuel_used)):
    W_start.append((W_empty + W_passengers + W_fuel_start - fuel_used[i])*g)


#Equivalent Airspeed (V_e)
Vc = []
for i in range(len(V_ias)):
    Vc.append(V_ias[i] - 2*0.51444444444)
    
###Pressure calculation
p = []

for i in range(len(hp)):
    p1 = p0*(1 + (lamda*hp[i])/T0)**(-g/(R*lamda))
    p.append(p1)


#Mach  
M = []

for i in range(len(p)):
    M1 = 1+((gamma-1)/(2*gamma))*(rho0/p0)*Vc[i]**2
    M2 = M1**(gamma/(gamma-1))
    M3 = M2-1
    M4 = 1+(p0/p[i])*M3
    M5 = M4**((gamma-1)/gamma)
    M6 = M5-1
    M7 = (2/(gamma-1))*M6
    M8 = sqrt(M7)
    M.append(M8)

#Calibrated Temp

Temp_c = []

for i in range(len(M)):
    Temp_c.append(total_air_temp[i]/(1+((gamma-1)/2)*M[i]**2))

#Angle of Attack
aoa = []
for i in range(len(M)):
    aoa.append(sqrt(gamma*R*Temp_c[i]))

#True Airspeed
V_tas = []
for i in range(len(M)):
     V_tas.append(aoa[i]*M[i])

rho = []
for i in range(len(hp)):
    rho.append(rho1(hp[i],Vc[i],total_air_temp[i]))



'''
V_e = []
for i in range(len(rho)):
    V_e.append(V_tas[i]*(sqrt(rho[i])/rho0)*(Ws/lift_stationary[i]))
'''
#Dimensionless Thrust Coefficient (Tc)


#delta_eq = -(1/Cmde)*(Cm0+Cma(a-a0)+CmTc*Tc)