import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint



class reactionBalance():
    
    
    def __init__(self, volume,concentration, temperature):
        if isinstance(volume, float):   
            self.Volume= volume
        else:
            print("volume must be a float,using default volume =1.0L")
            self.Volume = 1.0
        if isinstance(concentration, float):
            self.Concentration= concentration
        else:
            print("concentration must be a float,using default concentration =0.0mol/L")
            self.Concentration = 0.0
        if isinstance(temperature, float):
            self.Temperature = temperature
        else:
            print("Temperature must be a float, using default temperature =300.0k")
            self.Temperature = 300.0
        self.timeInterval = np.linspace(0,5,100)
        
    

    '''function that reeturns the inlet volumentric flowrate'''
    def inletVolumetricFlowRate(self):
        while True:
            try:
                # qf is the inlet_volumetric_flowrate
                qf = np.ones(len(self.timeInterval))* 10.0
                qf[50:] = 5.1
                return qf
            except:
                print("unknown error occured in the inletVolumetricFlowRate method")
            
    '''function to return the outlet volumetric flowrate'''
    def outletVolumetricFlowrate(self):
         while True:
            try:
                # q is the outlet volumetric flowrate
                q = np.ones(len(self.timeInterval))*5.0
                return q
            except:
                print("unknown error occured in the outletVolumetricFlowrate method")


    '''function to return the feed concentrations'''
    def feedConcentration(self):
        while True:
            try:
            # Feed Concentration (mol/L)
                Caf = np.ones(len(self.timeInterval))*2.0
                Caf[30:] = 0.5
                return Caf
            except:
                print("unknown error occured in the feedConcentration method")

    '''function to return the inlet  temperature'''
    def inletTemperature(self):
        while True:
            try:
            # Feed Temperature (K)
                Tf = np.ones(len(self.timeInterval))*400.0
                Tf[70:] = 350.0
                return Tf
            except:
                print("unknown error occured in the inletTemperature method")

    '''function that defines the mixing model and the mass balance, volume balance and the energy balance'''
    def reactionChamber(self, states,timeInterval,outletVolumetricFlowrate,inletVolumetricFlowrate,inletConcentration,inletTemperature):

        # error handling
        while True:
            try:
                Volume = states[0]# Volume (L)
                Concentration = states[1] # Concentration of A (mol/L)
                Temperature = states[2]# Temperature (K)

                # Parameters:
                # Reaction
                reactionRate = 0.0

                # Mass balance
                massBalance = inletVolumetricFlowrate - outletVolumetricFlowrate

                # Species balance

                speciesBalance= (inletVolumetricFlowrate*inletConcentration - outletVolumetricFlowrate*Concentration)/Volume - reactionRate - (Concentration*massBalance/Volume)

                # Energy balance
                energyBalance = (inletVolumetricFlowrate*inletTemperature - outletVolumetricFlowrate*Temperature)/Volume - (Temperature*massBalance/Volume)

                # Return calculations
                return [massBalance,speciesBalance,energyBalance]
            except ValueError:
                print("wrong value input in the reactionChamber method ")
                

    '''functions that manipulates the data, and saves theh results'''
    def saveData(self):
        # Storage for results
        if isinstance(self.Volume, float):
            Vol  = np.ones(len(self.timeInterval))*self.Volume
        else:
            print("concentration must be a float")
        if isinstance(self.Concentration, float):
            Cons = np.ones(len(self.timeInterval))*self.Concentration
        else:
            print("concentration must be a float")
        if isinstance(self.Temperature, float):
            Temp  = np.ones(len(self.timeInterval))*self.Temperature
        else:
            print("concentration must be a float")   
        Y = [self.Volume,self.Concentration,self.Temperature]
        # Loop through each time step
        for i in range(len(self.timeInterval)-1):
            # Simulate
            inputs = (self.outletVolumetricFlowrate()[i],self.inletVolumetricFlowRate()[i],self.feedConcentration()[i],self.inletTemperature()[i])
            ts = [self.timeInterval[i],self.timeInterval[i+1]]
            y = odeint(self.reactionChamber,Y,ts,args=inputs)
            # Store results
            Vol[i+1]  = y[-1][0]
            Cons[i+1] = y[-1][1]
            Temp[i+1]  = y[-1][2]
            # Adjust conditions for next loop
            Y = y[-1]
        

        # Construct results and save data file
        data = np.vstack((self.timeInterval,self.inletVolumetricFlowRate(),self.outletVolumetricFlowrate(),self.inletTemperature(),self.feedConcentration(),Vol,Cons,Temp)) # vertical stack
        data = data.T # transpose data
        np.savetxt('./output/data.txt',data,delimiter=',')

        # Plot the inputs and results
        plt.figure()

        plt.subplot(3,2,1)
        plt.plot(self.timeInterval,self.inletVolumetricFlowRate(),'b--',linewidth=3)
        plt.plot(self.timeInterval,self.outletVolumetricFlowrate(),'b:',linewidth=3)
        plt.ylabel('Flow Rates (L/min)')
        plt.legend(['Inlet','Outlet'],loc='best')

        plt.subplot(3,2,3)
        plt.plot(self.timeInterval,self.feedConcentration(),'r--',linewidth=3)
        plt.ylabel('Caf (mol/L)')
        plt.legend(['Feed Concentration'],loc='best')

        plt.subplot(3,2,5)
        plt.plot(self.timeInterval,self.inletTemperature(),'k--',linewidth=3)
        plt.ylabel('Tf (K)')
        plt.legend(['Feed Temp'],loc='best')
        plt.xlabel('Time (min)')

        plt.subplot(3,2,2)
        plt.plot(self.timeInterval,Vol,'b-',linewidth=3)
        plt.ylabel('Vol (L)')
        plt.legend(['Volume'],loc='best')

        plt.subplot(3,2,4)
        plt.plot(self.timeInterval,Cons,'r-',linewidth=3)
        plt.ylabel('Ca (mol/L)')
        plt.legend(['Concentration'],loc='best')

        plt.subplot(3,2,6)
        plt.plot(self.timeInterval,Temp,'k-',linewidth=3)
        plt.ylabel('T (K)')
        plt.legend(['Temperature'],loc='best')
        plt.xlabel('Time (min)')

        plt.show()