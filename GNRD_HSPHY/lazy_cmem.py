

import xml.etree.ElementTree as ET


open = \
"""	<structure name = "%s_%s" type = "group">
		<field type ="%s" name = "%s" >  </field>
		<actions>
		<ituff InnerDelimiter="_">
		<tname usetestname="ALWAYS">{PortName}_{Lane}_%s</tname>
		<result>strgval</result>"""

close= \
"""		</ituff>
		</actions>
	</structure>"""


lanes=["Q0","Q1","Q2","Q3","Q4","Q5","Q6","Q7"]

mytree = ET.parse("C:\\Users\\anandare\\OneDrive - Intel Corporation\\Documents\\DOCs\\GNRD\\HSPHY\\HSPHY_CMEM2.xml")
myroot = mytree.getroot()
config_set_list = ["PMA_BRINGUP_G1_6","PMA_BRINGUP_G2_6","PMA_BRINGUP_G3_6","PMA_BRINGUP_G4_6","PMA_BRINGUP_G5_6","PMA_BRINGUP_NTL","READ_NTL_RX_STATUS","READ_NTL_TX_STATUS"]

for config_set in config_set_list:
    for root in myroot:
        if (root.tag == "structure") and (root.attrib['name'] == config_set):
            for lane in lanes:
                print(open%(config_set,lane,config_set,config_set,config_set))
                for struct_content in root:
                    if struct_content.tag == "field":
                        # print(config_set)
                        # print(struct_content.attrib)
                        fname = struct_content.attrib['name']
                        if (lane in fname) or ("_CMN_" in fname):
                            print("		<value>%s:%s</value>"%(config_set,fname))
                print("%s\n"%close)

open2 = """	<structure name="%s" type="group">"""
close2="""	</structure>"""
# print()
portlanelist=["P0_OCT0","P0_OCT1","P1_OCT0","P1_OCT1","P2_OCT1","P2_OCT0"]
for config_set in config_set_list:
    print(open2%config_set)
    for port in portlanelist:
        for lane in lanes:
            field = """		<field type="%s_%s"	offset="0" ><input name="PortName">%s</input><input name="Lane">%s</input></field>"""%(config_set,lane,port,lane)
            print(field)
    print(close2)