#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 11:58:57 2018

@author: MatsKlijn
"""
#meh
from numpy import *
from Cit_par import *
from control.matlab import *
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


#Asymmetrical case

#---------------state space systems -------------------------------------------
#dimension having
C1_asymmetric = matrix([[(CYbdot-2*mub)*b/V0,0,0,0],
                         [0,-b/(2*V0),0,0], 
                         [0,0,(-4*mub*KX2*b**2)/(2*V0**2),(4*mub*KXZ*b**2)/(2*V0**2)],
                         [Cnbdot*b/(V0),0,(4*mub*KXZ*b**2)/(2*V0**2),(-4*mub*KZ2*b**2)/(2*V0**2)]
                         ])

C2_asymmetric = matrix([[CYb, CL, CYp*b/(2*V0),(CYr-4*mub)*b/(2*V0)],
                         [0,0,b/(2*V0),0],
                         [Clb,0,Clp*b/(2*V0),Clr*b/(2*V0)],
                         [Cnb,0,Cnp*b/(2*V0),Cnr*b/(2*V0)]
                         ])

C3_asymmetric = matrix([[CYda,CYdr],
                        [0,0],
                        [Clda,Cldr],
                        [Cnda,Cndr]
                        ])


A_asymmetric = -linalg.inv(C1_asymmetric)*C2_asymmetric
B_asymmetric = -linalg.inv(C1_asymmetric)*C3_asymmetric
C_asymmetric = identity(4)
D_asymmetric = zeros((4,2))

sys_asymmetric=ss(A_asymmetric,B_asymmetric,C_asymmetric,D_asymmetric)

# dimensionless
C1_asym_dimless = matrix([[(CYbdot-2*mub)*b/V0,0,0,0],
                         [0,-b/(2*V0),0,0], 
                         [0,0,-4*mub*KX2*b/V0,4*mub*KXZ*b/V0],
                         [Cnbdot*b/V0,0,4*mub*KXZ*b/V0,-4*mub*KZ2*b/V0]])

C2_asym_dimless = matrix([[CYb, CL, CYp,(CYr-4*mub)],
                         [0,0,1,0],
                         [Clb,0,Clp,Clr],
                         [Cnb,0,Cnp,Cnr]])

C3_asym_dimless = matrix([[CYda,CYdr],
                        [0,0],
                        [Clda,Cldr],
                        [Cnda,Cndr]])


A_asym_dimless = -linalg.inv(C1_asym_dimless)*C2_asym_dimless
B_asym_dimless = -linalg.inv(C1_asym_dimless)*C3_asym_dimless
C_asym_dimless=identity(4)
C_asym_hybrid = matrix([[1,0,0,0],[0,1,0,0],[0,0,2*V0/b,0],[0,0,0,2*V0/b]])
D_asym_dimless = zeros((4,2))

#true dimensionless output
sys_asym_dimless=ss(A_asym_dimless,B_asym_dimless,C_asym_dimless,D_asym_dimless)

#dimensionless computation but dimension having output
sys_hybrid=ss(A_asym_dimless, B_asym_dimless,C_asym_hybrid,D_asym_dimless)


#---state space computation------------------------------------------------------
#-------------------------------------------------------------------------------

#-------inputs-------------

simlength=15 #[s]

timestep=0.01 #[s]

t=arange(0,simlength,timestep)

uda=[0.025]*int(1/timestep)+[0]*(len(t)-int(1/timestep)) #input vector for aileron deflection
#uda=[0]*len(t)              
udr=[0]*len(t) 
#udr=[0.025]*int(1/timestep)+[0]*(len(t)-int(1/timestep))#input vector for rudder deflection
u=vstack((uda,udr)).T       #input vector to model

#--which model is selected----------------------------------------------------

#sys=sys_asymmetric          #standard dimension having
sys=sys_hybrid              #dimless computation, dim having outputs
#sys=sys_asym_dimless        #dimless outputs


#--what Input is selected------------------------------------------------------

y=lsim(sys,u,t)                     #Using input vector
#y=impulse(sys,t,input=0)            #Impulse input: 0=aileron // 1= rudder
#y=step(sys,t,input=0)               #Step input: 0=aileron // 1= rudder


#-----Matrix analysis--------------------------------------------------------

#--------dimensionless system--------------------------------------------------
print()

print('Asymmetric Flight:')

print()

eigenvalues_A_asym_dimless=linalg.eig(A_asym_dimless)[0]
print ('Eigenvalues:',eigenvalues_A_asym_dimless)

print()

T12_A_asym_dimless=log(0.5)/real(array(linalg.eig(A_asym_dimless)[0]))
print ('T1/2:',T12_A_asym_dimless)

print()

Period_A_asym_dimless=2*pi/imag(array(linalg.eig(A_asym_dimless)[0]))
print ('Period:',Period_A_asym_dimless)


print()

damping=damp(sys,doprint=False)[1]
print ('Damping:',damping)


print()

natfreq=damp(sys,doprint=False)[0]*sqrt(1-damp(sys,doprint=False)[1]**2)
print ('Nat. Frequency:',natfreq)


print()
damp(sys)


#----------plotting-----------------------------------------------------------
plt.figure(1)

plt.subplot(611)
plt.title('Sideslip Angle beta (rad)')
plt.plot(t,y[0][:,0],color='c',label='beta')

plt.subplot(612)
plt.title('Roll Angle phi (rad)')
plt.plot(t,y[0][:,1], color='r', label='phi')

plt.subplot(613)
plt.title('Roll Rate p (rad/s)')
plt.plot(t,y[0][:,2],color='b',label='q')

plt.subplot(614)
plt.title('Yaw Rate r (rad/s)')
plt.plot(t,y[0][:,3],color='g',label='r')

plt.subplot(615)
plt.title('input in rudder')
plt.plot(t,udr,color='y',label='dr')

plt.subplot(616)
plt.title('input in aileron')
plt.plot(t,uda,color='k',label='da')

#plt.show()