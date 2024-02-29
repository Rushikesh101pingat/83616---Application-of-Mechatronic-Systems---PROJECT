#! /usr/bin/env python3
from opcua import Client,ua
import time
import sys
import argparse #Used for command line arguments
import requests
import pymysql
from numpy import uint32

default_ip = "localhost"
default_port="4840"
default_PRG="GVL"

class openCart_DB:
	"""
	Allows to access the database used for opencart
	For thix example the database was created with XAMMP
	"""
	def __init__(self):
		"""
		Instantiate openCart db and connect to the DB
		"""
		self.connection=pymysql.connect(host="localhost",user="root",passwd="",database="opencart") #MySQL Connection to xammp Database
		self.cursor=self.connection.cursor()
	def get_order_products(self,order_id):
		"""
		Get all the products that belong to a specific order
		@param order_id: Unique Order Id number to query
		@returns array with information of each product for the queried order
		"""
		mysql_query="SELECT * FROM `oc_order_product` WHERE order_id=%d"%(order_id) #MySQL Query
		self.cursor.execute(mysql_query)
		rows=self.cursor.fetchall()
		order_products=[]
		#read each of the rows included in the DB and parse the columns
		#the indexes are fixed and can be corroborated by manually
		#opening the DB in XAMMP and counting the column in which each element is located
		for row in rows:
			order_info=dict()
			order_info["order_product_id"]=row[0] #Unique Order ID for each product in an order
			order_info["order_id"]=row[1] #common  id for all the products that have belong to the same order
			order_info["product_id"]=row[2] #Individual product id
			order_info["name"]=row[3] #Name of product
			order_info["model"]=row[4] #Model
			order_info["quantity"]=row[5]
			order_info["price"]=row[6]
			order_info["total"]=row[7] #price*qty
			order_info["tax"]=row[8]
			order_info["reward"]=row[9]
			order_products.append(order_info)
		return order_products
	def get_all_orders(self):
		"""
		Get all the orders that are stored in the opencart DB
		@returns dictionary:
				-orders: list of all the orders in the DB
				-last_order: ID of the last order stored in the DB
		"""
		mysql_query="SELECT * FROM `oc_order` ORDER BY `oc_order`.`order_id` DESC" #MySQL Query
		self.cursor.execute(mysql_query)
		rows=self.cursor.fetchall()
		orders=[]
		for row in rows:
			order_info=dict()
			order_info["order_id"]=row[0] #Unique Order ID
			order_info["customer_id"]=row[6]
			order_info["customer_group_id"]=row[7] #Individual product id
			orders.append(order_info)
		if len(orders)>0:
			last_order=orders[0]["order_id"]
		else:
			last_order=None
		return {"orders":orders,"last_order":last_order}	
	def __del__(self):
		self.connection.close()
class Example_OPCUA_Client:
	client=None
	def __init__(self,ip,port):
		"""
		Initialize example
		@parameter ip: string ip
		@parameter port: string port
		"""
		self.ip=ip
		self.port=port
		self.url=self.__get_opc_url()
	def __get_opc_url(self):
		return "opc.tcp://"+self.ip+":"+self.port
		
	def getChildInfo(self,rootNode,level=0):
		"""
		Print all the nodes that are part of a child
		"""
		levelIdentation=" "*level
		for child in rootNode.get_children():
			try:
				try:
					nodeClass=str(child.get_node_class())
					if "Variable" in nodeClass:
						nodeClass="V"
					else:
						nodeClass="O"
				except:
					nodeClass="?"
				nodeInfo=levelIdentation+"-[%s]%s  Id:%s"%((nodeClass,child.get_display_name().Text,str(child)))
				print(nodeInfo)
				self.getChildInfo(child,level+1)
			except Exception as e:
				pass
			
	def getVariables(self,Node):
		"""
		Get all the variables in a specific node and subnodes
		"""
		variables=[]
		for child in Node.get_children():
			try:
				value=child.get_value()
				variables.append({"Text":child.get_display_name().Text,"val":str(value),"id":str(child),"node":child})
			except Exception as e:
				pass
			try:
				child_vars=self.getVariables(child)
				variables.extend(child_vars)
			except:
				pass
			
		return variables
	def searchNode(self,baseNode,name):
		"""
		Search for a specific node in the OPC UA Server
		@param baseNode: base node where to searchNode
		@param name: String name that will be used to search for the specific node
		"""
		for child in baseNode.get_children():
			if child.get_display_name().Text==name:
				return child
			else:
				child_search=self.searchNode(child,name)
				if child_search!=None:
					return child_search
		return None
			
	def connect(self):
		try:
			self.client = Client(self.url)
			self.client.connect()
			print ("Client connected");	
		except Exception as e:
			print(str(e))
			sys.exit()
	def __del__(self):
		if self.client!=None:
			print("Disconnecting...")
			client.disconnect()

class Car_OPCUA:
	motorStatus=None
	node=None
	def __init__(self,baseNode,exampleClient):
		"""
		Example implementation of a class
		that retrieves information for the "fbCar" variable
		in the PLC Program
		"""
		self.motorStatus=False
		self.node=exampleClient.searchNode(baseNode,"OPCUA_Server")
		self.vars=dict()
		#Create a dictionary with the variables of the node for easy access
		for v in exampleClient.getVariables(self.node):
			self.vars[v["Text"]]=v
			
