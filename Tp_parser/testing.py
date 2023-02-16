import sys
from tkinter import Tk, Button, Frame, Label, Entry
from tkinter.scrolledtext import ScrolledText
import mtpl_parser
import threading

class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class MainGUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.root = Frame(self)
        self.root.pack()
        self.label = Label(self.root, text="Input Cmem xml file", font=("Arial",20))
        self.label.pack()
        self.label = Label(self.root, text=r"eg: C:\Users\anandare\Downloads\DDR_MM_CCC_2400.xml", font=("Arial",16))
        self.label.pack(padx = 20,pady=5)
        self.textbox = Entry(self.root,width=80,font=("Arial",10))
        self.textbox.pack(padx=0, pady=5)
        self.test_button = Button(self.root, text="Run", command=threading.Thread(target=self.test_print).start)
        self.test_button.pack(padx=5, pady=5)
        self.test_button.pack()
        self.log_widget = ScrolledText(self.root, height=10, width=120, font=("consolas", "8", "normal"))
        self.log_widget.pack(padx=15, pady=10)
        self.log_widget.pack()

    def reset_logging(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_print(self):
        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger
        # xmlpath = "I:/hdmxprogs/icd/ICDXXXXUXH33C10S050/TPL/Modules/SIO_RMN_X/InputFiles/rmnx_10g_bitprog_extlb_perlane_cmb_merge_cmem.xml"
        xmlpath = self.textbox.get()
        mp = mtpl_parser.MtplParser()
        mp.cmem_to_ctvdecoder(mtpl_path=xmlpath)




if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()