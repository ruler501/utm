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
#validVariables = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
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
    
def copyV(opos, newpos, nextstate, i):
    global curPos
    outStr = ""
    if opos <= curPos:
        outStr = moveV(opos-1,"startcv"+str(i),">",i)
    elif opos > curPos:
        outStr = moveV(opos,"startcv"+str(i),"<",i)
    curPos = newpos+1
    outStr += moveV(opos,"startcvc0"+str(i),"-","c0m"+str(i))
    curPos = newpos+1
    outStr += moveV(opos,"startcvc1"+str(i),"-","c1m"+str(i))

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
    outStr += "startcvr"+str(i)+",_\n"
    if resize > 1:
        outStr += "out"+str(resize-2)+"c0"+str(i)+",0,>\n\n"
        outStr += "out0c0"+str(i)+",_\n"
        outStr += "startc"+str(i)+",0,-\n\n"
    else:
        outStr += "startc"+str(i)+",0,-\n\n"
    for j in range(1,resize):
        outStr += "out"+str(j)+"c0"+str(i)+",_\n"
        outStr += "out"+str(j-1)+"c0"+str(i)+",0,>\n\n"
    curPos = newpos
    outStr += copyV(opos,newpos,nextstate,"c"+str(i))
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
    
inFile = open("UTM.utm")
out = open("UTM.utmo","w")
functions = {'incr': increment, 'decr': decrement}
inLines=inFile.readlines()

out.write("name: Auto-Generated\ninit: start0\naccept: end\n\n")

i=0
whileLoops = deque()
for lineno in range(len(inLines)):
    line = inLines[lineno].strip()
    if line == "}":
        i += 1
        continue
    if line[:5] == "while":
        pieces = line.split()
        if pieces[1] not in variables:
            raise NameError(pieces[1]+" is not a defined variable")
        vposition = variables[pieces[1]]    
        function = pieces[2]
        counter = pieces[3][:-1]
        for endno in range(lineno+1,len(inLines)):
            if inLines[endno].strip() == "}":
                whileLoops.append((len(whileLoops), lineno, endno-1, counter))
                if endno == len(inLines) - 1:
                    out.write(functions[function](vposition, "start"+str(i+1), "end",i))
                else:
                    out.write(functions[function](vposition, "start"+str(i+1), "start"+str(endno+1),i))
                break
        else:
            raise SyntaxError("While loop never finished")
        i+=1
        continue
    if "=" in line:
        pieces = line.split("=")
        if pieces[0] in variables:
            raise NameError("Can't copy over an existing variable, "+pieces[0]+" already exists")
        variable = pieces[1]
        if variable not in variables:
            if "," in variable:
                try:
                    allocatedSpace = int(variable.split(',')[1])
                    if variable.split(',')[0] in variables:
                        variables[pieces[0]] = max(variables.items(), key=operator.itemgetter(1))[1]+1
                        if i == len(inLines) - 1:
                            out.write(copyVresize(variables[variable.split(',')[0]],variables[pieces[0]],allocatedSpace,"end",i))
                        else:
                            out.write(copyVresize(variables[variable.split(',')[0]],variables[pieces[0]],allocatedSpace,"start"+str(i+1),i))
                        i+=1
                        continue
                    else:
                        raise NameError(variable.split(',')[0]+" is not a defined variable")
                except ValueError:
                    raise NameError(variable+" is not a defined variable")
            else:
                raise NameError(variable+" is not a defined variable")
        variables[pieces[0]] = max(variables.items(), key=operator.itemgetter(1))[1]+1
        if i == len(inLines) - 1:
            out.write(copyV(variables[variable],variables[pieces[0]],"end",i))
        else:
            out.write(copyV(variables[variable],variables[pieces[0]],"start"+str(i+1),i))
        i += 1
        continue
    function = line.split('(')[0]
    variable = line.split('(')[1][:-1]
    if variable not in variables:
        for loop in whileLoops:
            if loop[3]+variable in variables:
                variable = loop[3]+variable
                break
        else:
            raise NameError(variable+" is not a defined variable")
    for loop in whileLoops:
        if i == loop[2]:
            out.write(functions[function](variables[variable], "start"+str(loop[1]), "start"+str(loop[1]), i))
            break
    else:
        if lineno == len(inLines)-1:
            out.write(functions[function](variables[variable], "end", "end", i))
        else:
            out.write(functions[function](variables[variable], "start"+str(i+1), "start"+str(i+1), i))
    i += 1
    