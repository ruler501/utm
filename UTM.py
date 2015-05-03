import math
import operator
from collections import deque

moveright = """moveright{{i}}mv{{j}},0
moveright{{i}}mv{{j}},0,>

moveright{{i}}mv{{j}},1
moveright{{i}}mv{{j}},1,>\n\n"""

moveleft = """moveleft{{i}}mv{{j}},0
moveleft{{i}}mv{{j}},0,<

moveleft{{i}}mv{{j}},1
moveleft{{i}}mv{{j}},1,<\n\n"""

variables = {'i': 0}
curPos = 0

def moveV(pos,nextstate,movedirection,i):
    global curPos
    outStr = ""
    if pos > curPos:
        if pos - curPos > 1:
            outStr += "moveright0mv"+str(i)+",_\n"
            outStr += nextstate+",_,"+movedirection+'\n\n'
            outStr += moveright.replace("{{i}}","0").replace("{{j}}",str(i))
        for j in range(1,pos-curPos):
            outStr += "moveright"+str(j)+"mv"+str(i)+",_\n"
            outStr += "moveright"+str(j-1)+"mv"+str(i)+',_,>\n\n'
            outStr += moveright.replace("{{i}}",str(j)).replace("{{j}}",str(i))
        outStr += "start"+str(i)+",_\n"
        if pos - curPos > 1:
            outStr += "moveright"+str(pos-curPos-2)+"mv"+str(i)+",_,>\n\n"
        else:
            outStr += nextstate+",_,"+movedirection+'\n\n'
        outStr += "start"+str(i)+",0\n"
        outStr += "start"+str(i)+",0,>\n\n"
        outStr += "start"+str(i)+",1\n"
        outStr += "start"+str(i)+",1,>\n\n"
    elif pos < curPos:
        curPos += 1
        if curPos-pos > 1:
            outStr += "moveleft0mv"+str(i)+",_\n"
            outStr += nextstate+",_,"+movedirection+'\n\n'
            outStr += moveleft.replace("{{i}}","0").replace("{{j}}",str(i))
        for j in range(1,curPos-pos):
            outStr += "moveleft"+str(j)+"mv"+str(i)+",_\n"
            outStr += "moveleft"+str(j-1)+"mv"+str(i)+',_,<\n\n'
            outStr += moveleft.replace("{{i}}",str(j)).replace("{{j}}",str(i))
        outStr += "start"+str(i)+",_\n"
        if curPos-pos > 1:
            outStr += "moveleft"+str(curPos-pos-2)+"mv"+str(i)+",_,<\n\n"
        else:
            outStr += nextstate+",_,"+movedirection+'\n\n'
        outStr += "start"+str(i)+",0\n"
        outStr += "start"+str(i)+",0,<\n\n"
        outStr += "start"+str(i)+",1\n"
        outStr += "start"+str(i)+",1,<\n\n"
    else:
        outStr += "start"+str(i)+",_\n"
        outStr += nextstate+",_,"+movedirection+"\n\n"
        outStr += "start"+str(i)+",0\n"
        outStr += "start"+str(i)+",0,<\n\n"
        outStr += "start"+str(i)+",1\n"
        outStr += "start"+str(i)+",1,<\n\n"
    curPos = pos
    return outStr

