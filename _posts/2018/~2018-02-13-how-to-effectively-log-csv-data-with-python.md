---
title: "How to effectively log CSV data with Python"
date: "2018-02-13 14:37:15"
excerpt: "How can we leverage Python's built-in logging module to dump incoming data streams to a CSV file?"
header:
  teaser: assets/img/stock-photos/nick-hillier-339049.png
  overlay_image: assets/img/stock-photos/nick-hillier-339049.png
  overlay_filter: 0.1
classes: wide
categories:
- software
tags:
- python
- data
---

## CSV Format
Comma-separated values (CSV) data is one of the most basic and simple forms of plain-text data storage. Each line of the file is a data sample. Each sample consists of one or more fields, separated by commas. 

### Example Data


```python
import numpy as np

x = np.random.randint(low=0, high=10, size=(10,5))
np.savetxt('data.csv', x, delimiter=',', fmt='%g')
```


```python
!type data.csv
```

    5,7,0,2,0
    5,7,3,0,8
    8,1,7,8,6
    7,7,2,7,0
    4,0,9,8,5
    5,3,9,4,7
    1,8,1,2,5
    4,7,7,2,5
    8,6,2,5,9
    7,8,0,9,3
    

Quick. Easy. Simple.

However...

Data is rarely stored as a simple array. More often than not it's found as a structured object (i.e., an instance of a data class). One of my favourite structured data representations is `Protocol Buffers` (aka `protobuf`). Besides their cross-language compatibility, they easily decompose into JSON representations and Python `dict` objects. 

## Sample Data
In the context of my robotics research, I often have Python services handling data that I want to record and this data is often very well structured.


```python
from datetime import datetime

def generate_fake_robot_data():
    num_joints = 6
    data_sample = {
        'timestamp':datetime.now().strftime('%Y%m%d%H%M%S%f'),
        'joint_angles':np.deg2rad(np.random.randint(low=-180, high=180, size=(num_joints,))).tolist(),
        'joint_torques':np.random.randint(low=-180, high=180, size=(num_joints,)).tolist(),
        'status':'ok'
    }
    
    return data_sample
```


```python
print(generate_fake_robot_data())
```

    {'timestamp': '20180213155503255017', 'joint_angles': [1.4835298641951802, 1.0821041362364843, 2.426007660272118, 2.4085543677521746, -1.1693705988362009, 0.3839724354387525], 'joint_torques': [80, 63, 12, -163, -13, 137], 'status': 'ok'}
    

Some may say "why not just dump the sample as a JSON file?". 


```python
import json

data_json = json.dumps(generate_fake_robot_data(), indent=4, sort_keys=True)
print(data_json)
```

    {
        "joint_angles": [
            -1.5533430342749532,
            1.3089969389957472,
            0.06981317007977318,
            -0.15707963267948966,
            -1.6406094968746698,
            -0.4886921905584123
        ],
        "joint_torques": [
            -59,
            -145,
            -99,
            -127,
            -17,
            131
        ],
        "status": "ok",
        "timestamp": "20180213155503277019"
    }
    

While JSON is a great format, there are some nice advantages to well structured, relational data, especially when analyzing time-series data. Would we want to record each data sample as a separate JSON file? What happens when we record at 1000Hz? 

Having a single CSV file per recording session keeps things organized.

## Python Logging
Python comes with an awesome built-in `logging` module that can be customized for all sorts of purposes. There are two parts to CSV data logging. First, we need to set up a file-based logging with the Python logger. Second, we need to convert our data to CSV format.

