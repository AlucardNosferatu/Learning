import glob

s1="""    <object>
        <name>{0}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{1}</xmin>
            <ymin>{2}</ymin>
            <xmax>{3}</xmax>
            <ymax>{4}</ymax>
        </bndbox>
    </object>"""

s2="""<annotation>
    <folder>VOC2007</folder>
    <filename>{0}</filename>
    <source>
        <database>My Database</database>
        <annotation>VOC2007</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>J</name>
    </owner>
    <size>
        <width>256</width>
        <height>256</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>{1}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{2}</xmin>
            <ymin>{3}</ymin>
            <xmax>{4}</xmax>
            <ymax>{5}</ymax>
        </bndbox>
    </object>{6}
</annotation>
"""

textlist=glob.glob('labels\\001\*.txt')

for text_ in textlist:
    flabel = open(text_, 'r')
    lb = flabel.readlines()
    flabel.close()
    ob2 = ""
    if len(lb)<2:
        continue  # no annotation
    x1=2
    x2=lb[1].split(' ')
    x3 = [int(float(i) * 256) for i in x2]
    if len(lb)>2:  # extra annotation
        for i in range(2,len(lb)):
            y2 = lb[i].split(' ')
            y3 = [int(float(i) * 256) for i in y2]
            ob2+='\n' + s1.format(x1,y3[0],y3[1],y3[2],y3[3])
    imgname=('%06d' % (int(text_[13:-4])))+'.jpg'
    savename='Annotations\\'+str('%06d' % (int(text_[13:-4])))+'.xml'
    f = open(savename, 'w')
    ob1=s2.format(imgname, x1, x3[0],x3[1],x3[2],x3[3],  ob2)
    f.write(ob1)
    f.close()
