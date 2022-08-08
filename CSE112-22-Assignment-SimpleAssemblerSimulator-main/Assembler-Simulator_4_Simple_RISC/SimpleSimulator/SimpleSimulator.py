import sys 

# sim_in = open("input.txt","r")
# all_lines = sim_in.read().splitlines()
all_lines = sys.stdin.read().splitlines()
#print(all_lines)

registers = [0,0,0,0,0,0,0,[0,0,0,0]]

op_code_check = {
    "00000":["addf","A"],
    "00001":["subf","A"],
    "00010":["movf","B"],
    "10000": ["add","A"],
    "10001": ["sub","A"],
    "10010": ["movI","B"],
    "10011": ["movR","C"],
    "10100": ["ld","D"],
    "10101": ["st","D"],
    "10110": ["mul","A"],
    "10111": ["div","C"],
    "11000": ["rs","B"],
    "11001": ["ls","B"],
    "11010": ["xor","A"],
    "11011": ["or","A"],
    "11100": ["and","A"],
    "11101": ["inv","C"],
    "11110": ["cmp","C"],
    "11111": ["jmp","E"],
    "01100": ["jlt","E"],
    "01101": ["jgt","E"],
    "01111": ["je","E"],
    "01010": ["halt","F"],
}

op_codes = []
mem_heap = []
pc = 0
cycle = 1
flag = 0
pc_and_cycle = []
halted = False
lines = int(len(all_lines))
mem_left = 256-lines

def bin_to_16bit(dec_val):
    global registers

    if type(dec_val) == list:
        #print(dec_val, registers)
        dec_val=dec_val[0]
    if (dec_val > 2**16-1):
        bin_rep = str(bin(dec_val))
        bin_rep = bin_rep[2::]
        l = len(bin_rep)
        bin_rep = bin_rep[l-16:l:]
        binval = int(bin_rep, 2)
        binval = ('{0:016b}'.format(binval))
    else:
        binval = ('{0:016b}'.format(dec_val))
    return binval

def check_overflow(inst):
    global registers, flag
    try:
        temp = registers[inst]
    except ValueError:
        temp = -1
    if (temp > 2**16-1 or temp < 0):
        registers[-1][0] = 1
        flag = 8
        if (temp > 2**16-1):
            registers[inst] = int(bin_to_16bit(registers[inst]), 2)
        else:
            registers[inst] = 0
    return

def out():
    global pc,cycle
    s = [str(i) for i in registers[-1]]
    fla = "".join(s)
    flag = int(fla, 2)
    print(
        '{0:08b}'.format(pc),
        bin_to_16bit(registers[0]),
        bin_to_16bit(registers[1]),
        bin_to_16bit(registers[2]),
        bin_to_16bit(registers[3]),
        bin_to_16bit(registers[4]),
        bin_to_16bit(registers[5]),
        bin_to_16bit(registers[6]),
        bin_to_16bit(flag),
        sep=" "
    )
    pc_and_cycle.append((pc, cycle))
    cycle += 1

