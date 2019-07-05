#Prepare ouputs for SWAT-CUP glue file for visulization

import os, sys, math
#from nsga2lib import nsga2
script_location = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(script_location), "SWATModel"))

import nsga2

#---- Input ----(space on directory may cause problems during execution)
#SWATtxtinoutDirectory = os.path.join(os.path.dirname(script_location),"SWATModel", "TxtInOut")
SWATtxtinoutDirectory = r"D:\proyectoSWATCUP\Prueba.Glue.SwatCup"
#---------------

#Create a directory for GLUE files
gluePath=SWATtxtinoutDirectory+'/SWAT-CUP_GLUE_files'
if not os.path.exists(gluePath):
    os.makedirs(gluePath)

#Initiliaze NSGA2 to get calibraiton inputs
NSGAII=nsga2.nsga2(SWATtxtinoutDirectory)
parname=NSGAII.parname
popsize=NSGAII.popsize
ngener=NSGAII.ngener
#Outlet_Obsdata=NSGAII.Outlet_Obsdata
HRU_Obsdata=NSGAII.HRU_Obsdata
#Outlets=Outlet_Obsdata.keys()
hrus=HRU_Obsdata.keys()

#======================== GLUE INPUTS ==========================
#Prepare glue.inf file
#TotalNumberofObservedVariables=str(int(len(Outlet_Obsdata)))
TotalNumberofObservedVariables=str(int(len(HRU_Obsdata)))
NumberOfDataPointsInEachVariable=''
#for outlet in Outlets:
for hru in hrus:
    #NumberOfDataPointsInEachVariable+=str(int(len(Outlet_Obsdata[outlet])))+'  '
    NumberOfDataPointsInEachVariable+=str(int(len(HRU_Obsdata[hru])))+'  '
NumberOfParameterToBeOptimized=str(int(len(parname)))    
glueinflines=TotalNumberofObservedVariables.ljust(20,' ')+': total number of observed variables\n'
glueinflines+=NumberOfDataPointsInEachVariable.ljust(20,' ')+': number of data points in each variable\n'
glueinflines+=NumberOfParameterToBeOptimized.ljust(20,' ')+': number of parameters to be optimized'
f=open(gluePath+'/glue.inf','w')
f.writelines(glueinflines)
f.close()

#Prepare var_file_name.txt file
varfilelines=''
#for outlet in Outlets:
for hru in hrus:
    #varfilelines+='FLOW_OUT_'+str(int(outlet))+'.txt\n'
    varfilelines+= str(hru)+'.txt\n'
f=open(gluePath+'/var_file_name.txt','w')
f.writelines(varfilelines[:-1])
f.close()


#Prepare glue_obs.dat file
glueobslines='number	data\n'
#for outlet in Outlets:
for hru in hrus:
    ###################################################################################################################################
    #IMPORTANT!! This number is not automatically written based on the real position/number (first column) in the file of observed data
    ###################################################################################################################################
    #i=0
    i=36
    #for value in Outlet_Obsdata[outlet]:
    for value in HRU_Obsdata[hru]:
        i+=1
        glueobslines+=str(i)+'\t'+str(value)+'\n'
f=open(gluePath+'/glue_obs.dat','w')
f.writelines(glueobslines[:-1])
f.close()        
#---------------------------------------------------------------



