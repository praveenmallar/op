from Tkinter import *
import connectdb as cdb
import tkMessageBox as tmb
import comp

class Room (Frame):

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
		self.delete=Button(f,text="Delete",command=self.delete)
		self.delete.pack(side=LEFT,padx=20)
		f=Frame(self,bd=1,relief=RIDGE,padx=10,pady=10)
		f.pack(pady=20,padx=20)
		self.editbox=StringVar()
		Entry(f,textvariable=self.editbox).pack(expand=1,pady=10)
		self.add=Button(f,text="Add",command=self.add)
		self.add.pack(side=LEFT,padx=20)
		self.rest=Button(f,text="Reset",command=self.reset)
		self.rest.pack(side=LEFT,padx=20)
		self.editroom=None
		self.packitems()
		
	def add(self):
		room=self.editbox.get()
		if self.editroom==None:
			sql="insert into room (room_num) values (%s);"
			values=[room]
		else:
			sql="update room set room_num=%s where id=%s;"
			values=[room,self.editroom]
		con=cdb.Db().connection()
		cur=con.cursor()
		cur.execute(sql,values)
		con.commit()
		self.packitems()
		
	def reset(self):
		self.editroom=None
		self.editbox.set("")
		
	def packitems(self):
		cur=cdb.Db().connection().cursor()
		sql="select * from room order by cast(room_num as unsigned), room_num;"
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
		
	def delete(self):
		room=self.rooms.get()
		if not tmb.askyesno("Confirm", "delete room "+room[0]+" ?"):
			return
		sql ="delete from room where id=%s;"
		con=cdb.Db().connection()
		cur=con.cursor()
		cur.execute(sql,[room[1]])
		con.commit()
		self.packitems()
		
		
if __name__=="__main__":
	Room(Tk()).mainloop()
