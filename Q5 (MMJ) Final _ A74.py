# Question.5
# Memory Mumbo Jumbo
# Group A-74 (Shivam Dwivedi, Akshmit Dewan, Kunal Sapra)

import math

def type1(n):
    memory = {'Mb': 1024 * 1024, 'MB': 1024 * 1024 * 8, 'kb': 1024, 'kB': 1024 * 8, 'b': 1, 'B': 1*8, 'Nibble' : 4, 'Word': 16}
    return memory[n]

def type2(n, z):
    if n == 'Bit' or n == 'Nibble' or n == 'Byte' :
        memory = {'Bit': 1, 'Nibble': 4, 'Byte': 8}
        return memory[n]
    else:
        return z

space_in_memory = input("Enter the available space in memory (Memory followed by it's type i.e. b,Nibble,B,Word,kb,kB,Mb,MB : ").split()
space_in_bits = type1(space_in_memory[1]) * int(space_in_memory[0])
type_mem_adr = input("Enter how the memory is addressed i.e. input from Bit,Nibble,Byte,Word : ")
type_mem_adr_bits = type2(type_mem_adr, 8)

type_of_question = input("Types of questions : \n 1. ISA & Instructions Related \n 2. System Enhancement Related - Type 1 \n 3. System Enhancement Related - Type 2 \nEnter the number corresponding to the question you want to ask : ")

if type_of_question == "1":
    l_ins = int(input("Enter the length of one instruction in bits : "))
    r_ins = int(input("Enter the length of one register in bits : "))
    print ("Output - \n 1. How many minimum bits are needed to represent an address in this architecture ? : {} \n 2. Number of bits needed by opcode : {} \n 3. Number of filler bits in Instruction type 2 : {} \n 4. Maximum numbers of instructions this ISA can support : {} \n 5. Maximum number of registers this ISA can support : {}".format(int(math.log(space_in_bits/type_mem_adr_bits, 2)), l_ins - r_ins - int(math.log(space_in_bits/type_mem_adr_bits, 2)), l_ins - 2*r_ins - (l_ins - r_ins - int(math.log(space_in_bits/type_mem_adr_bits, 2))), pow(2, l_ins - r_ins - int(math.log(space_in_bits/type_mem_adr_bits, 2))), pow(2, r_ins)))

elif type_of_question == "2":
    bits_in_the_cpu = int(input("Input how many bits the cpu is : "))
    change = input("Input how you would want to change the current addressable memory to any of the rest 3 options i.e. input from Bit,Nibble,Byte,Word : ")
    print("Output - How many address pins are saved or required : {}".format(int(math.log(type2(type_mem_adr, bits_in_the_cpu)/type2(change, bits_in_the_cpu), 2))))

elif type_of_question == "3":
    bits_in_the_cpu = int(input("Input how many bits the cpu is : "))
    ap_in_the_cpu = int(input("Input how many address pins it has : "))
    am = input("Input what type of addressable memory it has i.e. input from Bit,Nibble,Byte,Word : ")
    ans = int(pow(2, ap_in_the_cpu) * type2(am, bits_in_the_cpu)/8)
    print("Output - How big the main memory can be ? : {} bytes, {} kB, {} MB, {} GB, {} TB".format(ans, ans/1024, ans/1024/1024, ans/1024/1024/1024, ans/1024/1024/1024/1024))