def copyOverV(opos, newpos, nextstate, i):
    global curPos
    outStr = ""
    if newpos <= curPos:
        outStr = moveV(newpos,"startcve"+str(i),">",i)
        curPos = newpos
    else:
        outStr = moveV(newpos,"startcve"+str(i),">",i)
        curPos = newpos
    if opos <= curPos:
        outStr += moveV(opos,"startcv"+str(i),">","r"+str(i))
    else:
        outStr += moveV(opos,"startcv"+str(i),">","r"+str(i))
    curPos = newpos
    outStr += moveV(opos,"startcvc0"+str(i),"-","c0m"+str(i))
    curPos = newpos
    outStr += moveV(opos,"startcvc1"+str(i),"-","c1m"+str(i))
    
    outStr += "startcve"+str(i)+",0\n"
    if opos <= curPos:
        outStr += "startr"+str(i)+",_,<\n\n"
    else:
        outStr += "startr"+str(i)+",_,>\n\n"
    outStr += "startcve"+str(i)+",1\n"
    if opos <= curPos:
        outStr += "startr"+str(i)+",_,<\n\n"
    else:
        outStr += "startr"+str(i)+",_,>\n\n"
    outStr += "startcvec1"+str(i)+",_\n"
    if opos <= curPos:
        outStr += "startc1m"+str(i)+",_,<\n\n"
    else:
        outStr += "startc1m"+str(i)+",_,>\n\n"
    outStr += "startcvec1"+str(i)+",0\n"
    if opos <= curPos:
        outStr += "startc1m"+str(i)+",_,<\n\n"
    else:
        outStr += "startc1m"+str(i)+",_,>\n\n"
    outStr += "startcvec1"+str(i)+",1\n"
    if opos <= curPos:
        outStr += "startc1m"+str(i)+",_,<\n\n"
    else:
        outStr += "startc1m"+str(i)+",_,>\n\n"
    outStr += "startcvec0"+str(i)+",_\n"
    if opos <= curPos:
        outStr += "startc1m"+str(i)+",_,<\n\n"
    else:
        outStr += "startc1m"+str(i)+",_,>\n\n"
    outStr += "startcvec0"+str(i)+",0\n"
    if opos <= curPos:
        outStr += "startc0m"+str(i)+",_,<\n\n"
    else:
        outStr += "startc0m"+str(i)+",_,>\n\n"
    outStr += "startcvec0"+str(i)+",1\n"
    if opos <= curPos:
        outStr += "startc0m"+str(i)+",_,<\n\n"
    else:
        outStr += "startc0m"+str(i)+",_,>\n\n"
    outStr += "startcv"+str(i)+",_\n"
    outStr += nextstate+",_,>\n\n"
    outStr += "startcv"+str(i)+",0\n"
    outStr += "copyright"+str(newpos-opos)+"cv"+str(i)+"c0,_,>\n\n"
    outStr += "startcv"+str(i)+",1\n"
    outStr += "copyright"+str(newpos-opos)+"cv"+str(i)+"c1,_,>\n\n"
    outStr += "startcvc0"+str(i)+",_\n"
    outStr += "startcv"+str(i)+",0,>\n\n"
    outStr += "startcvc1"+str(i)+",_\n"
    outStr += "startcv"+str(i)+",1,>\n\n"
    outStr += "copyright0cv"+str(i)+"c1,_\n"
    outStr += "startcvec1"+str(i)+",1,>\n\n"
    outStr += "copyright0cv"+str(i)+"c1,0\n"
    outStr += "copyright0cv"+str(i)+"c1,0,>\n\n"
    outStr += "copyright0cv"+str(i)+"c1,1\n"
    outStr += "copyright0cv"+str(i)+"c1,1,>\n\n"
    outStr += "copyright0cv"+str(i)+"c0,_\n"
    outStr += "startcvec0"+str(i)+",0,>\n\n"
    outStr += "copyright0cv"+str(i)+"c0,0\n"
    outStr += "copyright0cv"+str(i)+"c0,0,>\n\n"
    outStr += "copyright0cv"+str(i)+"c0,1\n"
    outStr += "copyright0cv"+str(i)+"c0,1,>\n\n"
    for j in range(1,newpos-opos+1):
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,_\n"
        outStr += "copyright"+str(j-1)+"cv"+str(i)+"c1,_,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,0\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,0,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,1\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,1,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,_\n"
        outStr += "copyright"+str(j-1)+"cv"+str(i)+"c0,_,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,0\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,0,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,1\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,1,>\n\n"
    curPos = opos+1
    return outStr
    
