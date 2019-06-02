#!usr/bin/env python
# coding: utf-8

from immlib import *
import re

DESC = "Description of the Pyhton Script using IMMLIB"

#Function to calculate the offset
def offset(pattern):
	string = ""
	for i in range(ord("A"), ord("Z")+1):
		for j in range(ord("a"), ord("z")+1):
			for k in range(10):
				string += chr(i) + chr(j) + str(k)
	return string.find(pattern)

#Function to convert from hex to ASCII
def htoa(string):
	imm = Debugger()	
	substring = ""
	for i in range(8, -1, -2):
		substring += string[i:i+2]
	substring = substring.decode('hex')
	return substring

#Main Function
def main(args):

	#Instantiate a Debugger
	imm = Debugger()

	#Read the registers
	regs = imm.getRegs()
	for i in range(10):
		imm.log("")

		imm.log("##########################################################")
		imm.log("#### Registers")
		imm.log("##########################################################")
		imm.log("EIP: 0x%08X" %regs["EIP"])
		imm.log("ESP: 0x%08X" %regs["ESP"])
		imm.log("##########################################################")
		imm.log(hex(regs['EIP'])[2:-1])
		string = hex(regs['EIP'])[2:-1]
		eip = htoa(string)
		imm.log("EIP ASCII: %s –> Offset: %d" %(eip,offset(eip)))
		esp = imm.readString(regs["ESP"])[:4]
		imm.log("ESP Value: %s –> Offset: %d" %(esp, offset(esp)))
		imm.log("##########################################################")
		imm.createLogWindow()

	#Search for the code jmp esp
	code = "jmp esp"
	opcode = imm.assemble(code)
	search = imm.search(opcode)

	#Create a new table
	tbl = imm.createTable("Code Address",["Module","Code","Address"])

	#iterate through search and fill the table
	for addr in search:
		if imm.findModule(addr):
			module = imm.findModule(addr)[0]
			code2 = imm.disasm(addr).getDisasm()
			tbl.add(0,[module,code2,"0x%08X" %addr])

	return "[+] Success!!!"