import re
from io import StringIO
import sys



################# write the result in the final file for the final report                
def writeText(function):
    textfile = open("Final-Clang-Tidy-Report.txt","w")
    textfile.write(function)
    textfile.write('\n')
    textfile.close()

############### read specific string from file
def readClangConfig():
    stringLineToMatch = "LineThreshold"
    
    stringBranchToMatch = "BranchThreshold"
   
    stringNestingToMatch = "NestingThreshold"

    stringValueToMatch = "   value:"
    
    global resultL
    global resultB
    global resultN
    #### here we gave the function the third position of sys arguments when you should put the file path of .clang-tidy cofig.
    with open(sys.argv[2],"r") as f:
       
            while True:
                line1 = f.readline()
                line2 = f.readline()
               
                if stringLineToMatch in line1 and stringValueToMatch in line2:
                    elementsLineThres= line2.split("   value:        '", 1)
                    matchedEndLine = "'"
                    if matchedEndLine in line2:
                       new2 = elementsLineThres[1].split(matchedEndLine,1)
                       resultL=new2[0].strip()
                      # print(resultL)

                if stringBranchToMatch in line1 and stringValueToMatch in line2:
                    elementsBranchThres= line2.split("   value:        '", 1)
                    matchedEndBranch = "'"
                    if matchedEndBranch in line2:
                       new2 = elementsBranchThres[1].split(matchedEndBranch,1)
                       resultB=new2[0].strip()
                       #print(resultB)

                if stringNestingToMatch in line1 and stringValueToMatch in line2:
                    elementsNestingThres= line2.split("   value:        '", 1)
                    matchedEndNesting = "'"
                    if matchedEndNesting in line2:
                       new2 = elementsNestingThres[1].split(matchedEndNesting,1)
                       resultN=new2[0].strip()
                       #print(resultN)      
                if not line2: break


################## read from file the line then find the specific string of warning functions to write all the result line to another file
def readFileAndFindWarningFunctions():
   
    ##get the name of the warning functions by this string
    WarningFunctions = "warning: function"
    matchedLineF = ''
    ##get the notes of the warning functions by this string
    NoteOfTheFunctionsThresholds ="note:"
   
    result = []
    result2 = []
    result3 = []
    result4 = []

    listResult = []
   
    matchedline=''
    matchednesting=''
    matchedbranch=''
  
    ffinal =''
    flag2 =False
    i = 1
    re = ''
     
    ##### this to call the method which get the specific string from .clang-tidy config 
    readClangConfig()
    ##### then apply it here global variables in the below string for the final report
    listResult.append('\nClang Tidy Reporting for Kiso functions.. \n'
         +'The functions exceed recommended size/complexity thresholds [readability-function-size]:\n'
         + 'Thresholds: LineThresholods > '+resultL+' | BranchThresholds > '+resultB+' | NestingThresholds > '+resultN+'\n'
         + '--------------------------------------------------------------------------------')
    
    #### here when you run your python script file path and with the .txt file path 
    #### this sys.argv[1] give you the .txt file path from the command you will run with the python script file path       
    with open(sys.argv[1],"r") as f:
        for line in f:
            if WarningFunctions in line:
                matchedLineF = line
                elementsNameOfFunctions= matchedLineF.split('warning: ', 1)
                
                if len(WarningFunctions)<2: 
                    print("there are no warning functions")
                else:
                    new = elementsNameOfFunctions[1].split('exceeds',1)
                    result=new[0].strip()
                    re = 'Function ' + str(i)
                    listResult.append('\n')
                    listResult.append(re)
                    listResult.append('------------')
                    listResult.append(result+':')
                    flag2 =True
                    i = i+1
            elif NoteOfTheFunctionsThresholds in line:
                matchedLineF = line  
                elementsNameOfFunctions = matchedLineF.split('note:',1) 
                if len(NoteOfTheFunctionsThresholds)<2:
                     print("there are no notes for warning functions")
                else:    
                    matchedline ='including whitespace and comments (threshold '+resultL+')'
                    matchednesting ='starts here (threshold '+resultN+')'
                    matchedbranch=' (threshold '+resultB+')'
                    if matchedline in matchedLineF:
                       new2 = elementsNameOfFunctions[1].split(matchedline,1)
                       result2=new2[0].strip()
                       listResult.append(result2)

                    if matchedbranch in matchedLineF:
                        new4 = elementsNameOfFunctions[1].split(matchedbranch,1)
                        result4=new4[0].strip()
                        listResult.append(result4)  

                    if matchednesting in matchedLineF and flag2== True:
                        new3 = elementsNameOfFunctions[1].split(matchednesting,1)
                        result3=new3[0].strip()
                        listResult.append(result3)
                        flag2= False 
                    
                    
            ffinal = '\n'.join(listResult)
        writeText(ffinal)
        print(ffinal+'\n')

#### here it will call the function will do the final report 
readFileAndFindWarningFunctions()        
       