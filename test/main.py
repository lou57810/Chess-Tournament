from tkinter import *

ws = Tk()
ws.title('PythonGuides')
ws.geometry('200x200')

ep = ''
def keyLog(k):
    global ep
    ep = ep + str(k)
    actn.set(ep)

actn = StringVar()
Entry(ws, textvariable=actn).pack()

one_Btn = Button(ws, text='1', command=lambda: keyLog(1), padx=5, pady=5)
two_Btn = Button(ws, text='2', command=lambda: keyLog(2), padx=5, pady=5)
three_Btn = Button(ws, text='3', command=lambda: keyLog(3), padx=5, pady=5)

one_Btn.pack()
two_Btn.pack()
three_Btn.pack()

ws.mainloop()