### 1) File Logging
[Setting up Python's logging is quite easy and well documented](https://docs.python.org/3/library/logging.html).


```python
import logging

logger_name = 'csv_logger'

# clear all logger handlers
# this avoids a jupyter bug
# where duplicate logs may show
logging.getLogger(logger_name).handlers = []

# get handler to logger
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# define logging format
# very simple, we just want the str message
formatter = logging.Formatter(fmt='%(message)s')

# define stdout handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# define file handler
# i like to have unique filenames per recording session
# e.g., timestamps
fname = datetime.now().strftime('%Y%m%d%H%M%S')
file_handler = logging.FileHandler(filename=f'{fname}.csv')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```

### 2) Data Conversion
Since our logging formatter only takes a `str` as input, we need to convert our data from a `dict` to a structured CSV `str`.


```python
from typing import Iterable

def dict_to_flat_dict(d):
    """
    Flatten a dict.
    
    Certain dict keys may have iterables (i.e., arrays).
    These values should be flatten and given unique keys.
    """
    # init result      
    flat_d = {}
    
    # iterate through input and flatten iterable values
    # watch out for str values!    
    for k,v in d.items():
        if isinstance(v, Iterable) and not isinstance(v,str):
            for i,e in enumerate(v):
                flat_d[f'{k}_{i}'] = e
        else:
            flat_d[f'{k}'] = v
    
    return flat_d
```


```python
flat_data = dict_to_flat_dict(generate_fake_robot_data())
data_json = json.dumps(flat_data, indent=4, sort_keys=True)
print(data_json)
```

    {
        "joint_angles_0": -0.6457718232379019,
        "joint_angles_1": 2.7401669256310974,
        "joint_angles_2": 0.7330382858376184,
        "joint_angles_3": -0.5759586531581288,
        "joint_angles_4": 0.20943951023931956,
        "joint_angles_5": -2.775073510670984,
        "joint_torques_0": -118,
        "joint_torques_1": -121,
        "joint_torques_2": 72,
        "joint_torques_3": 147,
        "joint_torques_4": -132,
        "joint_torques_5": 60,
        "status": "ok",
        "timestamp": "20180213155503409026"
    }
    

Ah ha! Our data is now well structured and ready for CSV! 

Now just to convert it to a `str`:


```python
def flat_dict_to_csv(flat_d):
    return ','.join([str(v) for v in flat_d.values()])
```


```python
csv_data = flat_dict_to_csv(flat_data)
print(csv_data)
```

    20180213155503409026,-0.6457718232379019,2.7401669256310974,0.7330382858376184,-0.5759586531581288,0.20943951023931956,-2.775073510670984,-118,-121,72,147,-132,60,ok
    

And there we have it! 

Let's make a quick utility function that combines the above steps:


```python
def dict_to_csv(d):
    return flat_dict_to_csv(dict_to_flat_dict(d))
```

### Let's Log!


```python
for _ in range(10):
    logger.debug(dict_to_csv(generate_fake_robot_data()))
```

    20180213155503573034,0.9424777960769379,1.361356816555577,0.0,2.827433388230814,-2.234021442552742,-0.5235987755982988,-23,-171,77,-139,40,-151,ok
    20180213155503576037,-1.5882496193148399,0.8377580409572782,-3.12413936106985,1.361356816555577,2.2689280275926285,-2.234021442552742,-112,140,-115,-11,-47,20,ok
    20180213155503578036,-2.3911010752322315,-1.413716694115407,-2.129301687433082,-0.7155849933176751,-1.3089969389957472,0.9250245035569946,64,168,-179,162,14,-106,ok
    20180213155503580039,2.792526803190927,-2.4085543677521746,2.6878070480712677,-2.8797932657906435,-1.3962634015954636,2.443460952792061,99,-110,5,-165,40,168,ok
    20180213155503582035,2.722713633111154,0.2792526803190927,0.9250245035569946,3.12413936106985,-0.9599310885968813,1.8500490071139892,142,-126,7,162,149,85,ok
    20180213155503584037,-1.2217304763960306,1.0995574287564276,-0.5934119456780721,-1.6406094968746698,2.949606435870417,-1.4835298641951802,177,150,178,-60,-177,11,ok
    20180213155503586037,-2.8099800957108707,-0.9948376736367679,1.0995574287564276,-2.0943951023931953,-2.8099800957108707,-2.111848394913139,55,-51,40,-106,65,-108,ok
    20180213155503588038,0.47123889803846897,-0.20943951023931956,2.059488517353309,-1.2217304763960306,-2.6878070480712677,2.5830872929516078,-141,140,14,32,12,-128,ok
    20180213155503590035,0.9948376736367679,-0.017453292519943295,1.5707963267948966,1.2217304763960306,-0.8203047484373349,2.670353755551324,170,65,47,54,152,-32,ok
    20180213155503591038,0.4014257279586958,-1.361356816555577,2.2863813201125716,-2.076941809873252,-2.9321531433504737,2.2863813201125716,-90,-177,-172,-16,-153,157,ok
    
