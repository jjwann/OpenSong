from songdata import SongData
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from xml.etree import ElementTree
import sys

class Window(Frame):
    """ This is the main frame of the application
    """
    def __init__(self, master=None):
        """
            Args:
                master: The underlying tcl/tk interpreter
        """
        Frame.__init__(self, master)                 
        self.master = master
        self.open_file_name = None
        
        self.init_window()
        self.create_menu()

    def init_window(self):
        """ Creates the controls for the application
        """
        self.master.title("OpenSong Editor")
        self.grid()

        #The left frame contains the lyrics box
        left_frame = Frame(self)
        left_frame.pack(padx=10, pady=10, side=LEFT)
        
        lyric_label = Label(left_frame, text="Chords/Lyrics")
        lyric_label.grid(row=0, column=0, sticky=W)
        self.lyric_input = Text(left_frame)
        self.lyric_input.grid(row=1, column=0, rowspan=30)

        scrollb = Scrollbar(left_frame, command=self.lyric_input.yview)
        scrollb.grid(row=1, column=1, rowspan=30, sticky='nsew')
        self.lyric_input['yscrollcommand'] = scrollb.set

        #Everything else is on the right frame
        right_frame = Frame(self)
        right_frame.pack(padx=10, pady=10, fill=Y, side=LEFT)

        #Displays the song title
        title_label = Label(right_frame, text="Title")
        title_label.grid(row=0, column=0, sticky=W)

        self.title_input = Entry(right_frame, width=30)
        self.title_input.grid(row=1, column=0, columnspan=4, sticky=W)

        #Displays the song author
        author_label = Label(right_frame, text="Author")
        author_label.grid(row=2, column=0, sticky=W)

        self.author_input = Entry(right_frame, width=30)
        self.author_input.grid(row=3, column=0, columnspan=4, sticky=W)

        #Copyright
        copy_label = Label(right_frame, text="Copyright")
        copy_label.grid(row=4, column=0, sticky=W)

        self.copy_input = Entry(right_frame, width=30)
        self.copy_input.grid(row=5, column=0, columnspan=4, sticky=W)

        #CCLI Number
        ccli_label = Label(right_frame, text="CCLI Song Number")
        ccli_label.grid(row=6, column=0, columnspan=2, sticky=W)

        self.ccli_input = Entry(right_frame, width=15)
        self.ccli_input.grid(row=7, column=0, columnspan=2, sticky=W)
        
        sep = Separator(right_frame, orient=HORIZONTAL)
        sep.grid(row=8, column=0, sticky='we', pady=15, columnspan=4)

        pres_label = Label(right_frame, text="Presentation")
        pres_label.grid(row=9, column=0, sticky=W)

        self.pres_input = Entry(right_frame, width=30)
        self.pres_input.grid(row=10, column=0, columnspan=4, sticky=W)

        #Capo information
        capo_frame = Frame(right_frame)
        capo_frame.grid(row=11, column=0, pady=(15,5), columnspan=4, sticky='we')

        capo_label = Label(capo_frame, text="Capo")
        capo_label.grid(row=0, column=0, sticky=E)

        self.capo_val = StringVar()

        self.capo_input = OptionMenu(capo_frame, self.capo_val, '', '', '1', '2', '3', '4', '5')
        self.capo_input.grid(row=0, column=1, sticky=W)  

        #True if capoed chords are to be displayed on the printed sheet; false otherwise
        capo_check_label = Label(capo_frame, text="Print Capo")
        capo_check_label.grid(row=0, column=2, padx=(40, 5), sticky=E)

        self.capo_check = BooleanVar()
        
        self.capo_check_input = Checkbutton(capo_frame, var = self.capo_check)
        self.capo_check_input.grid(row=0, column=3, sticky=W)
        self.capo_check.set(False)

        #The key signature
        key_label = Label(right_frame, text="Key")
        key_label.grid(row=13, column=0, sticky=W)

        self.key_input = Entry(right_frame, width=15)
        self.key_input.grid(row=14, column=0, columnspan=2, sticky=W)

    def create_menu(self):
        """Create the application menu
        """
        menu = Menu(self.master)
        self.master.config(menu=menu)

        self.menu = Menu(menu)
        self.menu.add_command(label="Open", command=self.populate_input)
        self.menu.add_command(label="Save", command=self.save, state="disabled")
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=exit)

        menu.add_cascade(label="File", menu=self.menu)

    def populate_input(self):
        """When invoked, the user selects a file to open and its contents are displayed
        """
        self.open_file_name = filedialog.askopenfilename(title = "Select file")

        def set_text(widget, pos, text):
            widget.delete(pos, END)
            widget.insert(pos, text)
            
        try:
            data = SongData(self.open_file_name)
            set_text(self.lyric_input, '1.0', data.lyrics)
            set_text(self.title_input, 0, data.title)
            set_text(self.author_input, 0, data.author)
            set_text(self.copy_input, 0, data.copyright)
            set_text(self.ccli_input, 0, data.ccli)
            set_text(self.pres_input, 0, data.presentation)
            
            self.capo_val.set(data.capo)
            self.capo_check.set(data.capo_print)

            set_text(self.key_input, 0, data.key)

            self.menu.entryconfig("Save", state="normal")
        except ElementTree.ParseError as e:
            messagebox.showerror(str(e))
                      
    def save(self):
        """Saves the updated song data to the opened file
        """
        if self.open_file_name:
            data = SongData(self.open_file_name)

            #OpenSong files must use Windows line endings
            if sys.platform.lower() == 'darwin' or 'linux' in sys.platform.lower():
                data.lyrics = self.lyric_input.get('1.0', END).replace('\n', '\r\n')
            else:
                data.lyrics = self.lyric_input.get('1.0', END)
            data.title = self.title_input.get()
            data.author = self.author_input.get()
            data.copyright = self.copy_input.get()
            data.ccli = self.ccli_input.get()
            data.presentation = self.pres_input.get()
            data.capo = self.capo_val.get()
            data.capo_print = self.capo_check.get()
            data.key = self.key_input.get()

            data.save()

root = Tk()

#size of the window
#root.geometry("1366x768")

app = Window(root)
root.mainloop() 

