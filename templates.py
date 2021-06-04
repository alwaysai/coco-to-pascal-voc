xml_template = \
"""<annotation>
<folder/>
<filename>{}</filename>
<source>
<database>Unknown</database>
<annotation>Unknown</annotation>
<image>Unknown</image>
</source>
<size>
<width>{}</width>
<height>{}</height>
<depth>3</depth>
</size>
<segmented>0</segmented>
{}</annotation>
"""

object_template = \
"""<object>
<name>{}</name>
<occluded>0</occluded>
<bndbox>
<xmin>{}</xmin>
<ymin>{}</ymin>
<xmax>{}</xmax>
<ymax>{}</ymax>
</bndbox>
</object>
"""