#======================== GLUE OUTPUTS ==========================
#Get Pareto front parameter and resulting objective function values
f=open(SWATtxtinoutDirectory+r"\NSGA2.OUT\output.out","r")
lines = f.readlines()
f.close()
prmtrno = int(NumberOfParameterToBeOptimized)
#Get the fist population (LHS) and last population (pareto front) 
print 'Reading NSGA-II first(good for sensitivity) and Pareto population...'
i=0; ObjectivesLHS=[]; ParametersLHS=[]; ObjectivesPareto=[]; ParametersPareto=[]
while i < len(lines):
    GenerationNo=-99.9
    if 'Generation No.     ->' in lines[i]:
        GenerationNo=int(lines[i].split('eneration No.     ->')[1].split('\n')[0])
    #fist population (LHS)
    if GenerationNo==1:
        i+=5
        for notused in xrange(popsize):
            variables = [float(x) for x in lines[i].split("\n")[0].split("|**|")[0].split(" ") if x!=""] #Get variables on line i before |**| (old population)
            ObjectivesLHS.append(variables[prmtrno:-2])
            ParametersLHS.append(variables[:prmtrno])
            i+=2
    #last population (pareto)
    if GenerationNo==int(ngener):
        i+=5
        for notused in xrange(popsize):
            variables = [float(x) for x in lines[i].split("\n")[0].split("|**|")[1].split(" ") if x!=""] #Get variables on line i after |**| (old population)
            ObjectivesPareto.append(variables[prmtrno:-2])
            ParametersPareto.append(variables[:prmtrno])
            i+=2
    i += 1
#Get Best result (based on average weighted objective funcs)
print 'Getting best NSGA-II parameter set...'
averageObjective=1e5; i=6; BestObjectiveSet=[]; BestParameterSet=[]
while i < len(lines):
    i+=2
    #Deal with generation title part
    if lines[i] == "\n":
        i += 10
        if i >= len(lines):#break if the loop is completed
            break
    Objs1 = [float(x) for x in lines[i].split("\n")[0].split("|**|")[0].split(" ") if (x!="" and x!="nan")][prmtrno:-2] #Get Objective functions on line i before |**| (old population)
    Objs2 = [float(x) for x in lines[i].split("\n")[0].split("|**|")[1].split(" ") if (x!="" and x!="nan")][prmtrno:-2] #Get Objective functions on line i after |**| (mate population)
    #Calculate weights for Objs1 and Objs2 objective functions
    averageObj1=(sum(Objs1)/float(len(Objs1)))
    averageObj2=(sum(Objs2)/float(len(Objs2)))
    if averageObj1<averageObjective:
        variables = [float(x) for x in lines[i].split("\n")[0].split("|**|")[0].split(" ") if x!=""] #Get variables on line i before |**| (old population)
        BestObjectiveSet=variables[prmtrno:-2]
        BestParameterSet=variables[:prmtrno]
        averageObjective=averageObj1
    if averageObj2<averageObjective:
        variables = [float(x) for x in lines[i].split("\n")[0].split("|**|")[1].split(" ") if x!=""] #Get variables on line i after |**| (old population)
        BestObjectiveSet=variables[prmtrno:-2]
        BestParameterSet=variables[:prmtrno]
        averageObjective=averageObj2
        
#Prepare modelpara.beh file
modelparaline=''
for pn in parname:
    modelparaline+=pn+'\t'
modelparaline+='objfun\n'

# Elimination of 'nan' values from list
BestObjectiveSetNotNaN = [float(x) for x in BestObjectiveSet if not math.isnan(x)]

#print LHS
for i in xrange(popsize):
    for prmtr in ParametersLHS[i]:
        modelparaline+=str(prmtr)+'\t'
    ObjectivesLHSNotNaN = [float(x) for x in ObjectivesLHS[i] if not math.isnan(x)] # Elimination of 'nan' values from list
    modelparaline+=str(sum(ObjectivesLHSNotNaN)/float(len(ObjectivesLHSNotNaN)))+'\n'
#print Pareto
for i in xrange(popsize):
    for prmtr in ParametersPareto[i]:
        modelparaline+=str(prmtr)+'\t'
    ObjectivesParetoNotNaN = [float(x) for x in ObjectivesPareto[i] if not math.isnan(x)] # Elimination of 'nan' values from list
    modelparaline+=str(sum(ObjectivesParetoNotNaN)/float(len(ObjectivesParetoNotNaN)))+'\n'
#print Best
for prmtr in BestParameterSet:
    modelparaline+=str(prmtr)+'\t'
