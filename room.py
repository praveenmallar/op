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
		self.editbox=Entry(f)
		self.editbox.pack(expand=1,pady=10)
		self.add=Button(f,text="Add",command=self.add)
		self.add.pack(side=LEFT,padx=20)
		self.reset=Button(f,text="Reset",command=self.reset)
		self.reset.pack(side=LEFT,padx=20)
		self.editroom=None
		self.packitems()
		
	def packitems(self):
		pass
		
	def add(self):
		pass
		
	def reset(self):
		pass
		
	def edit(self):
		pass
		
	def delete(self):
		pass
		
if __name__=="__main__":
	Room(Tk()).mainloop()
