def read_input(lst):
    while 1:
        ori_line = input().strip()
        if ori_line == "":
            continue
        elif ori_line == ".END":
            # print("file end")
            break

        l = ori_line.split(' ')
        if ".STRINGZ" in l:
            idx = l.index(".STRINGZ")
            t_l = l[idx + 1:]
            s = " ".join(t_l)
            new_line = l[:idx + 1]
            new_line.append(s)

            while '' in new_line:
                new_line.remove('')

            idx = new_line.index(".STRINGZ")
            ll = new_line[idx + 1].strip('\'')
            ll = ll.strip('\"')
            for c in ll:
                ori_file.append(ori_line + " " + c)
                t_line = new_line[:idx + 1]
                t_line.append(c)
                lst.append(t_line)

            ori_file.append(None)
            t_line = new_line[:idx + 1]
            t_line.append(None)
            lst.append(t_line)
            continue

        line = ori_line.split()
        n_items = len(line)
        # 此处必须用下标，如果用item遍历的话，只是copy value， line中原本含有的逗号的对象并不会改变
        for i in range(n_items):
            line[i] = line[i].strip(',')


        if ".BLKW" in line:
            idx = line.index(".BLKW")
            n_blank = int(line[idx+1].strip('#'))
            for j in range(n_blank):
                ori_file.append(ori_line)
                lst.append(line)
        elif ".STRINGZ" in line:
            idx = line.index(".STRINGZ")
            ll = line[idx+1].strip('\'')
            ll = ll.strip('\"')
            for c in ll:
                ori_file.append(ori_line + " " + c)
                t_line = line[:idx+1]
                t_line.append(c)
                lst.append(t_line)

            ori_file.append(None)
            t_line = line[:idx+1]
            t_line.append(None)
            lst.append(t_line)
        else:
            ori_file.append(ori_line)
            lst.append(line)



def generate_symbol_table(asm_file, symbol_table):
    n_lines = len(asm_file)
    for i in range(n_lines):
        a = asm_file[i][0]
        if a in instructions or a in traps or a in pseudo_operations:
            continue
        else:
            # 只选最早出现的那一个
            if a in symbol_table:
                continue
            else:
                # symbol_table[a] = i - 1 + start_memory_addr  # the first line cannot be counted (.ORIG x????)
                symbol_table[a] = i

def generate_machine_language(asm_file, machine_language_file):
    n_lines = len(asm_file)
    for i in range(n_lines):
        line = asm_file[i]
        if line[0] == ".ORIG":
            start_memory_addr = int(hex_2_bin(int(line[1].strip('x'), base=16), 16))
            machine_language_file.append(hex_2_bin(int(line[1].strip('x'), base=16), 16))
            continue
        if line[0] == ".END":
            break
        if line[0] in symbol_table:
            line = line[1:]

        if line[0] == ".BLKW":
            # j = int(line[1].strip('#'))
            # for k in range(j):
            machine_language_file.append("0111011101110111")
        elif line[0] == ".STRINGZ":
            # for c in line[1]:
            #     b = "00000000" + dec_2_bin(ord(c), 8)
            #     machine_language_file.append(b)
            # machine_language_file.append("0000000000000000")
            if line[1] == None:
                machine_language_file.append("0000000000000000")
            else:
                b = "00000000" + dec_2_bin(ord(line[1]), 8)
                machine_language_file.append(b)
        elif line[0] == ".FILL":
            machine_language_file.append(imm_2_str(line[1], 16))
        elif line[0] in traps:
            machine_language_file.append(hex_2_bin(traps[line[0]], 16))
        else:
            machine_language_file.append(assembly_2_binary(line, i+1)) # next instruction addr


