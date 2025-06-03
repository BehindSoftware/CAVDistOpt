import xml.etree.ElementTree as ET

def case_1():
    tree = ET.parse("data/cross.routest.xml")
    root = tree.getroot()

    new_item = ET.SubElement(root, "vType")
    new_item.attrib["id"] = "test"
    new_item.attrib["jmIgnoreFoeProb"] = "1"
    new_item.attrib["jmIgnoreFoeSpeed"] = "300"
    new_item.attrib["jmTimegapMinor"] = "0"
    new_item.attrib["jmIgnoreJunctionFoeProb"] = "1"
    new_item.attrib["jmCrossingGap"] = "0"
    new_item.attrib["sigma"] = "1" #collision has been provided with this on the junction
    #new_item.attrib["tau"] = "0.1" #changed the collisions, it increased but not junction only on the way
    new_item.attrib["guiShape"] = "passenger/van"

#TO DO: why type is generated on the xml

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1001"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1004"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "102 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1007"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "104 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1002"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1005"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "102 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1008"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "104 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1003"
    new_item.attrib["depart"] = "504.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1006"
    new_item.attrib["depart"] = "505.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "102 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1009"
    new_item.attrib["depart"] = "505.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "104 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    tree.write("data/cross.routest.xml")
    pass
    
def case_1_twosec():
    tree = ET.parse("data/cross.routest.xml")
    root = tree.getroot()

    new_item = ET.SubElement(root, "vType")
    new_item.attrib["id"] = "test"
    new_item.attrib["jmIgnoreFoeProb"] = "1"
    new_item.attrib["jmIgnoreFoeSpeed"] = "300"
    new_item.attrib["jmTimegapMinor"] = "0"
    new_item.attrib["jmIgnoreJunctionFoeProb"] = "1"
    new_item.attrib["jmCrossingGap"] = "0"
    new_item.attrib["sigma"] = "1" #collision has been provided with this on the junction
    #new_item.attrib["tau"] = "0.1" #changed the collisions, it increased but not junction only on the way
    new_item.attrib["guiShape"] = "passenger/van"

#TO DO: why type is generated on the xml

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1001"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1004"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "102 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1007"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "104 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1002"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1005"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "102 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1008"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "104 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1003"
    new_item.attrib["depart"] = "504.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1006"
    new_item.attrib["depart"] = "505.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "102 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1009"
    new_item.attrib["depart"] = "505.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "104 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2001"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "109 6 1001 103 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2004"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "107 6 1001 103 2"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2007"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "108 6 1001 103 1"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2002"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "109 7"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2005"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "106 8"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2008"
    new_item.attrib["depart"] = "503.00"
    new_item.attrib["color"]="1,0,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "107 9"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2003"
    new_item.attrib["depart"] = "504.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "108 6 1001 103 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2006"
    new_item.attrib["depart"] = "505.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "108 9"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "2009"
    new_item.attrib["depart"] = "505.00"
    new_item.attrib["color"]="0,1,0"
    new_item.attrib["type"] = "test"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "107 6 1001 103 4"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    tree.write("data/cross.routest.xml")
    pass


def add_manual_vehicle():
    tree = ET.parse("data/cross.routest.xml")
    root = tree.getroot()

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1001"
    new_item.attrib["depart"] = "501.00"
    new_item.attrib["color"]="0,0,1"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3 1008 116 18 1018 131 33"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1002"
    new_item.attrib["depart"] = "521.00"
    new_item.attrib["color"]="1,0,0"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3 1008 116 18 1018 131 33"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1003"
    new_item.attrib["depart"] = "541.00"
    new_item.attrib["color"]="0,1,0"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3 1008 116 18 1018 131 33"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    new_item = ET.SubElement(root, "vehicle")
    new_item.attrib["id"] = "1004"
    new_item.attrib["depart"] = "561.00"
    new_item.attrib["color"]="255,255,255"
    sub_item = ET.SubElement(new_item, "route")
    sub_item.attrib["edges"] = "101 3 1008 116 18 1018 131 33"

    new_item.tail= "    \n    "
    sub_item.tail= "\n    "

    tree.write("data/cross.routest.xml")
    pass

def create_connections(intersection_ID, x_intersection_num, y_intersection_num):
    with open("data/cross.contest.xml", "w") as connections:
        print('<?xml version="1.0" encoding="iso-8859-1"?>', file=connections)
        print('<connections xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/connections_file.xsd">', file=connections)
        index = 100
        index_to = 1
        for node in range(intersection_ID):
            print('<connection from="{}" to="{}"/>'.format(index+1,index_to+1), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+1,index_to+2), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+1,index_to+3), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+2,index_to), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+2,index_to+2), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+2,index_to+3), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+3,index_to), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+3,index_to+1), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+3,index_to+3), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+4,index_to), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+4,index_to+1), file=connections)
            print('<connection from="{}" to="{}"/>'.format(index+4,index_to+2), file=connections)
            index+= 5
            index_to+= 5
        print('</connections>', file=connections)
    pass