parser = argparse.ArgumentParser(description='OPC UA Python Application Demo FH Aachen AMS83616')
parser.add_argument('-n',action='store_true', help='Show the Nodes of the Server')
parser.add_argument('-v',action='store_true', help='Find Variables in the OPC UAServer')
parser.add_argument('-o',action='store_true', help='Show only variables from Object Node\nOnly used in combination with -v')
parser.add_argument('-read',action='store_true', help='Start the Read OPC UA Server Demo')
parser.add_argument('-write',action='store_true', help='Writes a Boolean Value by writing to the Server Demo')

args = parser.parse_args()

example=Example_OPCUA_Client(default_ip,default_port)

# Prompt user for (optional) command line arguments, when run from Python IDLE:


if args.n:
	example.connect()
	print("Retrieving OPC UA Server Nodes...")
	root = example.client.get_root_node()
	print("Root Folder is: ",root )
	print("Nodes are:")
	example.getChildInfo(root)

if args.v:
	example.connect()
	print("Retrieving Variables")
	if args.o:
		print("BaseNode: Objects")
		baseNode=example.client.get_objects_node()
	else:
		print("BaseNode: Root")
		baseNode=example.client.get_root_node()
	variables=example.getVariables(baseNode)
	for var in variables:
		print(var["Text"],"\t","id:"+var["id"],var["val"][:100])
		
if args.read or args.write:
	try:
		example.connect()
		program_node=example.searchNode(example.client.get_objects_node(),default_PRG)
		if program_node==None:
			print("Are you sure that the OPC UA Server is set correctly?")
		else:
			print("Wago OPC UA Server Demo Found")
			Car=Car_OPCUA(program_node,)
			if args.read:
				print("------------------------------")
				example.getChildInfo(program_node)
				print("------------------------------")
				print("Starting Read Demo")
				timeNode=example.searchNode(program_node,"tTime")
				tempNode=Car.vars["temp"]["node"]
				print("------------------------------")
				while True:
					hours=timeNode.get_value()/3600000
					minutes=(hours%1)*60
					seconds=(minutes%1)*60
					print("PLC Time:\t%d:%02d:%02d\tCar Temp:\t%.2f"%(hours,minutes,seconds,tempNode.get_value()))
					time.sleep(0.5)
			else:
				motorNode=Car.vars["motor"]["node"]
				motorValue=motorNode.get_value()
				print("Changing Motor Value from %s to %s"%(motorValue,not motorValue))
				motorNode.set_value(not motorValue)	
	except KeyboardInterrupt:
		pass
		
		
print("Connecting to DB")
eStore_DB=openCart_DB() #Connecting to DB
print("Connected")
order_query=eStore_DB.get_all_orders() #get info from all the orders in the DB
last_order=order_query["last_order"]
total_orders=len(order_query["orders"]) #total orders is equal to the length of the total orders found in th eDB
print("Total Orders:",total_orders)
print("Waiting for new orders..")
"""
Simple infinite loop that polls the DB and 
waits for any new row that is added to the DB table
Of course this is not the best method when working
with millions of entries but for sake of the programs size
 and scope of of the Lecture this will be enough.
"""
while True:
	order_query=eStore_DB.get_all_orders()
	if len(order_query["orders"])>total_orders:
		total_new_orders=len(order_query["orders"])-total_orders #this assumes that the DB does not erase orders
		for new_order in order_query["orders"][:total_new_orders]: #Get the last orders that are new     
			print("Detected new order [#%d]"%(new_order["order_id"]))
			products=eStore_DB.get_order_products(new_order["order_id"])
			example.connect()
			program_node=example.searchNode(example.client.get_objects_node(),default_PRG)
			if program_node==None:
				print("Are you sure that the OPC UA Server is set correctly?")
			Car=Car_OPCUA(program_node,example)
			v = 0	
			
			for product in products:
				
				print("Id %d,Name %s Qty:%d Total %d"%(product["product_id"],product["name"],product["quantity"],product["total"]))
				if (product["name"] == "BMX") or (product["name"] == "Folding") or (product["name"] == "Electric") or (product["name"] == "Road"):
				       BikeNode=Car.vars["eType"]["node"]
				       print("Bike- %s"%product["name"])
				       BikeNode.set_value(product["name"])
				       qtyNode=Car.vars["uiQty"]["node"]
				       x=ua.DataValue(ua.Variant(product["quantity"],ua.VariantType.Int16))
				       x.ServerTimestamp= None
				       x.SourceTimestamp= None
				       qtyNode.set_value(x)
				elif (product["name"] == "Bell") or (product["name"] == "Lights") or (product["name"] == "GPS") \
				or (product["name"] == "Speedometer") or (product["name"] == "Lock"):
					v = v+1
					BikeNode=Car.vars["aeAccessories[%s]"%v]["node"]
					print("Accessory- %s"%product["name"])
					BikeNode.set_value(product["name"])
			OrderNode=Car.vars["ulOrderNo"]["node"]
			q=ua.DataValue(ua.Variant((new_order["order_id"]),ua.VariantType.Int16))
			q.ServerTimestamp= None
			q.SourceTimestamp= None
			OrderNode.set_value(q)		
		total_orders+=total_new_orders

		
