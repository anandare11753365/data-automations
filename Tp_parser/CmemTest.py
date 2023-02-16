
import xml.etree.ElementTree as ET

input_file = "C:/Users/anandare/OneDrive - Intel Corporation/Documents/sample.xml"
# input_file = "C:/Users/anandare/source/repos/applications.manufacturing.ate-test.torch.networking.wlw.class.wlw/Modules/SIO_SERDES/InputFiles/wlw_serdes_extlb_ro.xml"
mytree = ET.parse(input_file)
root = mytree.getroot()
# print(type(myroot))
def offset(ofst):
    if ofst == None:
        return 0
    else:
        return(int(ofst))
def _bits(bits):
    bits_split = bits.split("-")
    if len(bits_split) == 2:
        lsb,msb = int(bits_split[1]),int(bits_split[0])
    else:
        lsb,msb = int(bits),int(bits)
    return (msb,lsb)

def fromto(offset,msb,lsb):
    from_ = offset+lsb
    to_ = offset+msb
    return (from_,to_)
master_list = []
for set in root.findall("set"):
    set_name=set.get("name")
    for set_pin in set.findall("pin"):
        pin_name = set_pin.get("name")
        expected_bits = set_pin.get("expected_bits")
        for pin in set_pin.findall("field"):
            pin_field_type = pin.get('type')
            inputs = {input.get('name'): str(input.text) for input in pin.findall('input')}
            for struct in root.findall("structure"):
                struct_name = struct.get('name')
                if pin_field_type == struct_name:
                    # print("   %s"%pin_field_type)
                    for field in struct.findall('field'):
                        field_type = field.get('type')
                        field_name = field.get('name')
                        field_offset = offset(field.get('offset'))
                        inputs.update({input.get('name'): str(input.text) for input in field.findall('input')})
                        for struct1 in root.findall("structure"):
                            struct1_name = struct1.get('name')
                            struct1_type = struct1.get('type')
                            if struct1_name == field_type:
                                if struct1.find('actions/ituff'):
                                    delimiter = struct1.findall('actions/ituff')[0].get('InnerDelimiter')
                                    tname = struct1.findall('actions/ituff/tname')[0].text
                                    for inkey,inval in inputs.items():
                                        tname = tname.replace("{%s}"%inkey,inval)
                                    ituff_value = [str(item.text).split(":") for item in struct1.findall('actions/ituff/value')]
                                for field2 in struct1.findall('field'):
                                    field2_type = field2.get('type')
                                    field2_name = field2.get('name')
                                    field2_offset = offset(field2.get('offset'))
                                    inputs.update({input.get('name'): str(input.text) for input in field2.findall('input')})
                                    for struct2 in root.findall("structure"):
                                        struct2_name = struct2.get('name')
                                        struct2_type = struct2.get('type')
                                        if struct2_name == field2_type:
                                            if struct2.find('actions/ituff'):
                                                delimiter = struct2.findall('actions/ituff')[0].get('InnerDelimiter')
                                                tname = struct2.findall('actions/ituff/tname')[0].text
                                                for inkey,inval in inputs.items():
                                                    tname = tname.replace("{%s}"%inkey,inval)
                                                ituff_value = [str(item.text).split(":") for item in struct2.findall('actions/ituff/value')]
                                            for field3 in struct2.findall('field'):
                                                field3_type = field3.get('type')
                                                field3_name = field3.get('name')
                                                field3_offset = offset(field3.get('offset'))
                                                inputs.update({input.get('name'): str(input.text) for input in field3.findall('input')})
                                                for struct3 in root.findall("structure"):
                                                    struct3_name = struct3.get('name')
                                                    struct3_type = struct3.get('type')
                                                    if struct3_name == field3_type:
                                                        if struct3.find('actions/ituff'):
                                                            delimiter = struct3.findall('actions/ituff')[0].get('InnerDelimiter')
                                                            tname = struct3.findall('actions/ituff/tname')[0].text
                                                            for inkey,inval in inputs.items():
                                                                tname = tname.replace("{%s}"%inkey,inval)
                                                            ituff_value = [str(item.text).split(":") for item in struct3.findall('actions/ituff/value')]
                                                        if struct3_type == "token":
                                                            bits = struct3.findall("bits")[0].text
                                                            base = struct3.findall("base")[0].text
                                                            msb,lsb = _bits(bits)
                                                            sumOffset = field_offset+field2_offset+field3_offset

                                                            for reg in ituff_value:
                                                                key,register = reg[0],reg[1]
                                                                if field2_name == key and field3_name==register:
                                                                    for inkey,inval in inputs.items():
                                                                        register = register.replace("{%s}"%inkey,inval)
                                                                    master_list.append([set_name,pin_name,expected_bits,tname,register,fromto(sumOffset,msb,lsb)[0],fromto(sumOffset,msb,lsb)[1],sumOffset,bits,base])

