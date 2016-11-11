import sqlite3
import csv
from sets import Set

MainGraph = {}

#Graph node structure which hold next nodes and previous nodes(previous nodes not used)
class CGraphNode:
	def __init__(self):
		self.TransferedTo = Set()
		
		self.RecivedFrom = Set()

#its level 1 search friend of friend relation 
def SearchInGraph(id1,id2):
	if((id2 in MainGraph)):
		for tranID in MainGraph[id1].TransferedTo :
			if(tranID in MainGraph[id2].TransferedTo ):
				return True
		return False
	else:
		return False

#to check if the value is int
def isint(val):
	if type(val) == int:
		return True
	else:
		return False
	
# Recursive search function with depth limited to value 3(depth 4)
def DepthSearch(id1,id2,depth,MaxDepth):
	if(depth >= MaxDepth):
		return False
	
	if(id1 in MainGraph):
		if(id2 in MainGraph[id1].TransferedTo ):
			return True
	for NewIdx,NewId in enumerate(MainGraph[id1].TransferedTo) :
		found = DepthSearch(NewId,id2,depth+1,MaxDepth)
		if(found):
			return True
	return False;

#connect to DB
conn = sqlite3.connect('database.db')
conn.text_factory = str
c = conn.cursor()

# code to read csv files
# with open('batch_payment.csv', 'rU') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		if(len(row) < 4):
# 			continue
# 		if(row[1] in MainGraph):
# 			MainGraph[row[1]].TransferedTo.add(row[2])			
# 		else:
# 			NodeObj = CGraphNode()
# 			MainGraph[row[1]] = NodeObj
# 			MainGraph[row[1]].TransferedTo.add(row[2])
# 	
# 		if(row[2] in MainGraph):
# 			MainGraph[row[2]].RecivedFrom.add(row[1])
# 		else:
# 			NodeObj = CGraphNode()
# 			MainGraph[row[2]] = NodeObj
# 			MainGraph[row[2]].RecivedFrom.add(row[1])	
# 		
#

#iterate though all the history and contract the graph		
for row in c.execute('select * from transaction_history;'):
	#next node links
	if(isint(row[1]) == False):
		continue
	if(int(row[1]) in MainGraph):
		MainGraph[int(row[1])].TransferedTo.add(int(row[2]))			
	else:
		NodeObj = CGraphNode()
		MainGraph[int(row[1])] = NodeObj
		MainGraph[int(row[1])].TransferedTo.add(int(row[2]))
	#previous node links
	if(int(row[2]) in MainGraph):
		MainGraph[int(row[2])].RecivedFrom.add(int(row[1]))
	else:
		NodeObj = CGraphNode()
		MainGraph[int(row[2])] = NodeObj
		MainGraph[int(row[2])].RecivedFrom.add(int(row[1]))




print "done creating Graph"

#opening the out put files for writing 
output1 = open('./paymo_output/output1.txt','w')
output2 = open('./paymo_output/output2.txt','w')
output3 = open('./paymo_output/output3.txt','w')		

#code using csv read	
# with open('stream_payment.csv', 'rU') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		if(len(row) < 4):
# 			continue
# 		if(row[1] in MainGraph):
# 			if(row[2] in MainGraph[row[1]].TransferedTo ):
# 				output1.write("trusted\n")
# 				output2.write("trusted\n")
# 				output3.write("trusted\n")
# 				continue
# 			else:
# 				output1.write("unverified\n")
# 			#for level two
# 				IsTrusted = SearchInGraph(row[1],row[2])
# 				if(IsTrusted):
# 					output2.write("trusted {id1} {id2}\n".format(id1=row[1],id2=row[2]))
# 					output3.write("trusted\n")
# 				else:
# 					output2.write("unverified\n")
# 					if(DepthSearch(row[1],row[2],0)):
# 						output3.write("trusted {id1} {id2}\n".format(id1=row[1],id2=row[2]))
# 					else:
# 						output3.write("unverified\n")
# 		
# 		else:
# 			output1.write("unverified\n")
# 			output2.write("unverified\n")
# 			output3.write("unverified\n")

#iterate though the stream table
for row in c.execute('select * from transaction_stream;'):
	if(isint(row[1]) == False or isint(row[2]) == False):
		continue
	if(int(row[1]) in MainGraph):
		#search at level1 direct connection
		if(int(row[2]) in MainGraph[int(row[1])].TransferedTo ):
			output1.write("trusted\n")
			output2.write("trusted\n")
			output3.write("trusted\n")
			continue
		else:
			output1.write("unverified\n")
		#search level two on redirection
			IsTrusted = DepthSearch(int(row[1]),int(row[2]),0,2)
			if(IsTrusted):
				output2.write("trusted\n")
				output3.write("trusted\n")
			else:
				output2.write("unverified\n")
				#print "searching id1 "+str(row[1])+" id2 "+str(row[2])
				if(DepthSearch(int(row[1]),int(row[2]),0,4)):
					output3.write("trusted\n")
				else:
					output3.write("unverified\n")
		
	else:
		output1.write("unverified\n")
		output2.write("unverified\n")
		output3.write("unverified\n")
	

output1.close()
output2.close()
output3.close()