def assembly_2_binary(line, id_line):
    if line[0] == "ADD":
        if line[3] in regs:
            b = instructions["ADD"] + regs[line[1]] + regs[line[2]] + "000" + regs[line[3]]
            return b
        else:
            b = instructions["ADD"] + regs[line[1]] + regs[line[2]] + "1" + imm_2_str(line[3], 5)
            return b
    elif line[0] == "AND":
        if line[3] in regs:
            b = instructions["AND"] + regs[line[1]] + regs[line[2]] + "000" + regs[line[3]]
            return b
        else:
            b = instructions["AND"] + regs[line[1]] + regs[line[2]] + "1" + imm_2_str(line[3], 5)
            return b
    elif line[0] == "NOT":
        b = instructions["NOT"] + regs[line[1]] + regs[line[2]] + "111111"
        return b
    elif line[0] == "LD":
        if line[2] in symbol_table:
            b = instructions["LD"] + regs[line[1]] + dec_2_bin(symbol_table[line[2]] - id_line, 9)
            return b
        else:
            b = instructions["LD"] + regs[line[1]] + dec_2_bin(int(line[2].strip("#")), 9)
            return b
    elif line[0] == "LDR":
        b = instructions["LDR"] + regs[line[1]] + regs[line[2]] + imm_2_str(line[3], 6)
        return b
    elif line[0] == "LDI":
        if line[2] in symbol_table:
            b = instructions["LDI"] + regs[line[1]] + dec_2_bin(symbol_table[line[2]] - id_line, 9)
            return b
        else:
            b = instructions["LDI"] + regs[line[1]] + dec_2_bin(int(line[2].strip("#")), 9)
            return b
    elif line[0] == "LEA":
        if line[2] in symbol_table:
            b = instructions["LEA"] + regs[line[1]] + dec_2_bin(symbol_table[line[2]] - id_line, 9)
            return b
        else:
            b = instructions["LEA"] + regs[line[1]] + dec_2_bin(int(line[2].strip("#")), 9)
            return b
    elif line[0] == "ST":
        if line[2] in symbol_table:
            b = instructions["ST"] + regs[line[1]] + dec_2_bin(symbol_table[line[2]] - id_line, 9)
            return b
        else:
            b = instructions["ST"] + regs[line[1]] + dec_2_bin(int(line[2].strip("#")), 9)
            return b
    elif line[0] == "STR":
        b = instructions["STR"] + regs[line[1]] + regs[line[2]] + imm_2_str(line[3], 6)
        return b
    elif line[0] == "STI":
        if line[2] in symbol_table:
            b = instructions["STI"] + regs[line[1]] + dec_2_bin(symbol_table[line[2]] - id_line, 9)
            return b
        else:
            b = instructions["STI"] + regs[line[1]] + dec_2_bin(int(line[2].strip("#")), 9)
            return b
    elif line[0] == "TRAP":
        b = "11110000" + hex_2_bin(int(line[1].strip('x'), base=16), 8)
        return b
    elif line[0] == "JMP":
        b = "1100000" + regs[line[1]] + "000000"
        return b
    elif line[0] == "RET":
        b = "1100000" + regs["R7"] + "000000"
        return b
    elif line[0] == "JSR":
        if line[1] in symbol_table:
            b = instructions["JSR"] + "1" + dec_2_bin(symbol_table[line[1]] - id_line, 11)
            return b
        else:
            b = instructions["JSR"] + "1" + dec_2_bin(int(line[1].strip("#")), 11)
            return b
    elif line[0] == "JSRR":
        b = "0100000" + regs[line[1]] + "000000"
        return b
    elif line[0] == "RTI":
        return "1000000000000000"
    elif line[0] == "BR":
        if line[1] in symbol_table:
            b = instructions["BR"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BR"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRn":
        if line[1] in symbol_table:
            b = instructions["BRn"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRn"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRz":
        if line[1] in symbol_table:
            b = instructions["BRz"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRz"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRp":
        if line[1] in symbol_table:
            b = instructions["BRp"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRp"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRnz":
        if line[1] in symbol_table:
            b = instructions["BRnz"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRnz"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRzp":
        if line[1] in symbol_table:
            b = instructions["BRzp"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRzp"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRnp":
        if line[1] in symbol_table:
            b = instructions["BRnp"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRnp"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b
    elif line[0] == "BRnzp":
        if line[1] in symbol_table:
            b = instructions["BRnzp"] + dec_2_bin(symbol_table[line[1]] - id_line, 9)
            return b
        else:
            b = instructions["BRnzp"] + dec_2_bin(int(line[1].strip("#")), 9)
            return b

# unsigned so fill it by 0
def hex_2_bin(num, bits):
    if bits == 16:
        return format(num, "016b")
    elif bits == 8:
        return format(num, "08b")

# maybe negative
def dec_2_bin(num, bits):
    if num >= 0:
        num = bin(num)
        num = num.replace("0b", "")
        return '0' * (bits - len(num)) + num
    else:
        inverse = -num
        complement = 2 ** bits - inverse
        complement = bin(complement)
        complement = complement.replace("0b", "")
        return complement

# str -> str
def imm_2_str(imm, bits):
    if '#' in imm:
        return dec_2_bin(int(imm.strip('#')), bits)
    else:
        return dec_2_bin(int(imm.strip('x'), base=16), bits)

instructions = {
    "ADD": "0001", "AND": "0101", "NOT": "1001",
    "LD": "0010", "LDR": "0110", "LDI": "1010",
    "LEA": "1110", "ST": "0011", "STR": "0111",
    "STI": "1011", "TRAP": "1111",
    "JMP": "1100", "JSR": "0100", "RTI": "1000",
    "BR": "0000111", "BRn": "0000100", "BRz": "0000010", "BRp": "0000001",
    "BRnz": "0000110", "BRzp": "0000011", "BRnp": "0000101", "BRnzp": "0000111",
    "RET":"","JSRR":""
}
traps = {
    "GETC": 0xF020, "OUT": 0xF021, "PUTS": 0xF022, "IN": 0xF023, "PUTSP": 0xF024, "HALT": 0xF025
}
regs = {
    "R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "R7": "111"
}
pseudo_operations = [
    ".ORIG", ".FILL", ".BLKW", ".STRINGZ", ".END"
]

# how to deal with RET?
ori_file = []
asm_file = []
machine_language_file = []
symbol_table = {}
start_memory_addr = 0
memory_offset = 0

read_input(asm_file)
# for line in asm_file:
#     print(line)

#有bug，因为.BLKW, .STRINGZ都不止占用一行，所以生成的和代码的行数不一致
generate_symbol_table(asm_file, symbol_table)
# for key, value in symbol_table.items():
#     print(key, value)


generate_machine_language(asm_file, machine_language_file)
# for line in ori_file:
#     # if line == None:
#     #     continue
#     print(line)
#
for line in machine_language_file:
    print(line)

# nn = len(ori_file)
# for i in range(nn):
#     if ori_file[i] == None:
#         print(format(".STRINGZ END", "60") + machine_language_file[i])
#     else:
#         print(format(ori_file[i], "60") + machine_language_file[i])