def copyV(opos, newpos, nextstate, i):
    global curPos
    outStr = ""
    if opos <= curPos:
        outStr = moveV(opos,"startcv"+str(i),">",i)
    elif opos > curPos:
        outStr = moveV(opos,"startcv"+str(i),">",i)
    curPos = newpos+1
    outStr += moveV(opos+1,"startcvc0"+str(i),"-","c0m"+str(i))
    curPos = newpos+1
    outStr += moveV(opos+1,"startcvc1"+str(i),"-","c1m"+str(i))

    outStr += "startcv"+str(i)+",_\n"
    outStr += nextstate+",_,>\n\n"
    outStr += "startcv"+str(i)+",0\n"
    outStr += "copyright"+str(newpos-opos)+"cv"+str(i)+"c0,_,>\n\n"
    outStr += "startcv"+str(i)+",1\n"
    outStr += "copyright"+str(newpos-opos)+"cv"+str(i)+"c1,_,>\n\n"
    outStr += "startcvc0"+str(i)+",_\n"
    outStr += "startcv"+str(i)+",0,>\n\n"
    outStr += "startcvc1"+str(i)+",_\n"
    outStr += "startcv"+str(i)+",1,>\n\n"
    outStr += "copyright0cv"+str(i)+"c1,_\n"
    outStr += "startc1m"+str(i)+",1,<\n\n"
    outStr += "copyright0cv"+str(i)+"c1,0\n"
    outStr += "copyright0cv"+str(i)+"c1,0,>\n\n"
    outStr += "copyright0cv"+str(i)+"c1,1\n"
    outStr += "copyright0cv"+str(i)+"c1,1,>\n\n"
    outStr += "copyright0cv"+str(i)+"c0,_\n"
    outStr += "startc0m"+str(i)+",0,<\n\n"
    outStr += "copyright0cv"+str(i)+"c0,0\n"
    outStr += "copyright0cv"+str(i)+"c0,0,>\n\n"
    outStr += "copyright0cv"+str(i)+"c0,1\n"
    outStr += "copyright0cv"+str(i)+"c0,1,>\n\n"
    for j in range(1,newpos-opos+1):
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,_\n"
        outStr += "copyright"+str(j-1)+"cv"+str(i)+"c1,_,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,0\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,0,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,1\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c1,1,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,_\n"
        outStr += "copyright"+str(j-1)+"cv"+str(i)+"c0,_,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,0\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,0,>\n\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,1\n"
        outStr += "copyright"+str(j)+"cv"+str(i)+"c0,1,>\n\n"
    curPos = opos+1
    return outStr
    
def copyVresize(opos, newpos, resize, nextstate, i):
    global curPos
    outStr = moveV(newpos, "startcvr"+str(i), ">", i)
    outStr += "startcvr"+str(i)+",0\n"
    if resize > 1:
        outStr += "out"+str(resize-2)+"c0"+str(i)+",0,>\n\n"
    else:
        outStr += "startc"+str(i)+",0,-\n\n"
    outStr += "startcvr"+str(i)+",1\n"
    if resize > 1:
        outStr += "out"+str(resize-2)+"c0"+str(i)+",0,>\n\n"
    else:
        outStr += "startc"+str(i)+",0,-\n\n"
    outStr += "startcvr"+str(i)+",_\n"
    if resize > 1:
        outStr += "out"+str(resize-2)+"c0"+str(i)+",0,>\n\n"
        outStr += "out0c0"+str(i)+",_\n"
        outStr += "startc"+str(i)+",0,-\n\n"
        outStr += "out0c0"+str(i)+",0\n"
        outStr += "startc"+str(i)+",0,-\n\n"
        outStr += "out0c0"+str(i)+",1\n"
        outStr += "startc"+str(i)+",0,-\n\n"
    else:
        outStr += "startc"+str(i)+",0,-\n\n"
    for j in range(1,resize):
        outStr += "out"+str(j)+"c0"+str(i)+",_\n"
        outStr += "out"+str(j-1)+"c0"+str(i)+",0,>\n\n"
        outStr += "out"+str(j)+"c0"+str(i)+",0\n"
        outStr += "out"+str(j-1)+"c0"+str(i)+",0,>\n\n"
        outStr += "out"+str(j)+"c0"+str(i)+",1\n"
        outStr += "out"+str(j-1)+"c0"+str(i)+",0,>\n\n"
    curPos = newpos
    if newpos in variables.values():
        outStr += copyOverV(opos,newpos,nextstate,"c"+str(i))
    else:
        outStr += copyV(opos,newpos,nextstate,"c"+str(i))
    return outStr