def create_edges(intersection_ID, x_intersection_num, y_intersection_num):
    with open("data/cross.edgtest.xml", "w") as edges:
        print('<?xml version="1.0" encoding="UTF-8"?>', file=edges)
        print('<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">', file=edges)
        #TO DO: There is a problem for 1x1 
        for node in range(intersection_ID):
            #note:priority and speed has been removed in edges
            #Output from center
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+1,node*5,node*5+1,1), file=edges)
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+2,node*5,node*5+2,1), file=edges)
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+3,node*5,node*5+3,1), file=edges)
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+4,node*5,node*5+4,1), file=edges)
            #Input to center
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+101,node*5+1,node*5,1), file=edges)
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+102,node*5+2,node*5,1), file=edges)
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+103,node*5+3,node*5,1), file=edges)
            print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(node*5+104,node*5+4,node*5,1), file=edges)
        #Connection between edges (starts from 1001 and adds right then up if there is)
        cursor=0
        temp=1001
        for y_line in range(y_intersection_num): #-1 for starting from 0
            for x_line in range(x_intersection_num): #-1 for starting from 0 -> 0,1,2:3
                if(x_line!=(x_intersection_num-1)): #the last intersection of x line
                    print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(temp,(cursor*5)+2,(cursor*5)+9,1), file=edges)
                    temp+= 1
                    print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(temp,(cursor*5)+9,(cursor*5)+2,1), file=edges)
                    temp+= 1
                if(y_line!=0): #the first intersection of y line
                    print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(temp,(cursor*5)+1,(cursor*5)-(x_intersection_num*5)+3,1), file=edges)
                    temp+= 1
                    print('<edge id="{}" from="{}" to="{}" numLanes="{}"/>'.format(temp,(cursor*5)-(x_intersection_num*5)+3,(cursor*5)+1,1), file=edges)
                    temp+= 1
                cursor+= 1
        print('</edges>', file=edges)
    pass


def create_detectors(intersection_ID,detector_pos):
    with open("data/cross.dettest.xml", "w") as detectors:
        print('<additional>', file=detectors)
        detector_ID = 1
        lane_number = 100
        for node in range(1,intersection_ID*5+1):
            if(node%5!=0):
                #freq: The aggregation period the values the detector collects shall be summed up
                print('<inductionLoop id="{}" lane="{}_0" pos="{}" freq="1" length="490" file="../reports/cross.out" friendlyPos="x"/>'.format(detector_ID,lane_number+1,detector_pos), file=detectors)
                print('<inductionLoop id="{}" lane="{}_0" pos="{}" freq="1" length="490" file="../reports/cross.out" friendlyPos="x"/>'.format(detector_ID+4,(lane_number+1)%100,detector_pos), file=detectors)
                detector_ID+= 1
            else:
                detector_ID = detector_ID + 4
            lane_number+= 1
        print('</additional>', file=detectors)

def create_nodes(x_intersection_num,y_intersection_num, detector_pos, TL):
    with open("data/cross.nodtest.xml", "w") as nodes:
        print('<?xml version="1.0" encoding="UTF-8"?>', file=nodes)
        print('<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">', file=nodes)

        intersection_ID = 0
        for y_line in range(y_intersection_num):
            for x_line in range(x_intersection_num):
                if(TL==True):
                    print('<node id="{}" x="{}" y="{}" type="traffic_light"/>'.format(intersection_ID*5,x_line*1000,y_line*(-1000)), file=nodes) #not worked collision detection at type unregulated
                else:
                    print('<node id="{}" x="{}" y="{}" type="priority"/>'.format(intersection_ID*5,x_line*1000,y_line*(-1000)), file=nodes) #not worked collision detection at type unregulated
                print('<node id="{}" x="{}" y="{}" type="priority"/>'.format(intersection_ID*5+1,x_line*1000,500+y_line*(-1000)), file=nodes)
                print('<node id="{}" x="{}" y="{}" type="priority"/>'.format(intersection_ID*5+2,500+x_line*1000,y_line*(-1000)), file=nodes)
                print('<node id="{}" x="{}" y="{}" type="priority"/>'.format(intersection_ID*5+3,x_line*1000,-500+y_line*(-1000)), file=nodes)
                print('<node id="{}" x="{}" y="{}" type="priority"/>'.format(intersection_ID*5+4,-500+x_line*1000,y_line*(-1000)), file=nodes)
                intersection_ID+= 1
                #if(x_line!=0):
                    # Creating edges and edges between edges
                create_edges(intersection_ID, x_intersection_num, y_intersection_num)
                    #pass
        print('</nodes>', file=nodes)
    #Creating junctions/intersections
    create_connections(intersection_ID, x_intersection_num, y_intersection_num)
    create_detectors(intersection_ID,detector_pos)
    pass

def create_map(x_intersection_num, y_intersection_num, path_length, detector_pos, TL):
    create_nodes(x_intersection_num,y_intersection_num, detector_pos, TL)

    pass