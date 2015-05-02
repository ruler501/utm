subRoutine = """sub0,_
sub0,_,>

sub0,1
sub1,_,>

sub1,_
sub2,_,>

sub1,1
sub1,1,>

sub2,_
sub3,_,<

sub2,1
sub2,1,>

sub3,_
end,1,-

sub3,1
sub4,_,<

sub4,_
end,_,-

sub4,1
sub5,1,<

sub5,_
sub6,_,<

sub5,1
sub5,1,<

sub6,_
end,1,-

sub6,1
sub7,1,<

sub7,_
sub0,_,>

sub7,1
sub7,1,<"""

moveright = """moveright{{i}}cv{{j}},0
moveright{{i}}cv{{j}},0,>

moveright{{i}}cv{{j}},1
moveright{{i}}cv{{j}},1,>\n\n"""

moveleft = """movelef{{i}}cv{{j}},0
moveleft{{i}}cv{{j}},0,>

moveleft{{i}}cv{{j}},1
moveleft{{i}}cv{{j}},1,>\n\n"""

variables = {'i': 0}
#validVariables = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
curPos = 0

def moveV(pos,nextstate,movedirection):
    vposition = max(variables,key=variables.get)+1
    vnum = 0
    outStr = ""
    while "cv"+str(vnum) in variables:
        vnum += 1
    variables["cv"+str(vnum)] = vposition
    if pos > curPos:
        outStr += "moveright1cv"+str(vnum)+",_\n"
        outStr += nextstate+",_,"+movedirection+'\n\n'
        outStr += moveright.replace("{{i}}","1").replace("{{j}}",str(vnum))
        for i in range(2,pos-curPos):
            outStr += "moveright"+str(i)+"cv"+str(vnum)+",_\n"
            outStr += "moveright"+str(i-1)+"cv"+str(vnum)+',_,>\n\n'
            outStr += moveright.replace("{{i}}",str(i)).replace("{{j}}",str(vnum))
    elif pos < curPos:
        outStr += "moveleft1cv"+str(vnum)+",_\n"
        outStr += nextstate+",_,"+movedirection+'\n\n'
        outStr += moveleft.replace("{{i}}","1").replace("{{j}}",str(vnum))
        for i in range(2,pos-curPos):
            outStr += "moveleft"+str(i)+"cv"+str(vnum)+",_\n"
            outStr += "moveleft"+str(i-1)+"cv"+str(vnum)+',_,>\n\n'
            outStr += moveleft.replace("{{i}}",str(i)).replace("{{j}}",str(vnum))
    return outStr
    
def copyV(opos, newpos, nextpos):
    vposition = max(variables,key=variables.get)+1
    vnum = 0
    outStr = ""
    while "cv"+str(vnum) in variables:
        vnum += 1
    variables["cv"+str(vnum)] = vposition
    if pos > curPos:
        pass
    elif pos < curPos:
        pass
    return outStr

inFile = open("UTM.utm")
out = open("UTM.utmo")
operations = {'-': sub, "*": mult}

i=0
for line in inFile:
    variable = line.split('=')[0]
    equation = line.split('=')[1]
    writingNew=False
    try:
        vposition = variables[variable]
    except KeyError:
        variables[variable] = max(variables,key=variables.get)+1
        vposition = variables[variable]
    worked = False
    for k,v in operations.iteritems():
        if k in equation:
            out.write(v(vposition, equation.split(k)[0], equation.split(k)[1], i)+'\n\n')
            worked = True
    if not worked:
        copyV(variables[equation],vposition,"start"+str(i))
    i += 1
