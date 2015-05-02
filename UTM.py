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
    vposition = max(variables.items(), key=operator.itemgetter(1))[1]+1
    outStr = ""
    variables["mv"+str(i)] = vposition
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
        outStr += "moveleft0mv"+str(i)+",_\n"
        outStr += nextstate+",_,"+movedirection+'\n\n'
        outStr += moveleft.replace("{{i}}","0").replace("{{j}}",str(i))
        for j in range(1,curPos-pos):
            outStr += "moveleft"+str(j)+"mv"+str(i)+",_\n"
            outStr += "moveleft"+str(j-1)+"mv"+str(i)+',_,<\n\n'
            outStr += moveleft.replace("{{i}}",str(j)).replace("{{j}}",str(i))
        outStr += "start"+str(i)+",_\n"
        outStr += "moveleft"+str(curPos-pos-2)+"mv"+str(i)+",_,<\n\n"
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
    vposition = max(variables.items(), key=operator.itemgetter(1))[1]+1
    outStr = ""
    if opos <= curPos:
        outStr = moveV(opos,"startcv"+str(i),">",i)
    elif opos > curPos:
        outStr = moveV(opos,"startcv"+str(i),"<",i)
    curPos = newpos+1
    outStr += moveV(opos,"startcvc0"+str(i),"-","c0m"+str(i))
    curPos = newpos+1
    outStr += moveV(opos,"startcvc1"+str(i),"-","c1m"+str(i))
    variables["cv"+str(i)] = newpos
    if newpos > opos:
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

i=0
whileLoops = deque()
for lineno in range(len(inLines)):
    line = inLines[lineno].strip()
    if line == "}":
        continue
    if line[:5] == "while":
        pieces = line.split()
        if pieces[1] not in variables:
            raise NameError(pieces[1]+" is not a defined variable")
        vposition = variables[pieces[1]]    
        function = pieces[2]
        counter = pieces[3][:-1]
        for endno in range(lineno+1,len(inLines)):
            if inLines[endno] == "}":
                whileLoops.append((len(whileLoops), lineno, endno-1, counter))
                out.write(functions[function](vposition, "start"+str(i+1), "start"+str(endno+1),i))
                break
        else:
            raise SyntaxError("While loop never finished")
        i+=1
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
            out.write(functions[function](variables[variable], "start"+str(loop[1]), "reject", i))
            break
    else:
        out.write(functions[function](variables[variable], "start"+str(i+1), "reject", i))
    i += 1
    