def copyVself(opos, resize, nextstate, i):
    global curPos
    outStr = moveV(opos,"startcvs"+str(i),">",i)
    outStr += "startcvs"+str(i)+",0\n"
    outStr += "startcvs"+str(i)+",0,>\n\n"
    outStr += "startcvs"+str(i)+",1\n"
    outStr += "startcvs"+str(i)+",0,>\n\n"
    outStr += "startcvs"+str(i)+",_\n"
    if resize > 1:
        outStr += "fillzeroes"+str(resize-2)+str(i)+",0,>\n\n"
        outStr += "fillzeroes0"+str(i)+",_\n"
        outStr += nextstate+",0,-\n\n"
        for j in range(1,resize-1):
            outStr += 'fillzeroes'+str(j)+str(i)+",_\n"
            outStr += 'fillzeroes'+str(j-1)+str(i)+",0,>\n\n"
    else:
        if resize < 1:
            outStr += nextstate+",_,<\n\n"
        else:
            outStr += nextstate+",0,-\n\n"
    return outStr

def outputConstant(pos,nextstate,constant,i,width):
    global curPos
    outStr = moveV(pos,"starto"+str(i),">",i)
    b = '{:0{width}b}'.format(constant%(2**width), width=width)
    outStr += "starto"+str(i)+",_\n"
    if len(b) > 1:
        outStr += "output1c"+b[1]+str(i)+","+b[0]+",>\n\n"
    else:
        outStr += nextstate+","+b[0]+",-\n\n"
    outStr += "starto"+str(i)+",0\n"
    outStr += "output1c"+b[1]+str(i)+","+b[0]+",>\n\n"
    outStr += "starto"+str(i)+",1\n"
    outStr += "output1c"+b[1]+str(i)+","+b[0]+",>\n\n"
    for j in range(1,len(b)-1):
        outStr += "output"+str(j)+"c"+b[j]+str(i)+",_\n"
        outStr += "output"+str(j+1)+"c"+b[j+1]+str(i)+","+b[j]+",>\n\n"
        outStr += "output"+str(j)+"c"+b[j]+str(i)+",0\n"
        outStr += "output"+str(j+1)+"c"+b[j+1]+str(i)+","+b[j]+",>\n\n"
        outStr += "output"+str(j)+"c"+b[j]+str(i)+",1\n"
        outStr += "output"+str(j+1)+"c"+b[j+1]+str(i)+","+b[j]+",>\n\n"
    if len(b) > 1:
        outStr += "output"+str(len(b)-1)+"c"+b[-1]+str(i)+",_\n"
        outStr += nextstate+","+b[-1]+",-\n\n"
        outStr += "output"+str(len(b)-1)+"c"+b[len(b)-1]+str(i)+",0\n"
        outStr += nextstate+","+b[-1]+",-\n\n"
        outStr += "output"+str(len(b)-1)+"c"+b[len(b)-1]+str(i)+",1\n"
        outStr += nextstate+","+b[-1]+",-\n\n"
    curPos = pos
    return outStr
    
def deleteVar(pos,nextstate,i):
    global curPos
    outStr = moveV(pos+1,"startd"+str(i),"<",i)
    outStr += "startd"+str(i)+",_\n"
    outStr += nextstate+",_,<\n\n"
    outStr += "startd"+str(i)+",0\n"
    outStr += "startd"+str(i)+",_,<\n\n"
    outStr += "startd"+str(i)+",1\n"
    outStr += "startd"+str(i)+",_,<\n\n"
    curPos = pos
    return outStr

