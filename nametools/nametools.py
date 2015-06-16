'''
Created on Jan 6, 2015

This library is used to handle the diverse, creative collection of field names used by scientists.

It also provides some functions that generate a dictionary of the correct names to use for any dataset. 

@author: DHawkins
'''

import csv

class NameException(Exception):
    pass

def make_name_dict(datafile):
    '''
    input file has format (e.g.)
    TORQUE, tq_dyno_nm
    TORQUE, trq_meas_nm
    TORQUE, Torque
    SPEED, spd_dyno_revs
    SPEED, dyno_shaft_rpm
    ...
    '''
    
    field_name_dict = {}
    try:
        with open(datafile, "r") as f:
            for row in csv.reader(f):
                field_name_dict.setdefault(row[0],[]).append(row[1])
        return field_name_dict
    
    except FileNotFoundError:
        raise FileNotFoundError('could not find {}'.format(datafile))    

def get_name_dict(file_headers, name_dict):
    '''
    @param file_headers: iter, all headers in file
    @param name_dict: path, to .csv file with name dict info
    @return: dict, {GENERIC_1: specific_1, GENERIC_2: specific_2}
    @raise NameException: If there are multiple matches for the same field
    
    With a full list of column names from your test file, 
    return a dictionary with the correct specific column header per generic
    
    a nice readable usage of this in application might be:

    >>> for my_data in lots_o_data:
    >>>     name_for = get_name_dict(my_data.headers)
    >>>     torq_vector = my_data[name_for['TORQUE']]
    >>>     spd_vector = my_data[name_for['SPEED']]
    >>>     pow_vector = calc_power(torq_vector, spd_vector)
        
    '''
    res = {}
    field_name_dict = make_name_dict(name_dict)
    for generic in field_name_dict.keys():
        
        match = []
        # do a case-insensitive search for the file field name in the field name dict
        for col in file_headers:
            if col.lower() in [i.lower() for i in field_name_dict[generic]]:
                match.append(col)
        
        if len(match) < 1:
            res[generic] = generic+'_not_found'
        elif len(match) > 1:
            raise NameException("Multiple possible matches for {}: {}".format(generic, list(match)))
        else:
            res[generic] = list(match)[0]
        
    return res

def get_name(generic, file_headers, name_dict):
    '''
    The one-off version of get_name_dict
    @param generic: str, the generic you are looking for
    @param file_headers: iter, all headers in the file 
    @return: str, the specific header in your file corresponding to the generic requested
    @raise NameException: if there are multiple matches for the same field
    '''
    field_name_dict = make_name_dict(name_dict)
    match = set(file_headers) & set(field_name_dict[generic])
    if len(match) < 1:
        return None
    elif len(match) > 1:
        raise NameException("Multiple possible matches for {}: {}".format(generic, list(match)))
    
    return list(match)[0]

if __name__ == "__main__":
    # TODO: bundle these into proper unit tests do0d!
    test_list = ['avg_iTestCA90_CADATDC', 'Inj1_2_Dur_ms', 'can_emsn_CO2_bsm_gkWh',
                 # if you uncomment this, error should be thrown for multiple
#                 'bsmCO2Exh_gkWh', 
                 'qmFuel_gsec']
    
    print(get_name_dict(test_list, r'../namedictionary.csv'))
    print(get_name('CO2_BRAKE', test_list, r'../namedictionary.csv'))