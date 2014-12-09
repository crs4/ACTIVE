import os
import inspect
#from mx.DateTime.Parser import DateTimeFromString
from datetime import datetime
from datetime import datetime
from libxmp.files import XMPFiles
from libxmp.exceptions import XMPError
from libxmp.core import XMPMeta
from libxmp.consts import *
"""from jobprocessor.xmp.libxmp.files import XMPFiles
from jobprocessor.xmp.libxmp.exceptions import XMPError
from jobprocessor.xmp.libxmp.core import XMPMeta
from jobprocessor.xmp.libxmp.consts import *"""


def metadata_synch(component_id, component_path, changes):
	"""
	This method is used to embedd XMP metadata in a multimedia file.

	:param component_id: Identificativo del componente che si vuole considerare
	:type component_id: int
	:param component_path: Path assoluto del componente che si vuole considerare
	:type component_path: str
	:param changes: Dizionario con i metadati da applicare al file considerato
	:type changes: dict
	"""
	xmpfile = XMPFiles(file_path = component_path, open_forupdate = XMP_OPEN_FORUPDATE)
	xmp = xmpfile.get_xmp()

	if not xmp:
	    xmp = XMPMeta()

	for ns in changes.keys():
	    # first of all check if namespace str(i[0]) and property name str(i[1]) exist
	    prefix = None
	    try:
		prefix = xmp.get_prefix_for_namespace(str(ns))
	    except XMPError, err:
		print('Error in get_prefix_for namespace: %s' % str(ns))
	    if prefix == None:
		# prefix does not exist so it must be created 
		try:
		    print('%s %s' % (str(ns), str(changes[ns]['prefix'])))
		    res = xmp.register_namespace(str(ns), str(changes[ns]['prefix'])) # CHANGE ME
		except XMPError, err:
		    print('Error in register_namespace: %s' % err)
	    for i in changes[ns]['fields'].keys():
		try:
		    property_exists = xmp.does_property_exist(str(ns), str(i))
		except XMPError, err:
		    print('Error in does_property_exist: %s' % err)
		if changes[ns]['fields'][i]['is_array'] == 'not_array':
					try:
						if changes[ns]['fields'][i]['xpath'] != []: # so it is a structure 
							if property_exists == False:
								# if it is a structure and the property does not exist, 
								# it must be created, otherwise, it will not be set.
								res = xmp.set_property(str(ns), str(i),'',prop_value_is_struct = XMP_PROP_VALUE_IS_STRUCT) 
							for index, elem in enumerate(changes[ns]['fields'][i]['value']):
								cleaned_xpath = re.sub( r"\[.\]", "", str(changes[ns]['fields'][i]['xpath'][index])) 
								xmp.set_property( str(ns), cleaned_xpath, str(elem) )
						elif changes[ns]['fields'][i]['type'] == 'date': 
							#mydate = DateTimeFromString(changes[ns]['fields'][i]['value'][0])
							mydate = datetime.strptime(changes[ns]['fields'][i]['value'][0], "%Y-%m-%d %H:%M:%S")
							mydate1 = datetime(mydate.year, mydate.month, mydate.day, mydate.hour, mydate.minute, int(mydate.second))
							xmp.set_property_datetime( str(ns), str(i), mydate1)
						elif changes[ns]['fields'][i]['type'] == 'bool': 
							xmp.set_property_bool( str(ns), str(i), bool(changes[ns]['fields'][i]['value'][0]))
						elif changes[ns]['fields'][i]['type'] == 'int': 
							xmp.set_property_int( str(ns), str(i), int(changes[ns]['fields'][i]['value'][0]))
						elif changes[ns]['fields'][i]['type'] == 'float': 
							xmp.set_property_float( str(ns), str(i), float(changes[ns]['fields'][i]['value'][0]))
						elif changes[ns]['fields'][i]['type'] == 'long': 
							xmp.set_property_long( str(ns), str(i), long(changes[ns]['fields'][i]['value'][0]))
						else:
							#log.debug('%s %s %s' % (str(ns), str(i), str(changes[ns]['fields'][i]['value'][0])))
							xmp.set_property( str(ns), str(i), str(changes[ns]['fields'][i]['value'][0]))
							
					except XMPError as ex1:
						print('XMPError in set_property: %s' % ex1)
					
					except Exception as ex2:
						print('XMPError in set_property: %s' % ex2)
		else:
				
					try:
	 
						# Property IS ARRAY 
						if changes[ns]['fields'][i]['xpath'] != []: # so it is a structure 
							print('Sorry. Array of structures is not supported by xmplib')
							continue
						if property_exists == False:
							# if it is an array and the property does not exist, 
							# it must be created, otherwise, it will not be set.
							if changes[ns]['fields'][i]['is_array'] == 'alt' and  changes[ns]['fields'][i]['type'] == 'lang' :
								res = xmp.set_property(str(ns), str(i),'',prop_value_is_array = XMP_PROP_VALUE_IS_ARRAY,  
																			   prop_array_is_alt = XMP_PROP_ARRAY_IS_ALT,
																			   prop_array_is_alttext = XMP_PROP_ARRAY_IS_ALTTEXT,
																			   prop_array_is_ordered = XMP_PROP_ARRAY_IS_ORDERED)
							elif changes[ns]['fields'][i]['is_array'] == 'seq': #array type is seq
								res = xmp.set_property(str(ns), str(i),'',prop_value_is_array = XMP_PROP_VALUE_IS_ARRAY, 
																			   prop_array_is_ordered = XMP_PROP_ARRAY_IS_ORDERED)
							elif changes[ns]['fields'][i]['is_array'] == 'bag': #array type is bag
								res = xmp.set_property(str(ns), str(i),'',prop_value_is_array = XMP_PROP_VALUE_IS_ARRAY, 
																			   prop_array_is_unordered = XMP_PROP_ARRAY_IS_UNORDERED)
							else: 
								res = xmp.set_property(str(ns), str(i),'',prop_value_is_array = XMP_PROP_VALUE_IS_ARRAY) 
						if changes[ns]['fields'][i]['type'] == 'lang':
							for index,elem in enumerate(changes[ns]['fields'][i]['value']):
								qual_value =  str(changes[ns]['fields'][i]['qualifier'][index])
								general = qual_value[:2]
								append_res = xmp.set_localized_text( str(ns), str(i), general ,qual_value, elem.encode('utf-8'), )
						else:
							number_of_items = xmp.count_array_items( str(ns), str(i)) 
							item_list = []
							for idx in xrange(number_of_items):
								item_list.append(xmp.get_array_item( str(ns), str(i), idx + 1).keys()[0])
							for index,elem in enumerate(changes[ns]['fields'][i]['value']):
								# method does_array_item_exist seems to work as expected
								# so, it is NECESSARY to get all items already in array 
								# and to check new items with this list
								if elem.encode('utf-8') not in item_list:
									append_res = xmp.append_array_item( str(ns), str(i), elem.encode('utf-8'), {'prop_value_is_array':XMP_PROP_VALUE_IS_ARRAY})
									
					except XMPError as ex:
						print()

	if xmpfile.can_put_xmp(xmp):
	    try:
		xmpfile.put_xmp(xmp)
	    except XMPError, err:
		print('Error while writing xmp into file: %s' % err)

	xmpfile.close_file()

	return True

