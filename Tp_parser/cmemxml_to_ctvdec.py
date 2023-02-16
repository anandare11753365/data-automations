import mtpl_parser
import tkinter as tk 
import os
import threading
import testing
import sys
# import subprocess as sub
# p = sub.Popen('./script',stdout=sub.PIPE,stderr=sub.PIPE)
# output, errors = p.communicate()
root = tk.Tk()         

def run_conv():
    # logger = testing.PrintLogger(log_widget)
    # sys.stdout = logger
    # sys.stderr = logger
    xmlpath = textbox.get()
    mp = mtpl_parser.MtplParser()
    label_1.config(text="Running",font=("Arial",16),fg="Orange") 
    if xmlpath.endswith('.xml') and os.path.isfile(xmlpath):
        mp.cmem_to_ctvdecoder(mtpl_path=xmlpath)
        # Console.insert(tk.INSERT, 'Done ')
        label_1.config(text="Done",font=("Arial",16),fg="Green")   
    else:
        label_1.config(text="Enter a valid Xml path",font=("Arial",16),fg="red")


root.geometry("700x400")

root.title("Cmem To Ctv Decoder Converter")

label = tk.Label(root, text="Input Cmem xml file", font=("Arial",20))
label.pack()
label = tk.Label(root, text=r"eg: C:\Users\anandare\Downloads\DDR_MM_CCC_2400.xml", font=("Arial",16))
label.pack(padx = 20,pady=5)


textbox = tk.Entry(root,font=("Arial",16))
textbox.pack(padx=10, pady=10)

button = tk.Button(root,text="Run", font=("Arial",18), command=threading.Thread(target=run_conv).start)
button.pack(pady=5)

label_1 = tk.Label(root, text="")
label_1.pack(pady=5)

# Console = tk.Text(root)
# Console.pack()

log_widget = tk.scrolledtext.ScrolledText(root, height=60, width=120, font=("consolas", "8", "normal"))
log_widget.pack()

# text.insert(tk.END, output)

root.mainloop()