def increment(pos,nextstate,errorstate,i):
    global curPos
    outStr = moveV(pos+1,"starti"+str(i),"<",i)
    outStr += "starti"+str(i)+",_\n"
    outStr += errorstate+",_,>\n\n"
    outStr += "starti"+str(i)+",0\n"
    outStr += nextstate+",1,-\n\n"
    outStr += "starti"+str(i)+",1\n"
    outStr += "starti"+str(i)+",0,<\n\n"
    curPos = pos
    return outStr

def decrement(pos,nextstate,errorstate,i):
    global curPos
    outStr = moveV(pos+1,"startd"+str(i),"<",i)
    outStr += "startd"+str(i)+",_\n"
    outStr += errorstate+",_,>\n\n"
    outStr += "startd"+str(i)+",0\n"
    outStr += "startd"+str(i)+",1,<\n\n"
    outStr += "startd"+str(i)+",1\n"
    outStr += nextstate+",0,-\n\n"
    curPos = pos
    return outStr

def pop(pos,nextstate,errorstate,i):
    global curPos
    if pos in popped:
        return pope(pos,nextstate,errorstate,i)
    outStr = moveV(pos+1,"startp"+str(i),"<",i)
    outStr += "startp"+str(i)+",0\n"
    outStr += "checkp"+str(i)+",_,<\n\n"
    outStr += "startp"+str(i)+",1\n"
    outStr += "checkp"+str(i)+",_,<\n\n"
    outStr += "checkp"+str(i)+",_\n"
    outStr += errorstate+",_,>\n\n"
    outStr += "checkp"+str(i)+",0\n"
    outStr += nextstate+",0,-\n\n"
    outStr += "checkp"+str(i)+",1\n"
    outStr += nextstate+",1,-\n\n"
    for k in variables:
        if variables[k] > pos:
            variables[k] += 1
    for i in range(len(popped)):
        if popped[i] > pos:
            popped[i] += 1
    curPos = pos
    popped.append(pos)
    return outStr

def pope(pos,nextstate,errorstate,i):
    global curPos
    outStr = moveV(pos+1,"startpp"+str(i),"-",i)
    outStr += "startpp"+str(i)+",_\n"
    outStr += "startp"+str(i)+",0,<\n\n"
    outStr += "startp"+str(i)+",0\n"
    outStr += "checkp"+str(i)+",_,<\n\n"
    outStr += "startp"+str(i)+",1\n"
    outStr += "checkp"+str(i)+",_,<\n\n"
    outStr += "checkp"+str(i)+",_\n"
    outStr += errorstate+",_,>\n\n"
    outStr += "checkp"+str(i)+",0\n"
    outStr += nextstate+",0,-\n\n"
    outStr += "checkp"+str(i)+",1\n"
    outStr += nextstate+",1,-\n\n"
    curPos = pos
    return outStr
    
def firstOne(pos,nextstate,errorstate,i):
    global curPos
    ourStr = moveV(pos,"startp"+str(i),">",i)
    ourStr += "startp"+str(i)+",0\n"
    ourStr += nextstate+",1,-\n\n"
    ourStr += "startp"+str(i)+",1\n"
    ourStr += "startp"+str(i)+",1,>\n\n"
    ourStr += "startp"+str(i)+",_\n"
    ourStr += errorstate+",_,<\n\n"
    
inFile = open("UTM.utm")
out = open("UTM.utmo","w")
functions = {'incr': increment, 'decr': decrement, "pop": pop, "first": firstOne}
popped = []
inLines=inFile.readlines()#[:-1]

out.write("name: Auto-Generated\ninit: start0\naccept: end\n\n")

