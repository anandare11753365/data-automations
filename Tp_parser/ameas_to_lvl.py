import mtpl_parser




import tkinter as tk 
import os
import shutil
import fileinput

root = tk.Tk()
def get_text():
    # my_label.config(text=textbox.get(1.0,tk.END))
    label_0.config(text="Select a module and click Run",font=("Arial",18))
    modulePath = textbox.get()
    modules = os.listdir(modulePath)
    for x in range(len(modules)):
      
        list.insert(tk.END, modules[x])
      
    # coloring alternative lines of listbox
        # list.itemconfig(x,
            #  bg = "blue" if x % 2 == 0 else "green")
             

def on_selection(event):
    # here you can get selected element
    # selected =  list.get('active')
    selected = list.get(list.curselection())

    # selected = list.get(tk.ACTIVE)
    label_1.config(text="Selected %s\nClick Run"%selected,font=("Arial",16),fg="green")


def run_conv():
    modulePath = textbox.get()
    module = list.get(list.curselection())
    mp = mtpl_parser.MtplParser(modulePath,module)
    mp.analog_measure_lvl_gen()
    label_1.config(text="Done generating levels and tcg",font=("Arial",16),fg="green")

root.geometry("700x700")

root.title("Ameas To Level Converter")

label = tk.Label(root, text="Input TP_Path/Modules", font=("Arial",20))
label.pack()
label = tk.Label(root, text="eg: C:/Users/anandare/WLWTP/Modules", font=("Arial",16))
label.pack(padx = 20,pady=5)

# textbox = tk.Text(root,height=1,font=("Arial",16))
# textbox.insert(tk.END,l)
# textbox.pack(padx=40, pady=10)

textbox = tk.Entry(root,font=("Arial",16))
# textbox.insert(tk.END,l)
textbox.pack(padx=10, pady=10)

button = tk.Button(root,text="Browse Modules", font=("Arial",18), command=get_text)
button.pack(pady=10)

label_0 = tk.Label(root, text="")
label_0.pack(pady=10)

list = tk.Listbox(root, selectmode = "single")
list.pack(padx=250, pady=5)
list.bind('<<ListboxSelect>>', on_selection)
list.pack(expand = True, fill = "both")

label_1 = tk.Label(root, text="")
label_1.pack(pady=5)

button = tk.Button(root,text="Run", font=("Arial",18), command=run_conv)
button.pack(pady=5)

# my_label = tk.Label(root, text="")
# my_label.pack(pady=5)


root.mainloop()