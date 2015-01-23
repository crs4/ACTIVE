from libxmp.files import XMPFiles

def extract(infile):
	""" 
	Extract the requested feature and returns a dictionary of extracted XMP metadata 

	:param infile: resource file path
	"""
	d = {}

	try:
	    xmpfile = XMPFiles(file_path = infile)
	    xmp = xmpfile.get_xmp()
	    
	    for x in xmp:            
		if x[-1]['IS_SCHEMA']:
		    d[x[0]] = []
		else:
		    d[x[0]].append(x[1:])
		    
	    xmpfile.close_file()
	    #xmpfile.terminate() Causa crash dei worker celery - worker exited prematurely with signal 11 - terminate chiude una libreria in uso da un altro task.
	except Exception as ex:
	    print(ex)
	return d

