from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from tkinter import messagebox
import random
from googletrans import Translator
import os


###############
'''
configfile = open("installation.txt","w")

L = ["pip install gtts \n",
	"pip install playsound \n",
	"pip install googletrans\n",
	"pip install gspread \n",
	"pip install oauth2client \n",
	"https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio \n",
	"flashcard.ico \n",
	"tab_flashcard.png \n",
	"tab_vocab.png \n",
	"translate.png \n",] 
configfile.writelines(L)
'''



deletemp3 = True 
allfolder = os.listdir()
################
# Config

import csv
datasettings = [['https://docs.google.com/spreadsheets/d/18w6DB9Lz_gZT0Cs_LSj1xqiy5435463fNxWmOpgPlLE'],['Japanese','Thai']]

def writedata(data):
	with open('config2.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		fw.writerows(data)

def writevocab():
	data = [['こんにちは','สวัสดีตอนกลางวัน'],
				['こんばんは','สวัสดีตอนบ่าย']]
	with open('vocab.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		fw.writerows(data)

#allfolder = ['config.csv']
if 'config2.csv' not in allfolder:
	writedata(datasettings)
#writedata(datasettings)


if 'vocab.csv' not in allfolder:
	writevocab()


def readconfig():
	with open('config2.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		conf = list(fr)
		print(conf)

		urlsheet = conf[0][0]
		column1 = conf[1][0]
		column2 = conf[1][1]
	return (urlsheet,column1,column2)


def readvocab():
	with open('vocab.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		conf = list(fr)
		print(conf)
	return conf


################



if deletemp3:
	for f in allfolder:
		if f[-3:] == 'mp3':
			os.remove(f)


import random
randomnum = list(range(65,90)) #gen A-z for ascii
global playagain
playagain = True

def generatename():
	nm = ''
	for i in range(15):
		rd = chr(random.choice(randomnum))
		nm += rd
	nm += '.mp3'
	return nm

allfilename = []


#################GOOGLE SHEET##################


sheeturl,columnname1,columnname2 = readconfig()


GOOGLESHEETURL = sheeturl

#pip install gspread oauth2client
connection = False
global allvocab
try:
	import gspread
	from pprint import pprint
	from oauth2client.service_account import ServiceAccountCredentials

	scope = ['https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/spreadsheets',
			'https://www.googleapis.com/auth/drive.file',
			'https://www.googleapis.com/auth/drive']

	creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
	client = gspread.authorize(creds)
	url = GOOGLESHEETURL
	sheet = client.open_by_url(url)
	sheet = sheet.get_worksheet(0)
	data = sheet.get_all_records()

	#allvocab = [[d['Japanese'],d['Thai']] for d in data]
	allvocab = [[d[columnname1],d[columnname2]] for d in data]
	connection = True
except:
	print('ไม่สามารถเชื่อมต่อกับ Google Sheet ได้')
	
	# allvocab = [['こんにちは','สวัสดีตอนกลางวัน'],
	# 			['こんばんは','สวัสดีตอนบ่าย']]

	allvocab = readvocab()


def add_vocab(list_data):
	sheet.insert_row(list_data,count + 2)

#################GOOGLE SHEET##################
import webbrowser
def ConfigSheet():
	url = GOOGLESHEETURL
	webbrowser.open(url)


def UpdateVocab():
	global allvocab
	v_statusbar.set('Updating Vocab...')
	try:
		url = GOOGLESHEETURL
		sheet = client.open_by_url(url)
		sheet = sheet.get_worksheet(0)
		data = sheet.get_all_records()

		allvocab = [[d[columnname1],d[columnname2]] for d in data]

		vocablist.delete(*vocablist.get_children())
		for vc in allvocab:
			vocablist.insert('','end',value=vc)
	except:
		messagebox.showerror('Error','มีปัญหาการเชื่อมต่อ')


#################GOOGLE SHEET##################

GUI = Tk()
GUI.title('โปรแกรมฝึกภาษา')
GUI.geometry('1100x600+0+0')
GUI.state('zoomed')
try:
	GUI.iconbitmap('flashcard.ico')
except:
	pass


menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
# filemenu.add_command(label='Close', command=GUI.quit)
filemenu.add_command(label='Config Google Sheet',command=ConfigSheet)
menubar.add_cascade(label='File',menu=filemenu)

vocabmenu = Menu(menubar,tearoff=0)
vocabmenu.add_command(label='Update Vocab',command=UpdateVocab)
vocabmenu.add_command(label='Add Vocab',command=lambda: messagebox.showinfo('Tab 3','กรุณาเลือกแท็บ 3'))
menubar.add_cascade(label='Vocab',menu=vocabmenu)


import webbrowser
def ContactUs():
	url = 'http://uncle-engineer.com'
	webbrowser.open(url)

def UncleEngineer():
	url = 'https://www.facebook.com/UncleEngineer'
	webbrowser.open(url)

helpmenu = Menu(menubar,tearoff=0)
helpmenu.add_command(label='Contact Us',command=ContactUs)
helpmenu.add_command(label='Donate',command=ContactUs)
helpmenu.add_command(label='Uncle Engineer',command=UncleEngineer)
menubar.add_cascade(label='Help',menu=helpmenu)



Font = ('TH Sarabun',16)
TKFont = ttk.Style()
TKFont.configure('TButton', font=('TH Sarabun', 12))

Tab = Notebook(GUI)

F1 = Frame(Tab)
F2 = Frame(Tab)
F3 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

try:

	flashcard = PhotoImage(file='tab_flashcard.png')
	vocab = PhotoImage(file='tab_vocab.png')
	transicon = PhotoImage(file='translate.png')

	Tab.add(F1, text='Flashcard', image=flashcard,compound='top')
	Tab.add(F2, text='All vocab', image=vocab,compound='top')
	Tab.add(F3, text='Translate', image=transicon,compound='top')
except:
	Tab.add(F1, text='Flashcard')
	Tab.add(F2, text='All vocab')
	Tab.add(F3, text='Translate')



global current_vocab

current_vocab = None
global checked
checked = False

def RandomFlashcard(event=None):
	v_check.set('')
	global checked
	checked =False
	vc = random.choice(allvocab)
	global current_vocab
	current_vocab = vc
	print(vc)
	v_vocab.set(vc[0])
	v_trans.set('')
	global playagain
	playagain = True

def ShowTranslate(event=None):
	v_trans.set(current_vocab[1])



def CheckTranslate(event=None):
	global checked
	print([v_check.get()],[current_vocab[1]])
	if v_check.get() == current_vocab[1].replace(' ','') and checked != True:
		v_score.set(int(v_score.get()) + 1)
		
		checked = True
		#RandomFlashcard() #uncomment this if autonextword

	v_trans.set(current_vocab[1])


##########################

from gtts import gTTS
from playsound import playsound


def SpeakNow(event=None):
	print(allfilename)
	print(v_vocab.get())
	global playagain
	tts = gTTS(text=v_vocab.get(), lang='de')

	if playagain == True:
		name = generatename()
		allfilename.append(name)

		tts.save(name)
		playagain = False


	
	if len(allfilename) > 1:
		os.remove(allfilename[0])
		del allfilename[0]
	playsound(allfilename[0])



def SpeakNow2(event=None):


	#v_translatenow.get()
	global playagain

	if v_radio.get() == 'de':
		tts = gTTS(text=v_transvocab.get(), lang='de')
	else:
		tts = gTTS(text=v_texttras.get(), lang='de')
	
	if playagain == True:
		name = generatename()
		allfilename.append(name)

		tts.save(name)
		playagain = False


	
	if len(allfilename) > 1:
		os.remove(allfilename[0])
		del allfilename[0]
	playsound(allfilename[0])



GUI.bind('<F4>',SpeakNow2)

def SpeakNow3(vocab_sound):


	#v_translatenow.get()
	global playagain
	tts = gTTS(text=vocab_sound, lang='de')

	if playagain == True:
		name = generatename()
		allfilename.append(name)

		tts.save(name)
		playagain = True
	
	if len(allfilename) > 1:
		os.remove(allfilename[0])
		del allfilename[0]
	playsound(allfilename[0])
##########################


FB0 = Frame(F1)
FB0.place(x=100,y=200)


check_label = ttk.Label(FB0,text='ตรวจความหมาย',font=('Angsana New',20))
check_label.grid(row=0,column=0)

v_check = StringVar()
check_vocab = ttk.Entry(FB0,textvariable=v_check,font=('Angsana New',20),width=50)
check_vocab.grid(row=0,column=1,padx=20,pady=20)
check_vocab.focus()
#### BIND #####
check_vocab.bind('<Return>',CheckTranslate)
GUI.bind('<F1>',RandomFlashcard)
GUI.bind('<F2>',ShowTranslate)

FB1 = Frame(F1)
FB1.place(x=100,y=300)


nextvocab = ttk.Button(FB1,text='คำศัพท์ถัดไป',command=RandomFlashcard)
nextvocab.grid(row=1,column=1,padx=20,ipadx=20,ipady=10)

nextvocab = ttk.Button(FB1,text='โชว์คำแปล',command=ShowTranslate)
nextvocab.grid(row=1,column=2,padx=20,ipadx=20,ipady=10)

checkvocab = ttk.Button(FB1,text='เช็คคำแปล',command=CheckTranslate)
checkvocab.grid(row=1,column=3,padx=20,ipadx=20,ipady=10)

speak = ttk.Button(FB1,text='อ่านออกเสียง',command=SpeakNow)
speak.grid(row=1,column=4,padx=20,ipadx=20,ipady=10)

GUI.bind('<F3>',SpeakNow)

#######LABEL VOCAB########
#FB2 = Frame(F1)
#FB2.place(x=100,y=50)
v_vocab = StringVar()
v_trans = StringVar()

show_vocab = ttk.Label(F1, textvariable=v_vocab,font=('Angsana New',30,'bold'))
show_vocab.place(x=100,y=20)

show_translate = ttk.Label(F1, textvariable=v_trans,font=('Angsana New',30,'bold'),foreground='green')
show_translate.place(x=100,y=70)

v_score = StringVar()
v_score.set('0')

score_label =ttk.Label(F1,text='คะแนน',font=('Angsana New',30))
score_label.place(x=50,y=400)

score = ttk.Label(F1, textvariable=v_score,font=('Angsana New',30,'bold'),foreground='red')
score.place(x=150,y=400)

if connection == False:
	messagebox.showerror('Connection Error','ไม่สามารถเชื่อมต่อกับ Google Sheet ได้')



def SoundTreeview(event=None):
	global playagain
	try:
		select = vocablist.selection()
		data = vocablist.item(select)
		print(data)
		vocabsound = data['values'][0]
		SpeakNow3(vocabsound)
		playagain == False

	except:
		messagebox.showinfo('Please Select Row','กรุณาเลือกคำศัพท์ก่อน')


############## TAB2 #############

L1 = ttk.Label(F2,text='คำศัพท์ทั้งหมด',font=('Angsana New',20)).pack()

header = ['Vocab','Translation']

vocablist = ttk.Treeview(F2, columns=header, show='headings',height=10)
vocablist.place(x=20,y=50)

###############
vocablist.bind('<Double-1>', SoundTreeview)

for hd in header:
	#tree.column("#0",minwidth=0,width=100, stretch=NO)
	vocablist.heading(hd,text=hd)
	#print('test')

headerwidth = [(100,600),(100,400)]

for hd,W in zip(header,headerwidth):
	vocablist.column(hd,minwidth=W[0],width=W[1])


for vc in allvocab:
	vocablist.insert('','end',value=vc)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Angsana New', 30))
style.configure("Treeview", font=('Angsana New', 20),rowheight=40)


scrolling = ttk.Scrollbar(F2, orient="vertical", command=vocablist.yview)
scrolling.pack(side='right',fill='y')
vocablist.configure(yscrollcommand=scrolling.set)


##############################
def add_vocab(list_data):
	data = sheet.get_all_records()
	count = len(data)
	sheet.insert_row(list_data,count + 2)

Lam = Translator()

def TranslateNow(event=None):
	print(v_radio.get(), v_texttras.get())

	trans = Lam.translate(v_texttras.get(),dest=v_radio.get())
	alltext = ''
	alltext += trans.text
	if trans.pronunciation != None and v_radio.get() == 'de':
		alltext += '\nคำอ่าน: ' + trans.pronunciation
	v_translatenow.set(alltext)
	v_transvocab.set(trans.text)
	if savetosheet.get() == 1:
		try:
			if v_radio.get() == 'th':
				add_vocab([v_texttras.get(),trans.text])
			else:
				add_vocab([trans.text,v_texttras.get()])

			v_statusbar.set('Save to Sheet: Done!')
		except:
			print('Can not save')
	global playagain
	playagain = True

L1 = ttk.Label(F3, text = 'กรุณาใส่คำที่ต้องการแปล',font=('Angsana New',20))
L1.pack(pady=10)


FR0 = Frame(F3)
FR0.pack()

v_radio = StringVar()

RB1 = ttk.Radiobutton(FR0,text='German',variable=v_radio,value='de')
RB2 = ttk.Radiobutton(FR0,text='Thai',variable=v_radio,value='th')
RB1.invoke()

RB1.grid(row=0,column=1)
RB2.grid(row=0,column=2)

savetosheet = IntVar()
savetosheet.set(0)

cbtn = ttk.Checkbutton(F3,text='Save to Google Sheet',variable=savetosheet)
cbtn.pack()

if connection == False:
	cbtn.config(state='disabled')

v_texttras = StringVar() #เก็บสิ่งที่เราพิมพ์ไว้
E1 = ttk.Entry(F3, textvariable = v_texttras,font=('Angsana New',20),width=50)
E1.pack(pady=20)
E1.bind('<Return>',TranslateNow)


EBF = Frame(F3)
EBF.pack(pady=20,ipadx=20,ipady=10)

EB1 = ttk.Button(EBF,text='แปล',command=TranslateNow)
EB1.grid(row=0,column=0,padx=10,ipadx=15,ipady=10)

EB2 = ttk.Button(EBF,text='อ่านออกเสียง',command=SpeakNow2)
EB2.grid(row=0,column=1,padx=10,ipadx=15,ipady=10)

#EB3 = ttk.Button(EBF,text='อ่านออกเสียง (ความหมายญี่ปุ่น)',command=SpeakNow3)
#EB3.grid(row=0,column=2,padx=10,ipadx=15,ipady=10)

v_transvocab =StringVar()

v_translatenow = StringVar()
v_translatenow.set('----Result----')

F31 = Frame(F3)
F31.pack(pady=20)

trans_label =ttk.Label(F31,text='คำแปล',font=('Angsana New',30))
trans_label.pack()

resulttext = ttk.Label(F31, textvariable=v_translatenow,font=('Angsana New',30,'bold'),foreground='red')
resulttext.pack()


def on_click(event):
    print('widget:', event.widget)
    print('x:', event.x)
    print('y:', event.y)

    #selected = nb.identify(event.x, event.y)
    #print('selected:', selected) # it's not usefull

    clicked_tab = Tab.tk.call(Tab._w, "identify", "tab", event.x, event.y)
    print('clicked tab:', clicked_tab)

    active_tab = Tab.index(Tab.select())
    print(' active tab:', active_tab)

    if clicked_tab == 2:
    	E1.focus()

    # if clicked_tab == active_tab:
    #     Tab.forget(clicked_tab)

Tab.bind('<Button-1>', on_click)

##### STATUS BAR ####
v_statusbar = StringVar()

statusbar = Label(F3, textvariable=v_statusbar, bd=1, relief=SUNKEN, anchor='w')
statusbar.pack(side=BOTTOM, fill=X)


GUI.mainloop()