from songdata import SongData
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.open_file_name = None
        
        self.init_window()
        self.create_menu()

    def init_window(self):    
        self.master.title("OpenSong Editor")
        self.grid(pady=10)

        left_frame = Frame(self)
        left_frame.pack(padx=10, side=LEFT)
        
        lyric_label = Label(left_frame, text="Chords/Lyrics")
        lyric_label.grid(row=0, column=0, sticky=W)
        self.lyric_input = Text(left_frame)
        self.lyric_input.grid(row=1, column=0, rowspan=30)
        
        right_frame = Frame(self)
        right_frame.pack(padx=10, fill=Y, side=LEFT)

        title_label = Label(right_frame, text="Title")
        title_label.grid(row=0, column=0, sticky=W)

        self.title_input = Text(right_frame, width=40, height=1)
        self.title_input.grid(row=1, column=0, columnspan=4)

        author_label = Label(right_frame, text="Author")
        author_label.grid(row=2, column=0, sticky=W)

        self.author_input = Text(right_frame, width=40, height=1)
        self.author_input.grid(row=3, column=0, columnspan=4)

        copy_label = Label(right_frame, text="Copyright")
        copy_label.grid(row=4, column=0, sticky=W)

        self.copy_input = Text(right_frame, width=40, height=1)
        self.copy_input.grid(row=5, column=0, columnspan=4)

        ccli_label = Label(right_frame, text="CCLI Song Number")
        ccli_label.grid(row=6, column=0, columnspan=2, sticky=W)

        self.ccli_input = Text(right_frame, width=15, height=1)
        self.ccli_input.grid(row=7, column=0, columnspan=2, sticky=W)
        
        sep = Separator(right_frame, orient=HORIZONTAL)
        sep.grid(row=8, column=0, sticky='we', pady=15, columnspan=4)

        pres_label = Label(right_frame, text="Presentation")
        pres_label.grid(row=9, column=0, sticky=W)

        self.pres_input = Text(right_frame, width=40, height=1)
        self.pres_input.grid(row=10, column=0, columnspan=4)

        capo_frame = Frame(right_frame)
        capo_frame.grid(row=11, column=0, pady=(15,5), columnspan=4, sticky='we')

        capo_label = Label(capo_frame, text="Capo")
        #capo_label.pack(side=LEFT)
        capo_label.grid(row=0, column=0, sticky=E)

        self.capo_val = StringVar()

        self.capo_input = OptionMenu(capo_frame, self.capo_val, '', '', '1', '2', '3', '4', '5')
        #self.capo_input.pack(side=LEFT)
        #self.capo_input.config(width=20)
        self.capo_input.grid(row=0, column=1, sticky=W)  

        capo_check_label = Label(capo_frame, text="Print Capo")
        capo_check_label.grid(row=0, column=2, padx=(40, 5), sticky=E)

        self.capo_check = BooleanVar()
        
        self.capo_check_input = Checkbutton(capo_frame, var = self.capo_check)
        self.capo_check_input.grid(row=0, column=3, sticky=W)
        self.capo_check.set(False)

        key_label = Label(right_frame, text="Key")
        key_label.grid(row=13, column=0, sticky=W)

        self.key_input = Text(right_frame, width=15, height=1)
        self.key_input.grid(row=14, column=0, columnspan=2, sticky=W)

    def create_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        self.menu = Menu(menu)
        self.menu.add_command(label="Open", command=self.populate_input)
        self.menu.add_command(label="Save", command=self.save, state="disabled")
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=exit)

        menu.add_cascade(label="File", menu=self.menu)

    def populate_input(self):
        self.open_file_name = filedialog.askopenfilename(title = "Select file")
        data = SongData(self.open_file_name)
        self.lyric_input.insert('1.0', data.lyrics)
        self.title_input.insert('1.0', data.title)
        self.author_input.insert('1.0', data.author)
        self.copy_input.insert('1.0', data.copyright)
        self.ccli_input.insert('1.0', data.ccli)
        self.capo_val.set(data.capo)
        self.capo_check.set(data.capo_print)

        self.key_input.insert('1.0', data.key)

        self.menu.entryconfig("Save", state="normal")
                      
    def save(self):
        if (self.open_file_name):
            data = SongData(self.open_file_name)
            data.lyrics = self.lyric_input.get('1.0', END)
            data.title = self.title_input.get('1.0', END)
            data.author = self.author_input.get('1.0', END)
            data.copyright = self.copy_input.get('1.0', END)
            data.ccli = self.ccli_input.get('1.0', END)
            data.capo = self.capo_val.get()
            data.capo_print = self.capo_check.get()

            data.save()  

root = Tk()

#size of the window
root.geometry("1366x768")

app = Window(root)
root.mainloop() 