modelparaline+=str(sum(BestObjectiveSetNotNaN)/float(len(BestObjectiveSetNotNaN)))+'\n'
f=open(gluePath+'/modelpara.beh','w')
f.writelines(modelparaline)
f.close()

#------ Run SWAT ------
os.chdir(SWATtxtinoutDirectory)
#outlets = Outlets
#outlets.sort()
#hrus.sort()
def RunSWAT4ParameterSets(ParameterSets):
    #_Outlet_Modeldata=[] #Results are in parameter set order
    _HRU_Modeldata=[] #Results are in parameter set order
    for parset in ParameterSets:
        #Print parameter set in model.in file
        modelinf = open(SWATtxtinoutDirectory+"\model.in","w")
        writeline =''
        for j in xrange(prmtrno): #parameter loop
            writeline += parname[j]+'\t'+str(parset[j])+'\n'       
        modelinf.writelines(writeline)
        modelinf.close()
        #Run command file (SWATedit, SWAT and extract exe files)
        os.system(SWATtxtinoutDirectory+'/nsga2_mid.cmd')
        #Read 'model.out' file
        #modelrchf = open(SWATtxtinoutDirectory+'/model.out','r')
        modelhruf = open(SWATtxtinoutDirectory+'/model.out','r')
        #lines = modelrchf.readlines()
        lines = modelhruf.readlines()
        #Outlet_Modeldata = {}
        HRU_Modeldata = {}
        k=0; Modeldata=[]
        #for outlet in outlets:
        for hru in hrus:
            #nofdatapoints = len(Outlet_Obsdata[outlet])
            nofdatapoints = len(HRU_Obsdata[hru])
            for j in range(k,k+nofdatapoints):
                Modeldata.append(float(lines[j].split()[1]))
            #Outlet_Modeldata[outlet] = Modeldata
            HRU_Modeldata[hru] = Modeldata
            k = j+1
            Modeldata=[]
        #_Outlet_Modeldata.append(Outlet_Modeldata)
        _HRU_Modeldata.append(HRU_Modeldata)
    #return _Outlet_Modeldata
    return _HRU_Modeldata
    
print '\n'*5, "-"*45,"\nRunning SWAT for LHS parameter sets...\n", "-"*45
#LHS__Outlet_Modeldata=RunSWAT4ParameterSets(ParametersLHS)
LHS__HRU_Modeldata=RunSWAT4ParameterSets(ParametersLHS)
print '\n'*5, "-"*45,"\nRunning SWAT for Pareto parameter sets...\n", "-"*45
#Pareto__Outlet_Modeldata=RunSWAT4ParameterSets(ParametersPareto)
Pareto__HRU_Modeldata=RunSWAT4ParameterSets(ParametersPareto)
print '\n'*5, "-"*45,"\nRunning SWAT for best parameter set...\n", "-"*45
#Best__Outlet_Modeldata=RunSWAT4ParameterSets([BestParameterSet])
Best__HRU_Modeldata=RunSWAT4ParameterSets([BestParameterSet])

#Prepare modelres.beh file
modelreslines=''
#print LHS
for i in xrange(popsize):
    #for outlet in outlets:
    for hru in hrus:
        #for val in LHS__Outlet_Modeldata[i][outlet]:
        for val in LHS__HRU_Modeldata[i][hru]:
            modelreslines+=str(val)+'\t'
    modelreslines+='\n'
#print Pareto
for i in xrange(popsize):
    #for outlet in outlets:
    for hru in hrus:
        #for val in Pareto__Outlet_Modeldata[i][outlet]:
        for val in Pareto__HRU_Modeldata[i][hru]:
            modelreslines+=str(val)+'\t'
    modelreslines+='\n'
#print Best
#for outlet in outlets:
for hru in hrus:
    #for val in Pareto__Outlet_Modeldata[0][outlet]:
    for val in Best__HRU_Modeldata[0][hru]:
        modelreslines+=str(val)+'\t'
modelreslines+='\n'
f=open(gluePath+'/modelres.beh','w')
f.writelines(modelreslines)
f.close()
#---------------------------------------------------------------
        


