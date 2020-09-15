import os
import os.path
import sys
import re

pwd = os.getcwd()

pwd = sys.argv[0]
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")

print pwd
print father_path
def listdirbaseroot(line,fout,countEx):
	
	line = line.replace("	","    ")
	line = line.replace("onCleanup","cleanup")
	line = line.replace("onEnterTransitionFinish","onEnterTransitionDidFinish")
	line = line.replace("onExitTransitionStart","onExitTransitionDidStart")
	line = line.replace("ccui.TouchEventType.ended","ccui.Widget.TOUCH_ENDED")
	line = line.replace("ccui.TouchEventType.began","ccui.Widget.TOUCH_BEGAN")
	line = line.replace("ccui.TouchEventType.moved","ccui.Widget.TOUCH_MOVED")
	line = line.replace("ccui.TouchEventType.canceled","ccui.Widget.TOUCH_CANCELED")
	
	
	if '.super.' in line:
		line = "    this._super()"
		have = True
		
	line = line.replace("\n","")
	line = line.replace("--","//")
	line = line.replace(":",".")
	line = line.replace("local ","var ")
	line = line.replace("nil","null")
	line = line.replace(" and "," && ")
	line = line.replace(" or "," || ")
	line = line.replace(" ~= "," != ")
	line = line.replace(" print"," cc.log")
	line = line.replace(".."," + ")
	line = line.replace("cc.FileUtils.getInstance()","jsb.fileUtils")
	line = line.replace(" self"," this")
	
	have = False
	if ' elseif' in line and 'then' in line:
		line = line.replace(" elseif"," }else if")
		have = True
	
	lineTrim = line.replace(" ","")
	if lineTrim == "else":
		line = line.replace("else","}else{")
		have = True
		
	if 'function' in line:
		if re.search(r"(.*)function.*[\:,\.](.*)(\(.*)", line):
			line=re.sub(r"(.*)function.*[\:,\.](.*)(\(.*)","\g<1>\g<2>: function \g<3> {",line)
			countEx.insert(0,"function1")
		elif re.search(r"(.*)function(.*)", line):
			line=re.sub(r"(.*)function(.*)","\g<1>function\g<2>{",line)
			countEx.insert(0,"function2")
		have = True
		
	if 'if' in line and 'then' in line:
		line=re.sub(r"(.*)if(.*)then","\g<1>if (\g<2>) {",line)
		line = line.replace("not ","! ")
		countEx.insert(0,"if")
		have = True
	
	if 'for' in line and 'do' in line:
		line = line.replace(" for "," for( ")
		line = line.replace(" do"," ){ ")
		countEx.insert(0,"for_do")
		have = True
		
	if ' end' in line or line.replace(" ","") == "end":
		mark = countEx.pop(0)
		if mark == "if":
			line = line.replace("end","}")
		elif mark == "function1":
			line = line.replace("end","},")
		elif mark == "function2":
			line = line.replace("end","}, this")
			line = line + ";"
		elif mark == "for_do":
			line = line.replace("end","}")
		else:
			print "end....."
		have = True
	
	#---
	lineTrim = line.replace(" ","")
	if lineTrim.startswith("//") or lineTrim == "":
		have = True
	
	if have == False:
		textIndex = line.find('//')
		if textIndex == -1:
			aa = line
		else:
			aa = line[:textIndex]
		aa = aa.strip(' ');
		line = line.replace(aa,aa+";")
		
	fout.write("    "+line+"\n")
	
	return countEx


countEx = [] #0 if / 1 func / 2 for
fout = open(father_path+"\out.txt","w")
fout.write('{')

for num in range(0,81):
	fout.write('"'+str(num)+'":')
	fin = open(father_path+"\level_"+str(num)+".txt")
	line = fin.readline()
	while line: 
		print line
		line = line.replace("\t","")
		line = line.replace("\n","")
		line = line.replace(" ","")
		fout.write(line)
		line = fin.readline()
	if num <> 2:
		fout.write(',')
	fin.close()

fout.write('}')
fout.close()

#line1 = "function BaseDialog.initDialogEvent()"
#line2 = "	self.shieldLayer:addTouchEventListener(function (sender,eventType)"
#
#			  #r"(.*)function.*\:(.*)(\(.*)"
#aa = re.search(r"(.*)function(.*)", line2)
#print(aa)









