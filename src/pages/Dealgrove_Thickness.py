import math
import time

# Orientation is taken as string of <100> or <111>, state is taken as string of wet and dry, time is taken in hours
# initial is the initial thickness in angstrom , Temperature is taken in celsius, Thickness output is string

def dealgrovethickness(ori,state,time,initial,temp):

   
    k = 8.6173 * math.pow(10,-5);
    
    temp=float(temp)+273.0                           #( C to Kelvin)
#    time=float(time)*60.0
    initial=initial* math.pow(10,-4)                #( angstrom  to micrometre)
    
    
    if(state=="wet"):
        B=386*math.exp(-0.78/(k*temp))
        
        if(ori=='<100>'):
            A=B/(9.7*(10**7)*math.exp(-2.05/(k*temp)))
        elif(ori=='<111>'):
            A=B/(1.63*(10**8)*math.exp(-2.05/(k*temp)))
    
        tau=((initial**2) + A*initial)/B
    
   
    elif(state=="dry"):
        B=772*math.exp(-1.23/(k*temp))
        
        if(ori=='<100>'):
            A=B/(3.71*(10**6)*math.exp(-2.00/(k*temp)))
        elif(ori=='<111>'):
            A=B/(6.23*(10**6)*math.exp(-2.00/(k*temp)))
        
        tau=((initial**2) + A*initial)/B
            
    
    thickness= (((-A) + math.sqrt((A**2)+(4*B*(time+tau))))/2)
    ans= thickness*10000  #Converting to angstrom 
    
   

    return (str(ans)+" Ǻ")