def type_a(inst):
    if inst[0]=="add":
        reg1 = registers[int(inst[1],2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        registers[int(inst[3], 2)] = reg1+reg2
        check_overflow(int(inst[3],2))

    elif inst[0]=="sub":
        reg1 = registers[int(inst[1], 2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        registers[int(inst[3], 2)] = reg1-reg2
        check_overflow(int(inst[3], 2))

    elif inst[0]=="mul":
        reg1 = registers[int(inst[1], 2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        registers[int(inst[3], 2)] = reg1 * reg2
        check_overflow(int(inst[3], 2))

    elif inst[0]=="xor":
        reg1 = registers[int(inst[1], 2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        registers[int(inst[3], 2)] = reg1 ^ reg2
    elif inst[0]=="or":
        reg1 = registers[int(inst[1], 2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        registers[int(inst[3], 2)] = reg1 | reg2
    elif inst[0] == "addf":
        reg1 = registers[int(inst[1], 2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        if type(reg1) != int:
            aaa = (2*(int(reg1[0:3],2)-3))(1+(((int(reg1[3]))(1/2))+((int(reg1[4]))(1/4)))+((int(reg1[5]))(1/8))+((int(reg1[6]))(1/16))+((int(reg1[7]))*(1/32)))
        else :
            aaa = reg1
        if type(reg2) != int:
            aab = (2*(int(reg2[0:3],2)-3))(1+(((int(reg2[3]))(1/2))+((int(reg2[4]))(1/4)))+((int(reg2[5]))(1/8))+((int(reg2[6]))(1/16))+((int(reg2[7]))*(1/32)))
        else :
            aab = reg2
        aac = aaa + aab
        reg3 = bin_to_16bit(aac)
    elif inst[0] == "subf":
        reg1 = registers[int(inst[1], 2)]
        reg2 = registers[int(inst[2], 2)]
        reg3 = registers[int(inst[3], 2)]
        if type(reg1) != int:
            aaa = (2*(int(reg1[0:3],2)-3))(1+(((int(reg1[3]))(1/2))+((int(reg1[4]))(1/4)))+((int(reg1[5]))(1/8))+((int(reg1[6]))(1/16))+((int(reg1[7]))*(1/32)))
        else :
            aaa = reg1
        if type(reg2) != int:
            aab = (2*(int(reg2[0:3],2)-3))(1+(((int(reg2[3]))(1/2))+((int(reg2[4]))(1/4)))+((int(reg2[5]))(1/8))+((int(reg2[6]))(1/16))+((int(reg2[7]))*(1/32)))
        else :
            aab = reg2
        aac = aaa - aab
        reg3 = bin_to_16bit(aac)

def type_b(inst):
    if inst[0] == "movI":
        registers[int(inst[1], 2)] = int(inst[2],2)
    elif inst[0] == "rs":
        registers[int(inst[1], 2)] = ( (int(inst[1],2)) // (2**(int(inst[2],2))) )
    elif inst[0] == "ls":
        registers[int(inst[1], 2)] = ( (int(inst[1],2)) * (2**(int(inst[2],2))) )
        if registers[int(inst[1], 2)] > ((2**16)-1):
            registers[int(inst[1], 2)] = 0

def type_c(inst):
    if inst[0] == "movR":
        if int(inst[1],2) == 7:
            s = [str(i) for i in registers[-1]]
            fla = "".join(s)
            registers[int(inst[2],2)] = int(fla,2)
        else:
            # print(registers[int(inst[1],2)]," - ", inst)
            registers[int(inst[2],2)] = registers[int(inst[1],2)]
    elif inst[0] == "div":
        registers[0] = registers[int(inst[1],2)] // registers[int(inst[2],2)]
        registers[1] = registers[int(inst[1],2)] % registers[int(inst[2],2)]
    elif inst[0] == "inv":
        registers[int(inst[2],2)] = ((2**16)-1) - registers[int(inst[1],2)]
    elif inst[0] == "cmp":
        reg1 = registers[int(inst[1],2)]
        reg2 = registers[int(inst[2],2)]
        if reg1<reg2:
            registers[-1][1]=1
        elif reg1>reg2:
            registers[-1][2]=1
        elif reg1==reg2:
            registers[-1][3]=1
    # print(registers[3], " - ", inst)

def type_d(inst):
    global mem_heap
    if inst[0] == "ld":
        registers[int(inst[1],2)] = int(mem_heap[int(inst[2],2)],2)
    elif inst[0] == "st":
        mem_heap[int(inst[2],2)] = bin_to_16bit(registers[int(inst[1],2)])

def type_e(inst):
    global pc,flag
    if inst[0] == "jmp":
        pc = int(inst[1],2)
    else:
        temp = flag
        flag = 0
        out()
        flag = temp
        if inst[0] == "jlt":
            if registers[-1][1]==1:
                pc = int(inst[1],2)
            else:
                pc+=1
        elif inst[0] == "jgt":
            if registers[-1][2]==1:
                pc = int(inst[1],2)
            else:
                pc+=1
        elif inst[0] == "je":
            if registers[-1][3]==1:
                pc = int(inst[1],2)
            else:
                pc+=1
        flag = 0
        registers[-1]=[0,0,0,0]

def type_f(inst):
    if inst[0] == "hlt":
        pass
for i in range(256):
    mem_heap.append("0000000000000000")
a=0
for line in all_lines:
    if halted==False:
        op = line[0:5]
        op_type = op_code_check.get(op)
        #print(op_type)
        if (op_type[0] != "movR" and op_type[0] != "jlt" and op_type[0] != "jgt" and op_type[0] != "je"):
            registers[-1]=[0,0,0,0] # Flag reset
        #print(op_type)

        if op_type[1]=="A":
            inst = [op_type[0],line[7:10],line[10:13],line[13:16]]
            type_a(inst)
        elif op_type[1]=="B":
            inst = [op_type[0],line[5:8],line[8:16]]
            type_b(inst)
        elif op_type[1]=="C":
            inst = [op_type[0],line[10:13],line[13:16]]
            type_c(inst)
        elif op_type[1]=="D":
            inst = [op_type[0],line[5:8],line[8:16]]
            type_d(inst)
        elif op_type[1]=="E":
            inst = [op_type[0],line[8:16]]
            type_e(inst)
        elif op_type[1]=="F":
            inst = [op_type[0]]
            halted = True
            type_f(inst)

        if op_type[1]!="E":
            s = [str(i) for i in registers[-1]]
            fla = "".join(s)
            flag = int(fla,2)
            # print(registers, " - ", op_type)
            print(
                '{0:08b}'.format(pc),
                bin_to_16bit(registers[0]),
                bin_to_16bit(registers[1]),
                bin_to_16bit(registers[2]),
                bin_to_16bit(registers[3]),
                bin_to_16bit(registers[4]),
                bin_to_16bit(registers[5]),
                bin_to_16bit(registers[6]),
                bin_to_16bit(flag),
                sep=" "
            )
            pc_and_cycle.append((pc,cycle))
            cycle+=1
            pc += 1
        # if (op_type[0] != "jmp" and op_type[0] != "jlt" and op_type[0] != "jgt" and op_type[0] != "je"):
        #     pc+=1
        op_codes.append(op)
        mem_heap[a] = line
        a+=1


for i in mem_heap:
    print(i)

#Question - 4
import matplotlib.pyplot as graph1

def graph():
    global pc_and_cycle
    x = []
    y = []
    for i in pc_and_cycle:
        x.append(i[1])
        y.append(i[0])
    graph1.scatter(x,y,c='Red')
    graph1.xlabel('Cycle')
    graph1.ylabel('PC')
    graph1.savefig('plot.png')
    graph1.show()

graph()