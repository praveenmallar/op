from Tkinter import *
import connectdb as cdb
import tkMessageBox as tmb
import comp

class Roomservicelist (Frame):

	def __init__ (self, parent=None):
		
		if not parent:
			parent=Toplevel()
		Frame.__init__(self,parent)
		self.pack()
		self.rooms=comp.myComp2(self,listheight=10)
		self.rooms.pack()
		f=Frame(self)
		f.pack(pady=20)
		self.edit=Button(f,text="Edit",command=self.edit)
		self.edit.pack(side=LEFT,padx=20)
		f=Frame(self,bd=1,relief=RIDGE,padx=10,pady=10)
		f.pack(pady=20,padx=20)
		self.editbox=StringVar()
		self.defaultrate=DoubleVar()
		Entry(f,textvariable=self.editbox).pack(expand=1,pady=10)
		Label(f,text="Rate:").pack()
		Entry(f,textvariable=self.defaultrate).pack(expand=1,pady=10)
		self.add=Button(f,text="Add",command=self.add)
		self.add.pack(side=LEFT,padx=20)
		self.rest=Button(f,text="Reset",command=self.reset)
		self.rest.pack(side=LEFT,padx=20)
		self.editroom=None
		self.packitems()
		
	def add(self):
		room=self.editbox.get()
		rate=self.defaultrate.get()
		if not tmb.askyesno("Confirm","Update room service " + room +" rate "+str(rate)+" ?"):
			return
		if self.editroom==None:
			sql="insert into roomservicelist (name,defaultrate) values (%s,%s);"
			values=[room,rate]
		else:
			sql="update roomservicelist set name=%s,defaultrate=%s where id=%s;"
			values=[room,rate,self.editroom]
		con=cdb.Db().connection()
		cur=con.cursor()
		cur.execute(sql,values)
		con.commit()
		self.packitems()
		
	def reset(self):
		self.editroom=None
		self.editbox.set("")
		self.defaultrate.set(0)
		
	def packitems(self):
		cur=cdb.Db().connection().cursor()
		sql="select * from roomservicelist order by name;"
		cur.execute(sql)
		rows=cur.fetchall()
		rooms=[]
		for r in rows:
			rooms.append([r[1],r[0]])
		self.rooms.changelist(rooms)
		self.reset()
		
	def edit(self):
		room=self.rooms.get()
		self.editroom=room[1]
		self.editbox.set(room[0])
		cur=cdb.Db().connection().cursor()
		sql="select defaultrate from roomservicelist where id= %s;"
		cur.execute(sql,[self.editroom])
		rate=cur.fetchall()[0][0]
		self.defaultrate.set(rate)
				

		
if __name__=="__main__":
	Roomservicelist(Tk()).mainloop()
