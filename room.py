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
		f=Frame(self)
		f.pack(side=RIGHT,padx=10,pady=10)
		sb=Scrollbar(f)
		sb.pack(side=RIGHT,fill=Y)
		self.canvas=Canvas(f,bd=1,relief=SUNKEN,yscrollcommand=sb.set,width=240,height=200)
		self.canvas.pack(fill=BOTH,expand=1)
		self.canvas.roomrates=[]
		sb.config(command=self.canvas.yview)
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
		if not tmb.askyesno("Confirm","Update the room " + room +"?"):
			return
		con=cdb.Db().connection()
		cur=con.cursor()
		if self.editroom==None:
			sql="insert into room (room_num) values (%s);"
			values=[room]
			cur.execute(sql,values)
			room=cur.lastrowid
		else:
			sql="update room set room_num=%s where id=%s;"
			values=[room,self.editroom]
			cur.execute(sql,values)
			room=self.editroom
		con.commit()
		for e in self.canvas.roomrates:
			rate=e.get()
			service=e.id
			sql="update roomservice set rate=%s where room=%s and service=%s;"
			cur.execute(sql,(rate,room,service))
			if cur.rowcount==0:
				sql ="insert ignore into roomservice(room,service,rate) values(%s,%s,%s);" 
				cur.execute(sql,(room,service,rate))
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
		cur=cdb.Db().connection().cursor()
		sql=("select roomservicelist.id as id,roomservicelist.name as service, roomservicelist.defaultrate as defaultrate, "
			 "roomservice.rate as rate from roomservicelist left join roomservice on roomservicelist.id=roomservice.service "
			 "and roomservice.room=%s left join room on roomservice.room=room.id;")
		cur.execute(sql,[room[1]])
		rows=cur.fetchall()
		self.canvas.delete(ALL)
		i=0
		for r in rows:
			f=Frame(self.canvas,bd=1,relief=RIDGE,pady=5)
			Label(f,text=r[1],width=20).pack(side=LEFT)
			e=DoubleVar()
			e.id=r[0]
			if r[3] is None:
				e.set(r[2])
			else:
				e.set(r[3])
			Entry(f,textvariable=e,width=8).pack(side=LEFT)
			self.canvas.roomrates.append(e)
			self.canvas.create_window(1,1+i*32,window=f,anchor=NW)
			i=i+1
		self.canvas.update_idletasks()
		self.canvas.config(scrollregion=self.canvas.bbox(ALL))
			
		
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
