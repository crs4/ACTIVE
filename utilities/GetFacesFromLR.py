#-----------------------------------------------------------------------
# Dato N immagini contenute in un folder <export_folder> costruisce
# un dizionario avente come chiavi i face tags e come valore la lista
# di file path delle immagini aventi tale tag nel metadato XMP:HierarchicalSubject
# 
# Questo codice e' dato a titolo di esempio.
#-----------------------------------------------------------------------

import sys
from os import listdir
from os.path import isfile, join
import exiftool
import string

mypath = "C:\\Active\\FaceModelsInput\\all\\"
category = 'FaceTags|'
offset = len(category)

files = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f))]
faces = {}

for f in files:
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(f)
	try:
		name = metadata[u'XMP:HierarchicalSubject'][offset:]
	except:
		name = '-'
		print '-'
		continue
	if string.find(name, '_') == -1:
		print name
	name = name.encode('ascii', 'ignore')
	name = string.split(name, '_')
	name = string.lstrip(string.lstrip(name[1]) + ' ' + name[0])
	if name not in faces:
		faces[name] = [f,]
	else:
		faces[name].append(f)

names = sorted(faces.keys())
for name in names:
	print name, ":", len(faces[name])