def bit_list(from_,to_):
    return [x for x in range(from_,to_+1)]

def size(from_,to_):
    return to_-from_+1

master_hash={}
for item in master_list:
    set_name=item[0]
    pin_name=item[1]
    expected_bits=item[2]
    tname=item[3]
    register=item[4]
    from_=item[5]
    to_=item[6]
    sumOffset=item[7]
    bits=item[8]
    base=item[9]
    key = "%s_%s$%s"%(set_name,pin_name,expected_bits)
    if key in master_hash:
        if register in master_hash[key]:
            # master_hash[key][register]
            pass
        else:
            master_hash[key][register]={"pin_name":pin_name,"size":size(from_,to_),"offset":sumOffset,"from":from_,"to":to_,"base":base,"tname":tname,"PerBit":1}
    else:
        master_hash[key] = {register:{"pin_name":pin_name,"size":size(from_,to_),"offset":sumOffset,"from":from_,"to":to_,"base":base,"tname":tname,"PerBit":1}}

to_del=[]
for config,register_dict in master_hash.items():
    used_up_bits=[]
    expected_bits = int(config.split("$")[1])
    res, last = [[]], None
    for field,details in register_dict.items():
        from_,to_ = details["from"],details["to"]
        bit_lists = bit_list(from_,to_)
        # print(bit_lists)
        a = [i for i in bit_lists if i in used_up_bits]
        if len(a)>0:
            # print(field,a)
            to_del.append((config,field))
            # pass
        else:
            used_up_bits.extend(bit_lists)
    used_up_bits.sort()
    # print(used_up_bits)
    b = [i for i in range(expected_bits) if not(i in used_up_bits)]
    for x in b:
        if last is None or abs(last - x) <= 2:
            res[-1].append(x)
        else:
            res.append([x])
        last = x
    # print(used_up_bits)
    # print(res)
    for x,dums in enumerate(res):
        dummy_register = "Dummy_%s"%x
        if dummy_register in master_hash[key]:
            # master_hash[key][dummy_register]
            pass
        else:
            master_hash[key][dummy_register]={"pin_name":pin_name,"size":size(min(dums),max(dums)),"offset":min(dums),"from":min(dums),"to":max(dums),"base":"-","tname":"-","PerBit":0}

for item in to_del:
    del master_hash[item[0]][item[1]]

# master_hash = 

for config,register_dict in master_hash.items():
    register_list_sorted = sorted(register_dict, key=lambda x: (register_dict[x]['offset']))
    for field in register_list_sorted:
        details = register_dict[field]
        print(details["pin_name"],field,details["offset"],details["size"],details["tname"],details["PerBit"],details["base"])


        # print(field,bit_list(from_,to_))
# print(used_up_bits)
# print("###############################")

# for type_tag in myroot.findall('structure'):
#     value = type_tag.get('name')
#     print(value)
# print("###############################")
# for type_tag in myroot.findall('structure/field'):
#     value = type_tag.get('type')
#     print(value)