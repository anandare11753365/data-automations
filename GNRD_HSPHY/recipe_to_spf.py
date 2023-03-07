
import zipfile
import re
import os
import tkinter as tk 

file_path = 'C:/Users/anandare/source/repos/data-automations/data-automations/GNRD_HSPHY/version_0x20102011.zip'
# zip file handler  

tap = "focus_tap stap_rmn0_nac_c1_r4"

def recipe_processor():
    file_path = textbox.get()
    tap = textbox2.get()
    zip = zipfile.ZipFile(file_path)
    spf_template = """

    label "WR_%sMEM_%s";
    set REG_ACC->req_valid = 'h1;
    set REG_ACC->rd1_wr0 = 'h0;
    set REG_ACC->addr = 'h%s;
    set REG_ACC->wr_data = 'h%s;
    flush;

    cycle 20;"""

    d = 0
    while os.path.exists(os.path.join(os.path.dirname(file_path),"hsphy_fdmem%s.spf"%d)):
        d += 1
    i = 0
    while os.path.exists(os.path.join(os.path.dirname(file_path),"hsphy_fdmem%s.spf"%i)):
        i += 1
    fd_out = os.path.join(os.path.dirname(file_path),"hsphy_fdmem%s.spf"%d)
    fd_out_wr = open(fd_out, 'w')
    fd_out_wr.write("focus_tap %s;\n"%tap)

    fi_out = os.path.join(os.path.dirname(file_path),"hsphy_fimem%s.spf"%i)
    fi_out_wr = open(fi_out, 'w')
    fi_out_wr.write("focus_tap %s;\n"%tap)

    recipe_raw_files = zip.namelist()

    for file in recipe_raw_files:
        # print(file)
        if file.endswith('fdmem'):
            fd = zip.open(file)
            fd_content = fd.readlines()
            fd_cnt=0
            for fd_lines in fd_content:
                fd_match = re.search("([0-9,a-f]*)\s.*?array.*?\((.*?)\)",fd_lines.decode('utf-8'))
                if fd_match:
                    data,addrs = fd_match.group(1),fd_match.group(2)
                    fd_template = spf_template%("FD",fd_cnt,addrs.lower().replace('0x',''),data)
                    # print(fd_template)
                    fd_out_wr.write(fd_template+'\n')
                    fd_cnt+=1
        elif file.endswith('fimem'):
            fi = zip.open(file)
            fi_content = fi.readlines()
            fi_cnt=0
            for fi_lines in fi_content:
                fi_match = re.search("([0-9,a-f]*)\s.*?array.*?\((.*?)\)",fi_lines.decode('utf-8'))
                if fi_match:
                    data,addrs = fi_match.group(1),fi_match.group(2)
                    fi_template = spf_template%("FI",fi_cnt,addrs.lower().replace('0x',''),data)
                    # print(fi_template)
                    fi_out_wr.write(fi_template+'\n')
                    fi_cnt+=1 
        else:
            pass

    fd_out_wr.close()
    fi_out_wr.close()
    my_label.config(text="Done generating\n%s\n%s"%(fd_out,fi_out),font=("Arial",16),fg="green")
    #     print(content)
root = tk.Tk()

root.geometry("700x400")

root.title("Hsphy Recipe To Spf")

label = tk.Label(root, text="Zip file path", font=("Arial",20))
label.pack()
label = tk.Label(root, text="eg: C:\\Users\\GNRD_HSPHY\\version_0x20102011.zip", font=("Arial",16))
label.pack(padx = 20,pady=5)

textbox = tk.Entry(root,font=("Arial",16))
textbox.pack(pady=10)

label2 = tk.Label(root, text="Input Tap name", font=("Arial",16))
label2.pack(padx = 20,pady=5)

textbox2 = tk.Entry(root,font=("Arial",16))
textbox2.pack(pady=10)

button = tk.Button(root,text="Run", font=("Arial",18), command=recipe_processor)
button.pack(pady=5)

my_label = tk.Label(root, text="")
my_label.pack(pady=5)


root.mainloop()