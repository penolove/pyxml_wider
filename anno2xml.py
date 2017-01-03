
from lxml import etree
import sys
import cv2
import math
import glob
import os

cur_ind=0
outfileID=len(glob.glob("JPEGImages/*.jpg"))


def img2xml(path,objects,shape):
    root = etree.Element("annotation")
    folder = etree.SubElement(root, "folder")
    filename = etree.SubElement(root, "filename")
    source = etree.SubElement(root, "source")
    databases = etree.SubElement(source, "database")

    folder.text = "VOC2007"
    filename.text = str(path).zfill(6)
    databases.text = "FDDB"

    size = etree.SubElement(root, "size")
    width = etree.SubElement(size,"width")
    height = etree.SubElement(size,"height")
    depth = etree.SubElement(size,"depth")
    depth.text = str(shape[2])
    width.text = str(shape[1])
    height.text = str(shape[0])

    obj_count=0
    for obj in objects:
        #object
        obj=[float(i) for i in obj.split()]
        #the smallest circumscribed parallelogram
        #[link] https://github.com/nouiz/lisa_emotiw/blob/master/emotiw/common/datasets/faces/FDDB.py
        xmin_ = int(obj[0])
        ymin_ = int(obj[1])
        xmax_ = int(obj[0]+obj[2])
        ymax_ = int(obj[1]+obj[3])
        
        # check if out of box
        if(xmin_ >0 and ymin_>0 and xmax_<shape[1] and ymax_<shape[0]):
            obj_count+=1
            object_=etree.SubElement(root, "object")
            name=etree.SubElement(object_, "name")
            name.text="face"
            pose=etree.SubElement(object_, "pose")
            pose.text="Unspecified"
            truncated=etree.SubElement(object_, "truncated")
            truncated.text="0"
            difficult=etree.SubElement(object_, "difficult")
            difficult.text="0"
            # bndbox
            bndbox=etree.SubElement(object_, "bndbox")
            xmin=etree.SubElement(bndbox,"xmin")
            ymin=etree.SubElement(bndbox,"ymin")
            xmax=etree.SubElement(bndbox,"xmax")
            ymax=etree.SubElement(bndbox,"ymax")
            xmin.text = str(xmin_)
            ymin.text = str(ymin_)
            xmax.text = str(xmax_)
            ymax.text = str(ymax_)
    if obj_count>0:
        et = etree.ElementTree(root)
        et.write("Wider2017/Annotations/"+path+".xml", pretty_print=True)
        return True
    else: 
        return False




if __name__=="__main__":
    # you need to modify the path_img below
    # and the FDDB-fold-were assign by your own
    if len(sys.argv) < 2:
        file_path='xywhXfile.txt'
    elif len(sys.argv)==2:
        file_path=sys.argv[1]
    else:
        print "usage : python example.py [ellipseList]"
    current_file=open(file_path,'r')
    image_with_target=[i.replace('\n','') for i in current_file.readlines()]
    print len(image_with_target)
    while (cur_ind<len(image_with_target)):
        path_img = '../WIDER_train/images/'+image_with_target[cur_ind]+'.jpg'
        img = cv2.imread(path_img) 
        cur_ind+=1
        len_obj=int(image_with_target[cur_ind])
        cur_ind+=1
        objects=image_with_target[cur_ind:cur_ind+len_obj]
        cur_ind+=len_obj
        path=str(outfileID).zfill(6)
        if(img2xml(path,objects,img.shape)):
            cv2.imwrite("Wider2017/JPEGImages/"+path+".jpg", img)
            outfileID+=1

