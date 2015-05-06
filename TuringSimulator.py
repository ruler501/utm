from collections import defaultdict

def showTape(tape,position):
    minValue=min(tape.keys(),key=int)
    maxValue=max(tape.keys(),key=int)
    outStr=""
    for i in range(minValue,maxValue+1):
        outStr += tape[i]
    outStr += '\n'+' '*(position-minValue)+'^'
    return outStr
    
def main(argv=None):
    tape = defaultdict(lambda: '_')
    states = defaultdict(lambda: defaultdict(lambda: ('reject','_','-')))
    movement = {'-': 0, '>': 1, '<': -1}
    name = "UTM"
    init = "start0"
    accept = "end"
    with open(argv[1]) as program:
        data = program.read().strip()
        transitions = data.split('\n\n')
        lines = transitions[0].split('\n')
        name = ' '.join(lines[0].split(' ')[1:])
        init = ' '.join(lines[1].split(' ')[1:])
        accept = ' '.join(lines[2].split(' ')[1:])
        for transition in transitions[1:]:
            lines = transition.split('\n')
            state = lines[0].split(',')[0]
            symbol = lines[0].split(',')[1]
            nstate = lines[1].split(',')[0]
            nsymbol = lines[1].split(',')[1]
            direction = lines[1].split(',')[2]
            if direction not in ('<','>','-'):
                raise SyntaxError
            states[state][symbol] = (nstate,nsymbol,direction)
    for i in range(len(argv[2])):
        tape[i] = argv[2][i]
    curState = init
    position = 0
    outFile=open(name+".log", 'w')
    while curState not in ("reject",accept):
        outFile.write('position='+str(position)+", current State="+str(curState)+", current character="+tape[position]+", tape:\n"+showTape(tape,position)+'\n\n')
        transition = states[curState][tape[position]]
        curState = transition[0]
        tape[position] = transition[1]
        position += movement[transition[2]]
    outFile.write('position='+str(position)+", current State="+str(curState)+", current character="+tape[position]+" tape:\n"+showTape(tape,position))
    
if __name__ == "__main__":
    main(['TuringSimulator.py','UTM.utmo','0001'])