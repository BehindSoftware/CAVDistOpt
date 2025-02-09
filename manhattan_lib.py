import os


def network_file_creation(x,y,road_length):
    print("netgenerate")
    os.system("netgenerate --grid --grid.x-number={} --grid.y-number={} --grid.x-length={} --grid.y-length={} -o data/cross.nettest.xml".format(x,y,road_length,road_length))

def detector_file_creation():
    os.system("python3 /usr/share/sumo/tools/output/generateTLSE1Detectors.py -n data/cross.nettest.xml -o data/detectors.add.xml")

#network_file_creation(1,2,500)
detector_file_creation()