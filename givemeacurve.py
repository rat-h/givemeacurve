from tkinter import *
from tkinter.font import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import json

class getdata(Frame):
	def __init__(self, master=None, filedb=None):
		Frame.__init__(self, master)
		self.pack()
		self.fln = None
		self.createWidgets()
		self.clkcondition = "none"
		self.xIleft  = None
		self.xIright = None
		self.yIup    = None
		self.yIdown  = None
		self.ImSize  = None
		self.curves  = {}
		self.marks   = []
		self.marksize= 5
		self.emarkcnt= -1
	def createWidgets(self):
		self.f = Frame(self)
		self.f.pack(side="right", fill="y")#, expand=True)
		self.OpenImage = Button(self.f, text="Open Image", command=self.readImage)
		self.OpenImage.grid(row=0,column=0, columnspan=2,sticky=W+E+N+S)
		self.Sep1  = Label(self.f, text = "Set Coordinate System").grid(row=1,column=0,sticky=W+E+N+S,columnspan=2)
		self.SetXL = Button(self.f, text="Set X-Left",  command=self.setXL).grid(row=2,column=0,sticky=W+E+N+S)
		self.SetXR = Button(self.f, text="Set X-Right", command=self.setXR).grid(row=3,column=0,sticky=W+E+N+S)
		self.SetYU = Button(self.f, text="Set Y-Up",      command=self.setYU).grid(row=5,column=0,sticky=W+E+N+S)
		self.SetYD = Button(self.f, text="Set Y-Down",    command=self.setYD).grid(row=4,column=0,sticky=W+E+N+S)
		self.xDleft  = Entry(self.f)
		self.xDleft.grid(row=2,column=1,sticky=W+E+N+S)
		self.xDleft.insert(0,"0.")
		self.xDright = Entry(self.f)
		self.xDright.grid(row=3,column=1,sticky=W+E+N+S)
		self.xDright.insert(0,"1.")
		self.yDup    = Entry(self.f)
		self.yDup.grid(row=5,column=1,sticky=W+E+N+S)
		self.yDup.insert(0,"1.")
		self.yDdown  = Entry(self.f)
		self.yDdown.grid(row=4,column=1,sticky=W+E+N+S)
		self.yDdown.insert(0, "0.")
		self.Sep2    = Label(self.f, text = "Named Curves").grid(row=6,column=0,sticky=W+E+N+S,columnspan=2)
		self.Sep3    = Label(self.f, text = "Curve Name").grid(row=7,column=0,sticky=W+E+N+S)
		self.CurveName = Entry(self.f)
		self.CurveName.grid(row=7,column=1,sticky=W+E+N+S)
		self.SartCurve = Button(self.f, text="Start Curve", command=self.sartCurve).grid(row=8, column=0,sticky=W+E+N+S)
		self.SartCurve = Button(self.f, text="Stop  Curve", command=self.stopCurve).grid(row=8, column=1,sticky=W+E+N+S)
		self.ShowCurve = Button(self.f, text="Show  Curve", command=self.showCurve).grid(row=9, column=0,sticky=W+E+N+S)
		self.ShowCurve = Button(self.f, text="Start Error", command=self.sartError).grid(row=10,column=0,sticky=W+E+N+S)
		self.Sep4    = Label(self.f, text = "File").grid(row=11,column=0,sticky=W+E+N+S,columnspan=2)
		self.Save = Button(self.f, text="Save", command=self.Save).grid(row=12,column=0,sticky=W+E+N+S)
		self.Load = Button(self.f, text="Load", command=self.Load).grid(row=12,column=1,sticky=W+E+N+S)
		
		self.Canvas = Canvas(self, width=900, height=600)
		self.Canvas.pack(side="left", fill="both", expand=True)
		
	def setXL(self):self.clkcondition = "lx"
	def setXR(self):self.clkcondition = "rx"
	def setYU(self):self.clkcondition = "uy"
	def setYD(self):self.clkcondition = "dy"
	
	def Save(self):
		if  self.xIleft  is None \
		 or self.xIright is None \
		 or self.yIup    is None \
		 or self.yIdown  is None \
		 or self.ImSize  is None : return
		options ={
			'defaultextension' : '.json',
			'filetypes': [('json', '.json')],
			'initialdir':".",
			'parent': self,
			'title':'Save to ...'
		}
		filename = asksaveasfilename(**options)
		if not filename : return
		xscale, yscale = (float(self.xDright.get()) - float(self.xDleft.get()))/float(self.xIright-self.xIleft), (float(self.yDup.get()) - float(self.yDdown.get()))/float(self.yIup-self.yIdown)
		with open(filename, "w") as fd:
			fdic ={}
			fdic['xscale']  = (float(self.xDright.get()) - float(self.xDleft.get()))/float(self.xIright-self.xIleft)
			fdic['yscale']  = (float(self.yDup.get()) - float(self.yDdown.get()))/float(self.yIup-self.yIdown)
			fdic['image']   = self.filename
			fdic["xDleft"]  = float(self.xDleft.get())
			fdic["xDright"] = float(self.xDright.get())
			fdic["yDup"]    = float(self.yDup.get())
			fdic["yDdown"]  = float(self.yDdown.get())
			fdic["xIleft"]  = float(self.xIleft)
			fdic["xIright"] = float(self.xIright)
			fdic["yIup"]    = float(self.yIup)
			fdic["yIdown"]  = float(self.yIdown)
			fdic["curves"]  = {}
			for name in self.curves:
				fdic["curves"][name] = []
				for x in self.curves[name]:
					if len(x) == 3:
						fdic["curves"][name].append([ float(x[0]-self.xIleft)*xscale+fdic["xDleft"],float(x[1]-self.yIdown)*yscale+fdic["yDdown"],x[2]*yscale ])
					else:
						fdic["curves"][name].append([ float(x[0]-self.xIleft)*xscale+fdic["xDleft"],float(x[1]-self.yIdown)*yscale+fdic["yDdown"] ] )
			fd.write(json.dumps(fdic)+"\n")
				
			
	def Load(self):
		if  self.xIleft  is None \
		 or self.xIright is None \
		 or self.yIup    is None \
		 or self.yIdown  is None \
		 or self.ImSize  is None : return
		options ={
			'defaultextension' : '.json',
			'filetypes': [('json', '.json')],
			'initialdir':".",
			'parent': self,
			'title':'Load from ...'
		}
		filename = askopenfilename(**options)
		if not filename : return
		xscale, yscale = float(self.xIright-self.xIleft)/(float(self.xDright.get()) - float(self.xDleft.get())), float(self.yIup-self.yIdown)/(float(self.yDup.get()) - float(self.yDdown.get()))
		xDleft = float( self.xDleft.get() )
		yDdown = float( self.yDdown.get() )
		
		with open(filename, "r") as fd:
			fdic = json.loads(fd.read())
		for name in fdic["curves"]:
			self.curves[name] = []
			for x in fdic["curves"][name]:
				if len(x) == 3:
					self.curves[name].append( [(x[0]-xDleft)*xscale+self.xIleft, (x[1]-yDdown)*yscale+self.yIdown, x[2]*yscale ] )
				else:
					self.curves[name].append( [(x[0]-xDleft)*xscale+self.xIleft, (x[1]-yDdown)*yscale+self.yIdown ] )
		
	def sartCurve(self):
		if self.CurveName.get() == "" : return
		if self.CurveName.get() == "none" : return
		self.clkcondition = self.CurveName.get()

	def stopCurve(self):
		self.clkcondition = "none"
		self.CurveName.delete(0, END)
		for w in self.marks:
			for m in w:
				self.Canvas.delete(m)
		self.marks = []
		self.emarkcnt = -1
	
	def showCurve(self):
		if self.CurveName.get() == "" : return
		if self.CurveName.get() == "none" : return
		curname = self.CurveName.get()
		self.stopCurve()
		if not curname in self.curves: return
		self.clkcondition = curname
		for w in self.curves[self.clkcondition]:
			if len(w) == 3:
				x,y,e = w
				self.marks.append( 
					[
					 self.Canvas.create_line(x-self.marksize,y-self.marksize,x+self.marksize,y+self.marksize,fill="blue",width=2),
					 self.Canvas.create_line(x-self.marksize,y+self.marksize,x+self.marksize,y-self.marksize,fill="blue",width=2),
					 self.Canvas.create_line(x,y-e,x,y+e,fill="blue",width=2)
					] )
			else:
				x,y = w
				self.marks.append( 
					[
					  self.Canvas.create_line(x-self.marksize,y-self.marksize,x+self.marksize,y+self.marksize,fill="blue",width=2),
					  self.Canvas.create_line(x-self.marksize,y+self.marksize,x+self.marksize,y-self.marksize,fill="blue",width=2)
					] )
			
	def sartError(self):
		if self.CurveName.get() == "" : return
		if self.CurveName.get() == "none" : return
		curname = self.CurveName.get()
		if not curname in self.curves: return
		if len(self.curves[curname]) < 1: return
		self.clkcondition = self.CurveName.get()
		self.emarkcnt=0
		for w in self.marks:
			for m in w:
				self.Canvas.delete(m)
		self.marks = []
		if len(self.curves[self.clkcondition][self.emarkcnt]) > 2:
			x,y,_ = self.curves[self.clkcondition][self.emarkcnt]
		else:
			x,y = self.curves[self.clkcondition][self.emarkcnt]
		self.marks.append( 
			[
			 self.Canvas.create_line(x-self.marksize,y-self.marksize,x+self.marksize,y+self.marksize,fill="blue",width=2),
			 self.Canvas.create_line(x-self.marksize,y+self.marksize,x+self.marksize,y-self.marksize,fill="blue",width=2)
			] )
			
	def readImage(self):
		"""TODO: Add all possible formats from PIL, please!"""
		options ={
			'filetypes': [('all files', '.*'), ('JPG', '.jpg'), ('PNG', '.png')],
			'initialdir':".",
			'parent': self,
			'title':'Select Image'
		}
		filename = askopenfilename(**options)
		if not filename : return
		self.filename = filename
		self.fln = Image.open(self.filename)
		self.ImSize = self.fln.size
		if self.ImSize[0] < self.ImSize[1]:
			self.marksize = self.ImSize[1]/150
		else:
			self.marksize = self.ImSize[0]/150
		self.Image = ImageTk.PhotoImage(self.fln)
		self.Canvas.config(width=self.ImSize[0], height=self.ImSize[1])
		self.Canvas.create_image( self.ImSize[0]/2+1, self.ImSize[1]/2+1 ,image=self.Image)
		self.Canvas.bind("<Button-1>", self.callback)
	def callback(self,event):
		if self.ImSize is None: return
		#canvas = event.widget
		x = event.x#canvas.canvasx(event.x)
		y = event.y#canvas.canvasy(event.y)
		if self.clkcondition == "none": return
		elif self.clkcondition == "lx":
			self.xIleft  = x
			self.clkcondition = "none"
			self.Canvas.create_line(x,y-self.ImSize[1]/20,x,y+self.ImSize[1]/20,fill="red", dash=(4, 4))
		elif self.clkcondition == "rx":
			self.xIright  = x
			self.clkcondition = "none"
			self.Canvas.create_line(x,y-self.ImSize[1]/20,x,y+self.ImSize[1]/20,fill="red", dash=(4, 4))
		elif self.clkcondition == "uy":
			self.yIup  = y
			self.clkcondition = "none"
			self.Canvas.create_line(x-self.ImSize[0]/20,y,x+self.ImSize[0]/20,y,fill="red", dash=(4, 4))
		elif self.clkcondition == "dy":
			self.yIdown  = y
			self.clkcondition = "none"
			self.Canvas.create_line(x-self.ImSize[0]/20,y,x+self.ImSize[0]/20,y,fill="red", dash=(4, 4))
		else:
			if self.emarkcnt >= 0:
				if len(self.curves[self.clkcondition][self.emarkcnt]) == 2:
					bx,by = self.curves[self.clkcondition][self.emarkcnt]
					er = abs(by-y)
					self.curves[self.clkcondition][self.emarkcnt].append(er)
				else:
					bx,by = self.curves[self.clkcondition][self.emarkcnt][:2]
					er = abs(by-y)
					self.curves[self.clkcondition][self.emarkcnt][2] = er
				self.marks[self.emarkcnt].append( self.Canvas.create_line(bx,by-er,bx,by+er,fill="blue",width=2) )
				self.emarkcnt += 1
				if self.emarkcnt < len(self.curves[self.clkcondition]):
					x,y = self.curves[self.clkcondition][self.emarkcnt][:2]
					self.marks.append( 
						[
						 self.Canvas.create_line(x-self.marksize,y-self.marksize,x+self.marksize,y+self.marksize,fill="blue",width=2),
						 self.Canvas.create_line(x-self.marksize,y+self.marksize,x+self.marksize,y-self.marksize,fill="blue",width=2)
						] )	
				else:
					self.stopCurve()
			else:
				if not self.clkcondition in self.curves:
					self.curves[self.clkcondition] = []
				self.curves[self.clkcondition].append( [x,y] )
				self.marks.append( 
					[ self.Canvas.create_line(x-self.marksize,y-self.marksize,x+self.marksize,y+self.marksize,fill="blue",width=2),
					  self.Canvas.create_line(x-self.marksize,y+self.marksize,x+self.marksize,y-self.marksize,fill="blue",width=2)
					] )
			

			


root=Tk()
dlg=getdata(root)
root.mainloop()