i=0
whileLoops = deque()
for lineno in range(len(inLines)):
    line = inLines[lineno].strip()
    if line == "}":
        for loop in whileLoops:
            if lineno == loop[2]+1:
                loopVariables = {}
                for var in loop[6]:
                    loopVariables[var] = variables[var]
                sorted_vars = sorted(loopVariables.items(),key=operator.itemgetter(1),reverse=True)
                if len(sorted_vars) > 0:
                    if len(sorted_vars) > 1:
                        if loop[4] == "pop":
                            curPos += 1
                        out.write(deleteVar(sorted_vars[0][1], "start"+sorted_vars[1][0]+str(i), str(i)))
                        if loop[4] == "pop":
                            curPos += 1
                        out.write(deleteVar(sorted_vars[-1][1], "startnp"+str(loop[1]), sorted_vars[-1][0]+str(i)))
                        del variables[sorted_vars[0][0]]
                        del variables[sorted_vars[-1][0]]
                    else:
                        if loop[4] == "pop":
                            curPos += 1
                        out.write(deleteVar(sorted_vars[0][1], "startnp"+str(loop[1]), str(i)))
                    for var in range(1,len(sorted_vars)-1):
                        if loop[4] == "pop":
                            curPos += 1
                        out.write(deleteVar(sorted_vars[var][1], "start"+sorted_vars[var+1][0]+str(i), sorted_vars[var][0]+str(i)))
                        del variables[sorted_vars[var][0]]
                curPos=loop[3]
        i += 1
        continue
    if line[:5] == "while":
        pieces = line.split()
        if pieces[1] not in variables:
            raise NameError(pieces[1]+" is not a defined variable")
        vposition = variables[pieces[1]]    
        function = pieces[2]
        counter = pieces[3][:-1]
        count = 1
        nested = False
        for endno in range(lineno+1,len(inLines)):
            if '{' in inLines[endno]:
                count += 1
            if inLines[endno].strip() == "}":
                count -= 1
                if count == 0:
                    for loop in whileLoops:
                        if loop[1] < i and loop[2] > i:
                            nested = True
                    nested = True
                    whileLoops.append([len(whileLoops), lineno, endno-1, vposition, function, nested, []])  
                    if nested:
                        if endno == len(inLines) - 1:
                            out.write(functions[function](vposition, "start"+str(i+1), "end",i))
                        else:
                            out.write(functions[function](vposition, "start"+str(i+1), "start"+str(endno),i))
                    curPos=vposition
                    break
        else:
            raise SyntaxError("While loop never finished")
        i+=1
        continue
    if "=" in line:
        pieces = line.split("=")
        variable = pieces[1]
        for loop in whileLoops:
            if i > loop[1] and i < loop[2] and loop[4]=="pop":
                curPos -= 1
        if variable not in variables:
            if "," in variable:
                try:
                    allocatedSpace = int(variable.split(',')[1])
                    if variable.split(',')[0] in variables:
                        if pieces[0] not in variables:
                            variables[pieces[0]] = max(variables.items(), key=operator.itemgetter(1))[1]+1
                            for loop in whileLoops:
                                if i > loop[1] and i < loop[2]:
                                    loop[6].append(pieces[0])
                        if variable.split(',')[0] == pieces[0]:
                            if i == len(inLines) - 1:
                                out.write(copyVself(variables[pieces[0]],variables[variable.split(',')[0]],allocatedSpace,"end",i))
                            else:
                                out.write(copyVself(variables[pieces[0]],allocatedSpace,"start"+str(i+1),i))
                        else:
                            if i == len(inLines) - 1:
                                out.write(copyVresize(variables[variable.split(',')[0]],variables[pieces[0]],allocatedSpace,"end",i))
                            else:
                                out.write(copyVresize(variables[variable.split(',')[0]],variables[pieces[0]],allocatedSpace,"start"+str(i+1),i))
                        i+=1
                        continue
                    else:
                        constant = int(variable.split(',')[0])
                        if pieces[0] not in variables:
                            variables[pieces[0]] = max(variables.items(), key=operator.itemgetter(1))[1]+1
                            for loop in whileLoops:
                                if i > loop[1] and i < loop[2]:
                                    loop[6].append(pieces[0])
                        if lineno == len(inLines) - 1:
                            out.write(outputConstant(variables[pieces[0]],"end",constant,i,allocatedSpace))
                        else:
                            out.write(outputConstant(variables[pieces[0]],"start"+str(i+1),constant,i,allocatedSpace))
                        i+=1
                        continue
                        
                except ValueError:
                    raise NameError(variable+" is not a defined variable")
            else:
                raise NameError(variable+" is not a defined variable")
        if pieces[0] not in variables:
            variables[pieces[0]] = max(variables.items(), key=operator.itemgetter(1))[1]+1
            if lineno == len(inLines) - 1:
                out.write(copyV(variables[variable],variables[pieces[0]],"end",i))
            else:
                out.write(copyV(variables[variable],variables[pieces[0]],"start"+str(i+1),i))
        else:
            if lineno == len(inLines) - 1:
                out.write(copyOverV(variables[variable],variables[pieces[0]],"end",i))
            else:
                out.write(copyOverV(variables[variable],variables[pieces[0]],"start"+str(i+1),i))
        i += 1
        continue
    function = line.split('(')[0]
    variable = line.split('(')[1][:-1]
    if variable not in variables:
        raise NameError(variable+" is not a defined variable")
    for loop in whileLoops:
        if lineno == loop[2]:
            if loop[5]:
                if loop[4] == "pop":
                    a = curPos
                    if curPos <= loop[3]:
                        curPos -= 1
                    out.write(functions[function](variables[variable], "start"+str(loop[2]+1), "start"+str(loop[2]+1), i))
                    for var in loop[6]:
                        if variables[var] < curPos:
                            curPos = variables[var]
                    t = curPos
                    out.write(functions[loop[4]](loop[3], "start"+str(loop[1]+1), "start"+str(loop[2]+2),"n"+str(loop[1])))
                    curPos = t
                    out.write(pope(loop[3], "start"+str(loop[1]+1), "start"+str(loop[2]+2),"np"+str(loop[1])))
                else:
                    out.write(functions[function](variables[variable], "startn"+str(loop[1]), "start"+str(loop[1]), i))
                    out.write(functions[loop[4]](loop[3], "start"+str(loop[1]+1), "start"+str(loop[2]+2),"n"+str(loop[1])))
                break
            else:
                if loop[4] == "pop":
                    a = curPos
                    if curPos <= loop[3]:
                        curPos -= 1
                    out.write(functions[function](variables[variable], "start"+str(loop[2]+1), "start"+str(loop[2]+1), i))
                    t = curPos
                    curPos = a
                    if endno == len(inLines) - 1:
                        out.write(functions[loop[4]](loop[3], "start"+str(loop[1]+1), "end",loop[1]))
                        curPos = t+1
                        out.write(pope(loop[3], "start"+str(loop[1]+1), "end","np"+str(loop[1])))
                    else:
                        out.write(functions[loop[4]](loop[3], "start"+str(loop[1]+1), "start"+str(loop[2]+2),loop[1]))
                        curPos = t+1
                        out.write(pope(loop[3], "start"+str(loop[1]+1), "start"+str(loop[2]+2),"np"+str(loop[1])))
                    break

                else:
                    out.write(functions[function](variables[variable], "start"+str(loop[1]), "start"+str(loop[1]), i))
                    if endno == len(inLines) - 1:
                        out.write(functions[loop[4]](loop[3], "start"+str(loop[1]+1), "end",loop[1]))
                    else:
                        out.write(functions[loop[4]](loop[3], "start"+str(loop[1]+1), "start"+str(loop[2]+2),loop[1]))
                    break
    else:
        for loop in whileLoops:
            if i > loop[1] and i < loop[2] and loop[4]=="pop":
                curPos -= 1
                print(curPos)
        if lineno == len(inLines)-1:
            out.write(functions[function](variables[variable], "end", "end", i))
        else:
            out.write(functions[function](variables[variable], "start"+str(i+1), "start"+str(i+1), i))
    i += 1
