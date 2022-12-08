
import os
import re
from tqdm import tqdm

# print(os.getlogin())

def counter_resolver():
    headtail= "-------------------------------------------------------------"

    tp_path = os.getcwd()
    # print(path)
    if os.path.isdir("%s\\%s"%(tp_path,"Modules")):
        modules_path = os.path.join(tp_path,"Modules")
        module_list = os.listdir(modules_path)
        # print(os.getlogin())

    else:
        print("%s\nHi %s,\n Make sure to run this program from same directory as /Modules eg below:--->>>\n  --->.\Counters Resolver.exe<---\n      .\Modules\n%s"%(headtail,os.getlogin(),headtail))
        k=input("press close to exit")
        return
    uniq_counter_dict = {}
    for module in module_list:
        module_path = os.path.join(modules_path,module)
        mtpl_file_path = os.path.join(module_path,"%s.mtpl"%module)
        
        if os.path.isfile(mtpl_file_path):
            # print(module)
            f = open(mtpl_file_path,'r')
            mtpl_lines = f.readlines()
            counter_open = False
            counter_open_curly = False
            counter_close_curly = False
            for line in mtpl_lines:

                counter_match = re.search(r'^Counters',line)

                if counter_open_curly:
                    counter_close_curly_match = re.search(r'^}',line)
                    if counter_close_curly_match:
                        # print("close")
                        counter_close_curly = True
                        counter_open_curly = False
                if counter_open:
                    counter_open_curly_match = re.search(r'^{',line)
                    if counter_open_curly_match:
                        # print("open")
                        counter_open_curly = True
                        counter_open = False
                if counter_match:
                    counter_open = True
                # print(line)
                if counter_open_curly and not(counter_close_curly):
                    # print(line)
                    counter_str_match = re.search("[np](\d{8}).*?$",line)
                    if counter_str_match:
                        counter_string = counter_str_match.group(0).replace(',','')
                        uniq_counter = counter_str_match.group(1)
                        counter_string = counter_string.replace('\t','').replace('\n','')
                        # print(module,uniq_counter,counter_string)
                        if uniq_counter in uniq_counter_dict:
                            uniq_counter_dict[uniq_counter].append((mtpl_file_path,counter_string))
                        else:
                            uniq_counter_dict[uniq_counter] = [(mtpl_file_path,counter_string)]
        
        else:
            print("unable to locate %s mtpl in %s"%("%s.mtpl"%module,mtpl_file_path))
        # break
        

    uniq_counter_list=list(uniq_counter_dict.keys())
    # print(uniq_counter_list)
    log_excel_list = []
    log_excel_list.append('module,counter_before,counter_after,change_status')
    mtpl_dict = {}
    for uniq_counter,content in tqdm(uniq_counter_dict.items()):
    # for uniq_counter,content in uniq_counter_dict.items():
        if len(content) > 1:
            log_excel_list.append('%s,%s,%s,remain'%(os.path.basename(content[0][0]),content[0][1],content[0][1]))
            for x in tqdm(range(len(content)-1),leave=False):
            # for x in range(len(content)-1):
                counter_string = content[x+1][1]
                mtpl_file_path = content[x+1][0]
                # mtpl_file_path_back_up = mtpl_file_path.replace(".mtpl","_backup.mtpl")
                # if os.path.isfile(mtpl_file_path_back_up):
                    # pass
                # else:
                    # shutil.copy(mtpl_file_path,mtpl_file_path_back_up)
                counter_str_match = re.search("[np](\d{4})(\d{4}).*?$",counter_string)
                counter_all = "%s%s"%(counter_str_match.group(1),counter_str_match.group(2))
                counter_lead = counter_str_match.group(1)
                counter = counter_str_match.group(2)
                # print(counter_all)
                while counter_all in uniq_counter_list:
                    counter_int = int(counter_all[-4:])
                    # print(counter_int)
                    if counter_int == 9999:
                        counter_int = 0
                    else:
                        counter_int +=1
                    counter_all = "%s%s"%(counter_lead,str(counter_int).zfill(4))
                    # uniq_counter_list.append(counter_all)
                    # print(counter_string,counter_all)
                counter_string_new = counter_string.replace(uniq_counter,counter_all)
                # print("old:%s\nnew:%s"%(counter_string,counter_string_new))
                log_excel_list.append('%s,%s,%s,changed'%(os.path.basename(mtpl_file_path),counter_string,counter_string_new))
                if mtpl_file_path in mtpl_dict:
                    mtpl_dict[mtpl_file_path].append((counter_string,counter_string_new))
                else:
                    mtpl_dict[mtpl_file_path] = [(counter_string,counter_string_new)]
                
                uniq_counter_list.append(counter_all)
                # break
                # uniq_counter_list.append(counter_all_new)
                # counter_string_new = counter_string.replace(counter_all,counter_all_new)
                # print(counter_string_new)
            # for item in content:
                # print(item[0],item[1])

    for file_path, content in mtpl_dict.items():
        # mtpl_file_path_back_up = file_path.replace('.mtpl','_backup.mtpl')
        file_path_fix = file_path.replace('.mtpl','_fix.mtpl')
        # os.remove(file_path)
        f = open(file_path,'r')
        f2 = open(file_path_fix,'w')
        lines = f.readlines()
        for line in lines:
            trig = True
            for fr in content:
                find,replace = fr[0],fr[1]
                if find in line:
                    f2.write(line.replace(find,replace))
                    trig = False
            if trig:
                f2.write(line)
        f2.close()
        f.close()
    flog = open(os.path.join(tp_path,"counter_logger.csv"),'w')

    for line in log_excel_list:
        flog.write("%s\n"%line)

    flog.close()

    if len(uniq_counter_list) == 0:
        k=input("%s\nHi %s,\n No duplicated counters found!!\n%s"%(headtail,os.getlogin(),headtail))
        return
    else:
        k=input("%s\nHi %s,\n Done resolving counters successfully!!\n Kindly check counter_logger.csv for more details:-->> \"%s\"\n%s"%(headtail,os.getlogin(),os.path.join(tp_path,"counter_logger.csv"),headtail))
        return


counter_resolver()