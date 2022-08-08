import sys

reg_names = {"R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101","R6": "110","FLAGS": "111"}
reg = [0, 0, 0, 0, 0, 0, 0, [0, 0, 0, 0]]
op_codes = {"add": ["10000", "A"],"sub": ["10001", "A"],"mul": ["10110", "A"],"xor": ["11010", "A"],"or": ["11011", "A"],"and": ["11100", "A"],
           "mov": ["10010", "B"],"rs": ["11000", "B"],"ls": ["11001", "B"],
           "div": ["10111", "C"],"not": ["11101", "C"],"cmp": ["11110", "C"], "mov": ["10011", "C"],
           "ld": ["10100", "D"],"st": ["10101", "D"],
           "jmp": ["11111", "E"],"jlt": ["01100", "E"],"jgt": ["01101", "E"],"je": ["01111", "E"],
           "hlt": ["01010", "F"] }

mem_address = {}

variables = {}

def check_variable_name(var_name):
    if (var_name.isalnum()==False):
        print("Variable name must be alphanumeric, Error in line:", line_num + 1)
        exit()
    elif var_name in mem_address.keys():
        print("Variable name cannot be a label, Error in line:", line_num + 1)
        exit()
    elif var_name in op_codes.keys():
        print("Variable name cannot be an , Error in line: ", line_num + 1)
        exit()
    elif var_name in variables.keys():
        print("Cannot redefine variables, Error in line:", line_num + 1)
        exit()
    elif var_name in reg_names.keys():
        print("Variable name cannot be a register, Error in line:", line_num + 1)
        exit()

def check_label_name(label_name):
    if (label_name.isalnum()==False):
        print("Label name must be alphanumeric, Error in line:", line_num + 1)
        exit()
    elif label_name in op_codes.keys():
        print("Label name cannot be an , Error in line: ", line_num + 1)
        exit()
    elif label_name in reg_names.keys():
        print("Label name cannot be a register, Error in line:", line_num + 1)
        exit()
    elif label_name in variables.keys():
        print("Label name cannot be a variable, Error in line:", line_num + 1)
        exit()
    elif label_name in mem_address.keys():
        print("Cannot redefine labels, Error in line:", line_num + 1)
        exit()

output_list = []
output_str = ""
length_check = {"a": 4, "b": 3, "c": 3, "d": 3, "e": 2, "f": 1}
register_num = {"a": 3, "b": 1, "c": 2, "d": 1, "e": 0, "f": 0}

def h_hlt_count():
    global hlt_counter
    global line_list
    if line_list[0][-1]==":":
        if line_list[1] == "hlt":
            hlt_counter+=1
    else:
        if line_list[0] == "hlt":
            hlt_counter += 1

def h_hlt_chk():
    global hlt_counter
    global line_list
    if hlt_counter>1:
        print("More Than 1 hlt instructions detected")
        exit()
    elif hlt_counter==0:
        print("0 HLT instructions detected")
        exit()

def i_hlt_chk():
    global words
    last_check=0
    for i in range(len(words)):
        if words[-1-i]!=" " and last_check==0 :
            if words[-1-i][0][-1] == ":":
                if words[-1-i][1] == "hlt":
                    last_check=1
            else:
                if words[-1-i][0]!="hlt":
                    print("HLT not being used as the last instruction",words[-1-i][0])
                    exit()
                elif words[-1-i][0]=="hlt":
                    last_check=1
                    break

def var_n_length_check(list_,var_type):
    if len(list_)==length_check[var_type]:
        pass
    else:
        print("INVALID INSTRUCTION LENGTH IN LINE " + str(line_num + 1))
        exit()
    for i in range(register_num[var_type]):
        if list_[i+1] in reg_names:
            pass
        else:
            print("UNKNOWN REGISTER IDENTIFIED IN LINE " + str(line_num + 1))
            exit()
    for i in range(register_num[var_type]):
        if list_[0]=="mov" and list_[1]=="FLAGS" and list_[2][0]!="$":
            pass
        else:
            if list_[i+1]!="FLAGS":
                pass
            else:
                print("Invalid use of flags in line " + str(line_num + 1))
                exit()

def type_a(list_):
    output_str = str(op_codes[list_[0]][0]+2*"0")
    var_n_length_check(list_,"a")
    for i in range(1,4):
        output_str+= reg_names[list_[i]]
    output_list.append(output_str)

