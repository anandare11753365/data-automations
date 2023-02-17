
import re
input = "C:/Users/anandare/source/repos/data-automations/data-automations/WLW_DDR/CLEAN_Unit208_SINGLEINIT_postprocess_14Feb23.txt"

file = open(input,'r')

lines = file.readlines()

def process_chs(decoder):
    decoderlist = re.split('\s+', decoder)
    # print(decoderlist[1])
    # print(decoderlist[2])
    pure_dec = decoderlist[3:]
    pure_dec = [o for o in pure_dec if "=" not in o]
    pure_dec = [o for o in pure_dec if "0x" not in o]
    # del pure_dec[1:2]
    return [decoderlist[1],decoderlist[2],pure_dec, len(pure_dec)]
concat_str=""
len_before=0
out_file_list = []
for x in range(len(lines)):
    match_tname = re.search("0_tname_(.*?$)", lines[x])

    if match_tname:
        tname = match_tname.group(1)
        values = lines[x+1]
        decoder = lines[x+2]
        if "xxxxxxx" in decoder:
            decoder = lines[x+3]
        else:
            item1 = process_chs(decoder)[0]
            item2 = process_chs(decoder)[1]
            pure_dec = process_chs(decoder)[2][:-1]
            pure_dec_len = process_chs(decoder)[3]
            print(pure_dec)
            concat_str += ",".join(pure_dec)+','
            concat_cap = ("%s,%s,%s,%s,%s,%s%s")%(tname,item1,item2,"_","CUSTOM",","*len_before,','.join(["%s:-100:100:dec"%(o) for o in range(pure_dec_len-1)]))
            # print(concat_cap)
            out_file_list.append(concat_cap)
            len_before = pure_dec_len+len_before-1
            # print("TOKEN_NAME,DELIMITER,DATA_TYPE")

file_out = open(input.replace(".txt",".csv"),'w')

file_out.write("TOKEN_NAME,ITEM1,ITEM2,DELIMITER,DATA_TYPE,%s\n"%concat_str)

for item in out_file_list:
    file_out.write("%s\n"%item)

file_out.close()
