# Annotation extraction from mat file

## downloads Widerface data set

and put it like:



## Second extract infomations from mat file

```
python mat_extract.py > xywhXfile.txt
```
it will be look like:

ooxx/oxoxox.jpg
3 # number of faces in this picture
(x,y,w,h)
(x,y,w,h)
(x,y,w,h)
ooxx/oxoxoxox.jpg
...

## Finally , translate xywh to xml and renames JPGEs

```
python anno2xml.py
```
files will be saved in Wider2017 folder


# wh infomations

for the mean w,h for Wider face is :
(28.5,36.9)

wh k-means with k=4
          w         h
1  61.88674  80.28675
2 400.33972 529.26481
3  14.76915  18.80862
4 169.08034 225.56282