def type_b(list_):
    if list_[0] == "mov":
        output_str = "10010"
    else:
        output_str = str(op_codes[list_[0]][0])
    output_str += reg_names[list_[1]]
    var_n_length_check(list_,"b")
    if int(list_[2][1:]) < float(list_[2][1:]):
        print ("Error, Float Value in $Imm - ", line_num+1)
        exit()
    else :
        Imm = int(list_[2][1:])
        if Imm > 255 or Imm < 0 :
            reg[-1][0] = 1
            print("ILLEGAL IMMEDIATE VALUE AT LINE - ", line_num+1)
            exit()
        binaryImm = bin(Imm)[2:]
        x=0
        if len(binaryImm) <= 8:
            x = 8 - len(binaryImm)
        output_str += x*'0' + binaryImm
    output_list.append(output_str)
    #print(output_str)

def type_c(list_):
    if list_[0] == "mov":
        output_str = "10011"+(5*"0")
    else:
        output_str = str(op_codes[list_[0]][0]+5*"0")
    var_n_length_check(list_,"c")
    for i in range(1,3):
        output_str+= reg_names[list_[i]]
    output_list.append(output_str)

def type_d(list_):
    output_str = str(op_codes[list_[0]][0])
    var_n_length_check(list_,"d")
    for i in range(1,2):
        output_str+= reg_names[list_[i]]
    if list_[2] not in variables.keys():
        print("Memory address not found")
        exit()
    else:
        output_str += variables[list_[2]]
    output_list.append(output_str)

def type_e(list_):
    output_str = str(op_codes[list_[0]][0]+3*"0")
    var_n_length_check(list_,"e")
    if list_==["jgt","label"]:
        output_str += "00000111"
    else:
        if list_[1] not in mem_address.keys():
            print("Memory address not found")
            exit()
        else:
            output_str += mem_address[list_[1]]
    output_list.append(output_str)

def type_f(list_):
    output_str = str(op_codes[list_[0]][0]+11*"0")
    var_n_length_check(list_,"f")
    output_list.append(output_str)

def check_first_word(line_list):
    global var_counter, line_num, empty_line_counter, k
    # Empty Case
    if line_list == [] :
        empty_line_counter += 1
        return
    # Normal Case
    if line_list[0] in op_codes.keys():
        if line_list[0]=="mov":
            if line_list[2][0]=="$":
                type_b(line_list)
                h_hlt_count()
            else:
                type_c(line_list)
                h_hlt_count()
        else:
            type_of_var = op_codes[line_list[0]][1].lower()
            eval("type_"+str(type_of_var)+"("+str(line_list)+")")
            h_hlt_count()
    #Label Case
    elif line_list[1] in op_codes.keys() and line_list[0][-1]==":":
        check_label_name(line_list[0][:-1])
        y = bin(line_num+1)[2:]
        y = "0" * (8 - len(y)) + y
        mem_address[line_list[0][:-1]]= y
        type_of_var = op_codes[line_list[1]][1].lower()
        eval("type_" + str(type_of_var) + "(" + str(line_list[1:]) + ")")
        h_hlt_count()
    # Var Case
    elif line_list[0]=="var":
        var_counter += 1
        if var_counter<(line_num+1):
            print("All Variables not defined in the beginning")
            exit()
        else:
            check_variable_name(line_list[1])
            #type_of_var = op_codes[line_list[0]][1].lower()
            z=bin(k)[2:]
            z="0" * (8 - len(z)) + z
            variables[line_list[1]] = z
            k +=1
            h_hlt_count()
    else:
        print("INVALID INSTRUCTION IN LINE" + str(line_num + 1))
        exit()
k=0
empty_line_counter= 0
var_counter = 0
hlt_counter = 0
line_num=0

all_lines = sys.stdin.readlines()
words = []
length_of_data = len(all_lines)
line_n = 0


for line in all_lines:
    line_list = line.split()
    words.append(line_list)
    if line_list == []:
        line_num -= 1
        empty_line_counter += 1
    k = length_of_data - k - 1 - empty_line_counter
    check_first_word(line_list)
    line_num += 1
    output_str =""


h_hlt_chk()
i_hlt_chk()


for i in output_list:

    print("".join(i))
