"""
This module has been defined in order to create a simple function which could be
invoked during the execution of Job Manager tests.
It shouldn't be used for other purposes.
"""

from time import sleep

def identity(*args, **kwargs):
    """
    This function is used just for test purposes and
    it simply returns the input value.
    Moreover it is used to define the signature of a
    function that will be exeuted by a Job (wrapping).

    @param val: Unique parameter passed to the function
    @type val: Object
    @param args: A tuple of generic parameters passed to the function
    @type args: Tuple of objects
    @param kwargs: A dictionary of generic paramaters
    @type kwargs: Dictionary
    @return: The provided input parameter
    @rtype: Object
    """
    #print "Executing test on value", val
    sleep(0.3)
    return args[0]
