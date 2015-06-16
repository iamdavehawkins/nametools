# nametools

For successfully handling similar data from multiple sources with different header information
 
#### Sample Use

```python
>>> from nametools import nametools as nt

>>> headers = ['trq_nm', 'spd_dyno_shaft_rpm', 'qm_fuel_rate']
    
>>> name_for = nt.get_name_dict(headers, r'./namedictionary.csv'))

>>> print(name_for['TORQUE'])
'trq_nm'
>>> print(name_for)
{'TORQUE': 'trq_nm',
 'SPEED' : 'spd_dyno_shaft_rpm',
 'FUEL_RATE' : 'qm_fuel_rate',
 'POWER' : 'POWER_not_found'
 }
```

#### Input Data Format (*.csv)
|||
|------|-------|
|TORQUE| trq_nm|
|TORQUE| trq_meas_nm|
|TORQUE| Torque|
|SPEED| spd_dyno_revs|
|SPEED| spd_dyno_shaft_rpm|
|FUEL_RATE| qm_fuel_rate|
|POWER| pow_pow_pow|
|...|...|...|
