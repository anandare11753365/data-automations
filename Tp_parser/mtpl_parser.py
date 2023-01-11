
import logger
import os
from typing import Union
import re
import xml.etree.ElementTree as ET
class MtplParser:
    def __init__(self,module_path,module_name : Union[str, list]=None):
        self.module_path = module_path
        self.module_name = module_name
        self.log = logger.Logger(__name__).get_logger()

    
    def _module_path(self):
        """
        Returns Module path when the MtplParser object is initialised with a TP path
        """
        if self.module_name == None:
            self.log.error("Make sure to insert a list of modules or a string of module")
            return ""
        else:
            path = os.path.join(self.module_path,self.module_name)
            if os.path.isdir(path):
                self.log.info("Module to parse: %s"%self.module_name)
                return path
            else:
                self.log.error("Module %s, does not exist in %s"%(self.module_name,self.module_path))
                return ""

        
           
    def mtpl_checker(self, module_name: str = ""):
        """
        Takes in module name, process or check if mtpls exist or multi mtpl(chooses 1) and returns the mtpl path
        """
        if module_name == "":
            module_path = self._module_path()

        mtpl_list = [os.path.join(module_path,f) for f in os.listdir(module_path) if f.endswith(".mtpl")]
        if len(mtpl_list) == 0:
            # no mtpl
            self.log.error("No \".mtpl\" file found under %s"%module_path)
        elif len(mtpl_list) > 1:
            self.log.warning("Many \".mtpl\": %s found under: %s\nSelecting Mtpl to be processed: %s"%(mtpl_list,module_path,mtpl_list[0]))
            return mtpl_list[0]
        else:
            self.log.info("Mtpl to be processed: %s"%mtpl_list[0])
            return mtpl_list[0]


    def mtpl_parser(self,section : str = 'Test', mtpl_path: list = None):
        """
        takes in mtpl paths, loop and apply functions:
        functions to process the sections based on user input:
        default section: Test
        """
        if mtpl_path == None:
            mtpl_path = self.mtpl_checker()
        # for mtpl_path in all_mtpl_list:
            # pass
        return self.mtpl_content(section, mtpl_path)

    def mtpl_content(self, section, mtpl_path: str = None):
        """
        takes in a single mtpl file and process the sections based on user input, default section: Test
        """
        mtpl_str = '\n'.join( [re.sub(r'#.*$', '', str(l.strip())) for l in open(mtpl_path,'r').readlines()] )
        if section == 'Counters':
            self.counter_parser(mtpl_str)
        elif section == 'Test':
            # print(self.test_parser(mtpl_str))
            return self.test_parser(mtpl_str)
        elif section == 'DUTFlow':
            pass
        else:
            pass
    
    def test_parser(self, mtpl_str: str):
        result = re.findall('Test\s.*?\{.*?\}',mtpl_str,re.DOTALL)
        test_dict ={}
        for raw_test in result:
            raw_test_list = raw_test.split('\n')
            raw_test_list.remove('{')
            raw_test_list.remove('}')
            test_name = raw_test_list[0].split(" ")[2]
            
            test_template = raw_test_list[0].split(" ")[1]
            test_params_values = raw_test_list[1:]
            test_p_v = [l.split("=") for l in test_params_values if '=' in l]
            # print(raw_test_list[0])
            # print(test_name)
            # test_name2 = raw_test_list[0].split(" ")[2]
            # print(test_name2)
            if not(test_name == ""):
                test_dict[test_name]={}
                test_dict[test_name]['test_template']=test_template
                # print(test_name)
                for pv in test_p_v:
                    param = pv[0]
                    value = self.process_value("=".join(pv[1:]))
                    # print('\t',param,value)
                    param = param.strip()
                    value = value.strip().strip('\"')
                    test_dict[test_name][param]=value
        return test_dict

    def counter_parser(self, mtpl_str: str):
        # print(mtpl_str)
        result = re.findall('Test\s.*?\{.*?\}',mtpl_str,flags=re.DOTALL)
        counter_dict ={}
        print(result)
        # for raw_counters in result:
            # raw_counters_list = raw_counters.split('\n')


    def process_value(self, value:str):
        if value[-1] == ';':
            value = value[:-1]
        if './Modules' in value:
            value = value.replace('./Modules',self.module_path)
        return value

    def rule_file_gen(self, mtpl_path:str = None, output_path:str=""):
        """
        Takes in a single mtpl_path and output path for rule file and generates csv rule files.
        """
        if mtpl_path == None:
            mtpl_dct = self.mtpl_parser(section='Test')
        else:
            mtpl_paths = [mtpl_path]
            mtpl_dct = self.mtpl_parser(section='Test', all_mtpl_list=mtpl_paths)

        if (os.path.isdir(output_path)):
            pass
        else:
            self.log.error('Output path \"%s\" does not exist, Setting \"C:\\temp\\rule_file\" as an output path'%output_path)
            temp_path='C:\\temp\\rule_file'
            isExist = os.path.exists(temp_path)
            if not isExist:
                os.makedirs(temp_path)
            else:
                output_path = temp_path
        cmem_rule_dict={}
        dc_rule_list=[]
        for test_name, param_hash in mtpl_dct.items():
            # print(test_name,param_hash['test_template'])
            # test_name = "%s::%s"%(os.path.splitext(base)[0])
            template = param_hash['test_template']
            if 'iCCmemDecodeTest' in template:
                # print(param_hash)
                # break_trigger = False
                config_file = param_hash['config_file']
                config_set = param_hash['config_set']
                if os.path.isfile(config_file) and config_file.endswith('.xml'):
                    print(config_file)
                    # break_trigger = True
                else:
                    self.log.error("Error on %s \nPath does not exist or not an xml file: %s"%(test_name,config_file))
                    continue

                # try:
                mytree = ET.parse(config_file)
                myroot = mytree.getroot()
                set_hash = {}
                struct_hash = {}
                # set_hash[struct_name]['fields'] = []
                testList=[]
                for root in myroot:
                    if (root.tag == "set") and (root.attrib['name'] == config_set):
                        set_hash[config_set] = {}
                        set_hash[config_set]['fields']=[]
                        for set_content in root:
                            
                            if set_content.tag == "pin":
                                for pin_content in set_content:
                                    # testList.append(pin_content.tag)
                                    if pin_content.tag == 'field':
                                        # print()
                                        field_type = pin_content.attrib['type']
                                        if 'name' in pin_content.attrib:
                                            field_name = pin_content.attrib['name']
                                        else:
                                            field_name = ""
                                        input_var = {}
                                        for field_content in pin_content:
                                            # testList.append(field_content.tag)
                                            if field_content.tag == 'input':
                                                input_var[field_content.attrib['name']] = field_content.text
                                                # pass
                                            else:
                                                self.log.warning("%s, %s, %s, %s tag is not processed or acknowleged"%(config_file,config_set,field_name, field_content.tag))
                                        set_hash[config_set]['fields'].append({'field_type':field_type,'field_name':field_name,'input_var':input_var})

                                    elif pin_content.tag == "token":
                                        
                                        for token_content in pin_content:
                                            if token_content.tag == "actions":
                                                for actionItem in token_content:
                                                    if actionItem.tag == "ituff":
                                                        for ituff_item in actionItem:
                                                            if ituff_item.tag == "tname":
                                                                if "usetestname" in ituff_item.attrib:
                                                                    if ituff_item.attrib['usetestname'] == "ALWAYS":
                                                                        tname_key = "%s_%s"%(test_name,ituff_item.text)
                                                                    else:
                                                                        tname_key = "%s"%(ituff_item.text)
                                                                        # print(tname_key)
                                                                cmem_rule_dict[str(ituff_item.text).replace(" ","").replace("\t","")]=[tname_key.upper()]
                                    else:
                                        self.log.warning("%s, %s, %s, %s tag is not processed or acknowleged"%(config_file,config_set,field_name, pin_content.tag))
                            else:
                                self.log.warning("%s, %s, %s, %s, %s tag is not processed or acknowleged"%(config_file,config_set,field_name, field_content.tag))
                    if root.tag == 'structure':
                        struct_name = root.attrib['name']
                        struct_hash[struct_name] = {} # each structure is a dict
                        if 'type' in root.attrib:
                            struct_type = root.attrib['type']
                        else:
                            self.log.warning("%s, %s, does not have structure: \"type\""%(config_file,struct_name))
                            struct_type = "group"
                        struct_hash[struct_name]['type'] = struct_type
                        struct_hash[struct_name]['fields'] = []
                        struct_hash[struct_name]['actions']={}
                        for struct_content in root:
                            # testList.append(struct_content.tag)
                            if struct_content.tag == "field":
                                field_type = struct_content.attrib['type']
                                if 'name' in struct_content.attrib:
                                    field_name = struct_content.attrib['name']
                                else:
                                    field_name = ""
                                input_var = {}
                                for field_content in struct_content:
                                    # testList.append(field_content.tag)
                                    if field_content.tag == 'input':
                                        input_var[field_content.attrib['name']] = field_content.text
                                        pass
                                    else:
                                        self.log.warning("%s, %s, %s, %s tag is not processed or acknowleged"%(config_file,struct_name,field_name, field_content.tag))
                                
                                struct_hash[struct_name]['fields'].append({'field_type':field_type,'field_name':field_name,'input_var':input_var})
                                # print(input_var)
                                # struct_hash[struct_name]['fields'].append({'name':field_name,'type':field_type})

                            elif struct_content.tag == "fail_port":
                                pass
                            elif struct_content.tag == "actions":
                                for actions_content in struct_content:
                                    if actions_content.tag == 'ituff':
                                        struct_hash[struct_name]['actions']['ituff'] = {}
                                        # pass
                                        if 'InnerDelimiter' in actions_content.attrib:
                                            delimiter = actions_content.attrib['InnerDelimiter']
                                        else:
                                            delimiter = '_'
                                            self.log.warning("%s, %s, %s Inner delimiter was not found in ituff attrib"%(config_file,struct_name, actions_content.tag))
                                        ituff_value_list =[]
                                        for ituff_content in actions_content:
                                            if ituff_content.tag == 'tname':
                                                if ('usetestname' in ituff_content.attrib) and (ituff_content.attrib['usetestname'] == 'ALWAYS'):
                                                    tname = "$tname$_%s"%(str(ituff_content.text).strip())
                                                else:
                                                    tname = "%s"%(str(ituff_content.text).strip())
                                                # print(tname)
                                            elif ituff_content.tag == 'result':
                                                pass
                                            elif ituff_content.tag == 'value':
                                                ituff_value_list.append(str(ituff_content.text).strip())
                                                pass
                                            else:
                                                pass
                                        struct_hash[struct_name]['actions']['ituff']['delimiter'] = delimiter
                                        struct_hash[struct_name]['actions']['ituff']['tname'] = tname
                                        struct_hash[struct_name]['actions']['ituff']['ituff_value_list'] = ituff_value_list
                                    else:
                                        self.log.warning("%s, %s, %s action content's tag is not processed or acknowleged"%(config_file,struct_name, actions_content.tag))
                                
                                # struct_hash[struct_name]['actions'][field_name] = field_type
                            elif struct_content.tag =="base":
                                pass
                            elif struct_content.tag =="bits":
                                pass
                            elif struct_content.tag == "limit_equal":
                                pass
                            else:
                                self.log.warning("%s, %s, %s tag is not processed or acknowleged"%(config_file,struct_name, struct_content.tag))
                input_var_full = {}
                for set_name,set_content in set_hash.items():
                    field_list = set_content['fields']
                    for field in field_list:
                        field_type = field['field_type']
                        field_name = field['field_name']
                        input_var = field['input_var']
                        input_var_full.update(input_var)
                        #####################################################
                        field_list_2 = struct_hash[field_type]['fields']
                        # action = self.action_processor(struct_hash,field_type)
                        # print(len(actions_2))
                        for field_2 in field_list_2:
                            field_type_2 = field_2['field_type']
                            field_name_2 = field_2['field_name']
                            input_var_2 = field_2['input_var']
                            input_var_full.update(input_var_2)
                            


                            #####################################################
                            field_list_3 = struct_hash[field_type_2]['fields']
                            for field_3 in field_list_3:
                                field_type_3 = field_3['field_type']
                                field_name_3 = field_3['field_name']
                                input_var_3 = field_3['input_var']
                                input_var_full.update(input_var_3)
                                #####################################################
                                field_list_4 = struct_hash[field_type_3]['fields']
                                for field_4 in field_list_4:
                                    field_type_4 = field_4['field_type']
                                    field_name_4 = field_4['field_name']
                                    input_var_4 = field_4['input_var'] 
                                    input_var_full.update(input_var_4)
                                    #####################################################
                                    field_list_5 = struct_hash[field_type_4]['fields']
                                    for field_5 in field_list_5:
                                        field_type_5 = field_5['field_type']
                                        field_name_5 = field_5['field_name']
                                        input_var_5 = field_5['input_var']
                                        input_var_full.update(input_var_5)
                                    # print(input_var_full)
                                        action = self.action_processor(struct_hash,field_type_5,input_var_full,test_name)
                                        delimiter = action[0]
                                        if not(delimiter == ""):
                                            tname = action[1]
                                            ituff_value_list = action[2]
                                            unique_ituff_head = "&%!".join(ituff_value_list)
                                            if unique_ituff_head in cmem_rule_dict:
                                                cmem_rule_dict[unique_ituff_head].append(tname)
                                            else:
                                                cmem_rule_dict[unique_ituff_head]=[tname]

                                    action = self.action_processor(struct_hash,field_type_4,input_var_full,test_name)
                                    delimiter = action[0]
                                    if not(delimiter == ""):
                                        tname = action[1]
                                        ituff_value_list = action[2]
                                        unique_ituff_head = "&%!".join(ituff_value_list)
                                        if unique_ituff_head in cmem_rule_dict:
                                            cmem_rule_dict[unique_ituff_head].append(tname)
                                        else:
                                            cmem_rule_dict[unique_ituff_head]=[tname]

                                action = self.action_processor(struct_hash,field_type_3,input_var_full,test_name)
                                delimiter = action[0]
                                if not(delimiter == ""):
                                    tname = action[1]
                                    ituff_value_list = action[2]
                                    unique_ituff_head = "&%!".join(ituff_value_list)
                                    if unique_ituff_head in cmem_rule_dict:
                                        cmem_rule_dict[unique_ituff_head].append(tname)
                                    else:
                                        cmem_rule_dict[unique_ituff_head]=[tname]
                            # print(input_var_full)
                            action = self.action_processor(struct_hash,field_type_2,input_var_full,test_name)
                            delimiter = action[0]
                            if not(delimiter == ""):
                                tname = action[1]
                                ituff_value_list = action[2]
                                unique_ituff_head = "&%!".join(ituff_value_list)
                                if unique_ituff_head in cmem_rule_dict:
                                    cmem_rule_dict[unique_ituff_head].append(tname)
                                else:
                                    cmem_rule_dict[unique_ituff_head]=[tname]

                        # print(input_var_full)
                        action = self.action_processor(struct_hash,field_type,input_var_full,test_name)
                        delimiter = action[0]
                        tname = action[1]
                        ituff_value_list = action[2]
                        unique_ituff_head = "&%!".join(ituff_value_list)
                        if unique_ituff_head in cmem_rule_dict:
                            cmem_rule_dict[unique_ituff_head].append(tname)
                        else:
                            cmem_rule_dict[unique_ituff_head]=[tname]
                        # print(tname)
            if 'iCAnalogMeasureTest' in template:
                config_file = param_hash['config_file']
                config_set = param_hash['config_set']
                if os.path.isfile(config_file) and config_file.endswith('.xml'):
                    print(config_file)
                    # break_trigger = True
                else:
                    self.log.error("Error on %s \nPath does not exist or not an xml file: %s"%(test_name,config_file))
                    continue
                mytree = ET.parse(config_file)
                set_hash={}
                myroot = mytree.getroot()
                for root in myroot:
                    if (root.tag == "ConfigList") and (root.attrib['name'] == config_set):

                        for config_list in root:
                            for config_item in config_list:
                                for cores_or_measurements_item in config_item:
                                    if cores_or_measurements_item.tag == 'Core':
                                        for core in cores_or_measurements_item:
                                            if core.tag == "iTuff":
                                                for ituff_content in core:
                                                    # print(ituff_content.tag)
                                                    if ituff_content.tag == "Token":
                                                        token_name = ituff_content.text
                                                    if ituff_content.tag == "UseInstName":
                                                        if ituff_content.text == "true":
                                                            tname_key = "%s_%s"%(test_name,token_name)
                                                        else:
                                                            tname_key = token_name
                                                        if tname_key in dc_rule_list:
                                                            pass
                                                        else:
                                                            dc_rule_list.append(tname_key)
            if 'iCDCLeakageTest' in template:
                config_file = param_hash['input_file']
                config_set = param_hash['config_set']
                if os.path.isfile(config_file) and config_file.endswith('.xml'):
                    print(config_file)
                    # break_trigger = True
                else:
                    self.log.error("Error on %s \nPath does not exist or not an xml file: %s"%(test_name,config_file))
                    continue
                dc_rule_list.append(test_name)               
        self.write_cmem_rule(output_path,cmem_rule_dict)
        self.write_dc_rule(output_path,dc_rule_list)

            # break

            # for name in namelist:
            #     print(name,headers_list)
    def write_cmem_rule(self,output,cmem_rule_dict):
        # rule_file_name = "rule_cmem"
        if len(cmem_rule_dict) == 0:
            self.log.info("No CMEM related is processed")
            return
        configHeader = "TOKEN_NAME,MODULE,IP,EDC_KILL,SUBFLOW,VOLTAGE_CORNER,TYPE,DATA_TYPE"
        rule_file_path1 = "%s\\rule_cmem_value_%s.csv"
        i1 = 0
        while os.path.exists(rule_file_path1%(output,i1)):
            i1 += 1
        f1 = open(rule_file_path1%(output,i1), 'w')
        f1.write("%s\n"%configHeader)
        temp_list = []
        for headers,namelist in cmem_rule_dict.items():
            if not("&%!" in headers):
                namelist_size_list = [len(x.split('_')) for x in namelist]

                for tname in namelist:
                    if self.test_instance_naming(tname):
                        name_split = tname.split("_")
                        name_split[3] = "(.*?)"
                        name_split[4] = "(.*?)"
                        name_split[7] = "(.*?)"
                        tokenName = "_".join(name_split)
                        tokenName = "%s::%s"%(self.module_name,tokenName)
                        stringToReturn = "%s,%s,%s,%s,%s,%s,VALUE,CUSTOM"%(tokenName,self.module_name,self.module_name.split("_")[0],"$1","$2","$3")
                    else:
                        tokenName = "%s::%s"%(self.module_name,tname)
                        stringToReturn = "%s,%s,%s,%s,%s,%s,VALUE,CUSTOM"%(tokenName,self.module_name,self.module_name.split("_")[0],"NA","NA","NA")
                    if stringToReturn in temp_list:
                        pass
                    else:
                        temp_list.append(stringToReturn)                   
                        f1.write("%s\n"%stringToReturn)
                
            else:
                headers_list=headers.split('&%!')
                headers_capture_list = ["%s:-100:100:dec"%x for x in range(len(headers_list))]
                namelist_size_list = [len(x.split('_')) for x in namelist]
                configHeader = "TOKEN_NAME,MODULE,IP,EDC_KILL,SUBFLOW,VOLTAGE_CORNER,TYPE,DELIMITER,DATA_TYPE,%s"%(",".join(headers_list))
                rule_file_path = "%s\\rule_cmem_%s.csv"
                i = 0
                while os.path.exists(rule_file_path%(output,i)):
                    i += 1
                f = open(rule_file_path%(output,i), 'w')
                f.write("%s\n"%configHeader)
                temp_list = []
                for tname in namelist:
                    if self.test_instance_naming(tname):
                        name_split = tname.split("_")
                        name_split[3] = "(.*?)"
                        name_split[4] = "(.*?)"
                        name_split[7] = "(.*?)"
                        tokenName = "_".join(name_split)
                        tokenName = "%s::%s"%(self.module_name,tokenName)
                        stringToReturn = "%s,%s,%s,%s,%s,%s,STATUS_READ,_,CUSTOM,%s"%(tokenName,self.module_name,self.module_name.split("_")[0],"$1","$2","$3",",".join(headers_capture_list))
                    else:
                        tokenName = "%s::%s"%(self.module_name,tname)
                        stringToReturn = "%s,%s,%s,%s,%s,%s,STATUS_READ,_,CUSTOM,%s"%(tokenName,self.module_name,self.module_name.split("_")[0],"NA","NA","NA",",".join(headers_capture_list))
                    if stringToReturn in temp_list:
                        pass
                    else:
                        temp_list.append(stringToReturn)                   
                        f.write("%s\n"%stringToReturn)
                f.close()
        f1.close()
    def write_dc_rule(self,output,dc_rule_list):
        # rule_file_name = "rule_cmem"
        if len(dc_rule_list) == 0:
            self.log.info("No Analog related is processed")
            return
        # for namelist in dc_rule_list:
        configHeader = "TOKEN_NAME,MODULE,IP,EDC_KILL,SUBFLOW,VOLTAGE_CORNER,TYPE,DELIMITER,DATA_TYPE"
        rule_file_path = "%s\\rule_dc_%s.csv"
        i = 0
        while os.path.exists(rule_file_path%(output,i)):
            i += 1
        f = open(rule_file_path%(output,i), 'w')
        f.write("%s\n"%configHeader)
        temp_list = []
        for tname in dc_rule_list:
            if self.test_instance_naming(tname):
                name_split = tname.split("_")
                name_split[3] = "(.*?)"
                name_split[4] = "(.*?)"
                name_split[7] = "(.*?)"
                tokenName = "_".join(name_split)
                tokenName = "%s::%s"%(self.module_name,tokenName)
                stringToReturn = "%s,%s,%s,%s,%s,%s,PIN_VALUE,_,CUSTOM"%(tokenName,self.module_name,self.module_name.split("_")[0],"$1","$2","$3")
            else:
                tokenName = "%s::%s"%(self.module_name,tname)
                stringToReturn = "%s,%s,%s,%s,%s,%s,PIN_VALUE,_,CUSTOM"%(tokenName,self.module_name,self.module_name.split("_")[0],"NA","NA","NA")
            if stringToReturn in temp_list:
                pass
            else:
                temp_list.append(stringToReturn)                   
                f.write("%s\n"%stringToReturn)
        f.close()

    def action_processor(self,struct_hash,field_type,input_var,test_name):
        
        action = struct_hash[field_type]['actions']
        if len(action)==0:
            return ["","",[]]
        else:
            ituff_content = action['ituff']
            delimiter = ituff_content['delimiter']
            tname = ituff_content['tname']
            tname = tname.replace("$tname$",test_name)
            # print(tname)
            for var,val in input_var.items():
                # print("\{%s\}"%var,val)
                tname = tname.replace("{%s}"%var,val)
            # print("fixed",tname)
            ituff_value_list = []
            for header in ituff_content['ituff_value_list']:
                for var,val in input_var.items():
                    header = header.replace("{%s}"%var,val)
                ituff_value_list.append(header)
            # print('before',ituff_value_list)
            if len(ituff_value_list) > 1:
                cntx=0
                smallest_element = min(ituff_value_list, key=len)
                for x in range(len(smallest_element)):
                    cnty=0
                    for y in range(len(ituff_value_list)):
                        if smallest_element[x] == ituff_value_list[y][x]:
                            cnty+=1
                    if cnty == len(ituff_value_list):
                        cntx+=1
                ituff_value_list = [x[cntx:] for x in ituff_value_list]
            # print('after',ituff_value_list)
            return [delimiter,tname.upper(),ituff_value_list]

    def test_instance_naming(self,tname: str):
        """Takes tname without module name in it and check for naming violation return true if no violation."""
        tname_split = tname.split('_')
        tname_field_count = len(tname_split)
        allowed_vc = ['MIN','NOM','MAX','VMIN','VNOM','VMAX']
        to_return = False
        if tname_field_count < 9:
            return False
        if tname_split[3] == 'E' or tname_split[3]=='K':
            to_return = True
        else:
            return False

        if tname_split[7] in allowed_vc:
            to_return = True
        else:
            return False

        return to_return  

if __name__ == "__main__":
    modulePath = "C:/Users/anandare/source/repos/applications.manufacturing.ate-test.torch.networking.wlw.class.wlw/Modules"
    mp = MtplParser(modulePath,'SIO_SERDES')
    mp.rule_file_gen(output_path="C:/temp/rule_file")
  
