from tkinter import Tk, Button, Label, Frame, Toplevel, Canvas, Scrollbar, Message
from os import listdir, startfile
from os.path import isfile, join, realpath, dirname, getsize
from sys import argv
from math import ceil
from datetime import datetime
from PIL import ImageTk,Image
window = Tk()
window.geometry("640x640")
window.configure(bg="#25252f")
window.update()
CWD = dirname(argv[0])
ProjectsList = [f for f in listdir(CWD+"\projects") if (not isfile(join(CWD+"\projects", f)))]
mainframe = Frame(window,bg="#25252f")
mainframe.pack(fill="both",expand=1)
canvas = Canvas(mainframe,bg="#25252f")
canvas.pack(side="left",fill="both",expand=1)
scrollbar = Scrollbar(mainframe,orient="vertical",command=canvas.yview)
scrollbar.pack(side="right",fill="y")

def _bound_to_mousewheel(event):
	canvas.bind_all("<MouseWheel>", _on_mousewheel)
def _unbound_to_mousewheel(event):
	canvas.unbind_all("<MouseWheel>")
canvas.bind('<Enter>', _bound_to_mousewheel)
canvas.bind('<Leave>', _unbound_to_mousewheel)
def _on_mousewheel(event):
	canvas.yview_scroll(-1*(event.delta//120), "units")
	
window.bind_all("<MouseWheel>", _on_mousewheel)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>",lambda e: canvas.config(scrollregion=canvas.bbox("all")))
gridFrame = Frame(canvas,bg="#25252f")
canvas.create_window((0,0),window=gridFrame,anchor="nw")
class ProjectGUI(Toplevel):
	def __init__(self,parent, icon, date, description, path):
		super().__init__(parent)
		self.icon = icon
		self.date = date
		self.description = description
		self.configure(bg="#8b8b93")
		self.leftFrame = Frame(self,borderwidth=1,relief="solid",height=120,bg="#25252f")
		self.leftFrame.pack(side="left",anchor="n", fill="both",expand=1,padx=1,pady=2)
		
		leftPicFrame = Frame(self.leftFrame,bg="#77758d")
		leftPicFrame.pack(side="top",anchor="w",padx=5,pady=5,ipadx=2,ipady=2)
		try:
			pic = ImageTk.PhotoImage(Image.open(join(path,"icon.png")).resize((180,180),Image.NEAREST))
		except FileNotFoundError:
			pic = ImageTk.PhotoImage(Image.open(join(CWD,"image.png")).resize((180,180),Image.NEAREST))
		leftPic = Label(leftPicFrame,image=pic,bg="#77758d")
		leftPic.pack(side="top",pady=(3,0))
		leftPic.image = pic

		leftButtonFrame = Frame(self.leftFrame,bg="#25252f")
		leftButtonFrame.pack(side="top",anchor="w",fill="x",padx=5,pady=3,ipadx=1,ipady=1)
		for text in ["X","U","Y"]:
			leftButtonBorder = Frame(leftButtonFrame,bg="#77758d")
			leftButtonBorder.pack(side="left",padx=2)
			leftButton = Button(leftButtonBorder,text=text,bg="#25252f",fg="lightgrey")
			leftButton.pack(padx=2,pady=2)
		leftDescriptionFrame = Frame(self.leftFrame,bg="#25252f")
		leftDescriptionFrame.pack(side="top",anchor="w",fill="both",padx=5,pady=5)
		#leftDescriptionLabel = Label(leftDescriptionFrame,text=description,wraplength=window.winfo_width()//1.4,justify="left")
		#leftDescriptionLabel.pack(side="top")
		leftDescriptionMessage = Message(leftDescriptionFrame,text=description,width=180,justify="left",fg="#8b8b93",bg="#25252f")
		leftDescriptionMessage.pack(side="top",anchor="w")
		
		
		self.rightFrame = Frame(self)
		self.rightFrame.pack(side="right",anchor="n", fill="both", expand=1,padx=1,pady=2)

		rightFilesFrame = Frame(self.rightFrame,bg="#25252f")
		rightFilesFrame.pack(side="top",anchor="w",fill="both",expand=1,ipadx=3,ipady=5)
		rightFilesCanvas = Canvas(rightFilesFrame,bg="#25252f")
		rightFilesCanvas.pack(side="left",fill="both",expand=1)
		rightFilesScrollbar = Scrollbar(rightFilesFrame,orient="vertical",command=rightFilesCanvas.yview)
		rightFilesScrollbar.pack(side="right",fill="y")
		
		def _bound_to_mousewheel(event):
			rightFilesCanvas.bind_all("<MouseWheel>", _on_mousewheel)
		def _unbound_to_mousewheel(event):
			rightFilesCanvas.unbind_all("<MouseWheel>")
		rightFilesCanvas.bind('<Enter>', _bound_to_mousewheel)
		rightFilesCanvas.bind('<Leave>', _unbound_to_mousewheel)
		def _on_mousewheel(event):
			rightFilesCanvas.yview_scroll(-1*(event.delta//120), "units")		
			
		rightFilesCanvas.configure(yscrollcommand=rightFilesScrollbar.set)
		rightFilesCanvas.bind("<Configure>",lambda e: rightFilesCanvas.config(scrollregion= rightFilesCanvas.bbox("all"))) 
		rightFilesCanvasFrame = Frame(rightFilesCanvas,bg="#25252f")
		window.update() # necessary for .winfo_width() to work. Tkinter will know width only when it's done rendering it
		
		rightFilesCanvas.create_window((0,0),window=rightFilesCanvasFrame, anchor="nw",width=rightFilesCanvas.winfo_width())
		for f in listdir(path):
			fileFrame = Frame(rightFilesCanvasFrame,bg="#25252f")
			fileFrame.pack(side="top",anchor="w",fill="x",expand=1,padx=3,pady=3)
			def funcGen(file, event=None):
				def func(event=None):
					try:startfile(join(path,file))
					except OSError:print("No default app set")
				return func
			fileFrame.bind("<Button-1>",funcGen(f))
			
			if(isfile(f)):
				name = "file.png"
			else:
				name = "directory.png"
			iconImage = ImageTk.PhotoImage(Image.open(join(CWD,name)).resize((45,45),Image.NEAREST))
			iconLabel = Label(fileFrame,image=iconImage,bg="#25252f")
			iconLabel.bind("<Button-1>",funcGen(f))
			iconLabel.image = iconImage
			iconLabel.pack(side="left")

			fileBorderFrame = Frame(fileFrame,bg="#87878f")
			fileBorderFrame.pack(side="left",fill="both",expand=1,ipadx=1,padx=4)
			nameLabel = Label(fileBorderFrame,text=f,font="Calibri 22",justify="left",anchor="w",bg="#25252f",fg="lightgrey")
			nameLabel.pack(side="left",padx=2,fill="x",expand=1)
			nameLabel.bind("<Button-1>",funcGen(f))

		rightBottomBorder = Frame(self.rightFrame,bg="#8b8b93")
		rightBottomBorder.pack(side="top",anchor="w",fill="both")
		rightBottomFrame = Frame(rightBottomBorder,height=70,bg="#25252f")
		rightBottomFrame.pack(side="top",anchor="w",fill="both",expand=1,padx=(0,1),pady=(2,0))
		window.update()
		
class Project():
	def __init__(self,projectName):
		self.name = projectName
		filePath = ""
		try:
			informationFile = [f for f in listdir(CWD+"\\projects\\"+projectName) if f[-5:]==".info"][0]
		except IndexError:
			print("no information file")
			filePath = CWD+"\\projects\\"+projectName+"\\"+projectName+".info"
			open(filePath,"w")
		else:
			filePath = join(CWD+"\\projects\\"+projectName,informationFile)
		
		if(getsize(filePath)==0):
			with open(filePath,"w") as file:
				self.icon = join(CWD,"empty.png")
				now = datetime.now()
				#self.date = "-".join((map(str,now.day,now.month,now.year)) + " " + ":".join(map(str,now.hour,now.minute,now.second)))
				self.date = str(now)
				self.description = "no description here yet"
				file.write("\n".join((self.icon,self.date,self.description)))
		else:
			with open(filePath,"r") as file:
				self.icon = file.readline()
				self.date = file.readline()
				self.description = file.readline()
	def OpenGUI(self,event):
		projectWindow = ProjectGUI(window, self.icon,self.date,self.description, CWD+"\\projects\\"+self.name)
		projectWindow.grab_set()
		projectWindow.resizable(width=False, height=False)

gridSide = ceil(len(ProjectsList)**0.5)
i = 0
#errorImage = ImageTk.PhotoImage(Image.open(join(CWD,"empty.png")).resize((205,205),Image.NEAREST))
errorImage = ImageTk.PhotoImage(Image.new("RGB",(205,205),(37,37,45)))
ImageTk.PhotoImage(Image.new("RGB",(1,1),(0,0,0)))
done = False
while not done:
	rowFrame = Frame(gridFrame,bg="lightgrey")
	rowFrame.pack(side="top",anchor="w",expand=1)
	for column in range(3):
		if(i>=len(ProjectsList)):
			#label = Label(rowFrame,image=pixelVirtual,width=162,borderwidth=1,relief="solid",compound="c")
			label = Label(rowFrame,image=errorImage,bg="#25252f")
			label.image = errorImage
			label.pack(side="left",ipadx=3,ipady=3)
			continue
		#label = Label(rowFrame,image=pixelVirtual,text=ProjectsList[i],borderwidth=1,relief="solid",width=160, compound="c")
		try:
			image = ImageTk.PhotoImage(Image.open(join(CWD,"projects",ProjectsList[i],"icon.png")).resize((205,205),Image.NEAREST))
		except FileNotFoundError:
			image = ImageTk.PhotoImage(Image.open(join(CWD,"image.png")).resize((205,205),Image.NEAREST))
		label = Label(rowFrame,image=image,borderwidth=1,relief="solid")#69
		label.image = image
		project = Project(ProjectsList[i])
		label.bind("<Button-1>",project.OpenGUI)
		
		label.pack(side="left")
		i+=1
	if(i>=len(ProjectsList)):
		done = True

window.mainloop()