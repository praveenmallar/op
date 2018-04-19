from Tkinter import *
import connectdb as cdb
import tkMessageBox as tmb
import comp


class Editor (Frame):
	
	def __init__(self,parent=None,id=None,table="service",fieldname="name",fieldrate="rate"):
		if not parent:
			parent=Toplevel()
		Frame.__init__(self,parent)
		self.table=table
		self.fieldname=fieldname
		self.fieldrate=fieldrate
		self.serviceid=None
		self.lister=None
		self.name=StringVar()
		self.rate=DoubleVar()
		Label(self,text=self.table).grid(row=0,column=0)
		Label(self,text=fieldrate).grid(row=1,column=0)
		Entry(self,text=self.name).grid(row=0,column=1,sticky=E+W,padx=10,pady=10)
		Entry(self,text=self.rate).grid(row=1,column=1,sticky=E+W,padx=10,pady=10)
		self.save=Button(self,text="save",command=self.save)
		self.save.grid(row=3,column=1,padx=10,pady=10)
		self.save.bind("<Return>",self.save)
		if id:self.setId(id)

	def setId(self,id=None):
		self.serviceid=id
		if not id:
			self.name.set("")
			self.rate.set("")
			return
		cur=cdb.Db().connection().cursor()
		cur.execute("select * from "+self.table+" where id=%s;",[id])
		row=cur.fetchone()
		self.name.set(row[1])
		self.rate.set(row[2])
	
	def load(self,id=None):
		self.setId(id)
		
	def save(self):
		if self.serviceid:
			print "serviceid"
			print self.table
			sql="update "+self.table+" set %s=%s, %s=%s where id=%s;"
			argtable=(self.fieldname,self.name.get(),self.fieldrate,self.rate.get(),self.serviceid)
			infostring="service updated"
		else:
			print "noserviceid"
			sql="insert into "+self.table+" (%s,%s) values(%s,%s);"
			argtable=(self.fieldname,self.fieldrate,self.name,get(),self.rate.get())
			infostring="added service"
		con=cdb.Db().connection()
		cur=con.cursor()
		try:
			print argtable
			cur.execute(sql,argtable)
			con.commit()
			tmb.showinfo("Success",infostring,parent=self.master)
			self.lister.reload()
			self.setId(None)
		except Exception, e:
			tmb.showerror("Failure",e, parent=self.master)
	

class Lister(Frame):
		
	def __init__(self,parent=None,Editor=None):
		if not parent:
			parent=Tk()
		Frame.__init__(self,parent)
		self.editor=Editor
		self.f=None
		self.packitems()
		
	def packitems(self):
		if self.f:
			self.f.pack_forget()
		self.f=Frame(self)
		self.f.pack()
		self.list=comp.myComp2(self.f,listheight=10)
		self.list.pack()
		f=Frame(self.f)
		f.pack(ipadx=10,ipady=10)
		self.button=Button(f,text="edit",command=self.load)
		self.button.pack(side=LEFT,padx=20,pady=20)
		self.button.bind("<Return>",self.load)
		self.deleteButton=Button(f,text="Delete",command=self.delete)
		self.deleteButton.pack(side=LEFT,padx=20,pady=20)
		self.add=Button(f,text="New",command=self.new)
		self.add.pack(side=LEFT,padx=20,pady=20)
		self.reload()
		
	def reload(self):
		cur=cdb.Db().connection().cursor()
		sql="select * from service;"
		cur.execute(sql)
		rows=cur.fetchall()
		temp=[]
		for r in rows:
			temp.append([r[1]+" :"+str(r[2]),r[0]])
		self.list.changelist(temp)		

	def new(self):
		self.editor.load()

	def load(self,e=None):
		id=self.list.get()[1]
		self.editor.load(id)

	def delete(self):
		item=self.list.get()
		if not tmb.askyesno("Confirm","Delete the service "+item[0]+"?",parent=self.master):
			return
		sql="delete from service where id=%s;"
		con=cdb.Db().connection()
		cur=con.cursor()
		cur.execute(sql,[item[1]])
		con.commit()
		self.packitems()	

class Service(Frame):
	def __init__(self,parent=None,*arg,**karg):
		if not parent:
			parent=Toplevel()
		Frame.__init__(self,parent,*arg,**karg)
		self.pack()
		e=Editor(self)
		l=Lister(self,e)
		e.lister=l
		l.pack(padx=25,pady=25)
		e.pack(padx=25,pady=25)
		
		
if __name__=="__main__":
	Service(Tk()).mainloop()
