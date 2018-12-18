#!/usr/bin/env python
from Tkinter import *
import printer as printbill
import shelve
import datetime as dt
import tkMessageBox
import connectdb as cdb

class Pharma():

	def __init__(self):
		self.master=Tk()
		cdb.checkdb()
		self.master.config(width=600,height=400)
		self.master.title("Mukunda Hospital")
		self.addmenus()
		self.addshortcuts()
		f=Frame(self.master)
		f.pack()
		self.master.mainloop()

	def addshortcuts(self):
		f=Frame(self.master,bd=1,relief=SUNKEN)
		f.pack()
		photo=PhotoImage(file="./images/bill.png")
		b=Button(f,image=photo,text="bill",compound=BOTTOM,width=100,height=100)
		b.pack(side=LEFT)

	def addmenus(self):
		menu=Menu(self.master)

		self.master.config(menu=menu)


if __name__=="__main__":
	Pharma()
