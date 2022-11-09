# pyF1TV (WIP)
Package to extract session/time data from F1TV data channel graphics.

## Installation
``` bash
pip install git+https://github.com/ulacioh/pyF1TV.git
```

## Usage
#### Qualy
``` python
from pyf1tv import DataChannelContext
from pyf1tv.season_2022 import QualyGraphics2022

import cv2

data_channel_ctx = DataChannelContext(QualyGraphics2022())
image = cv2.imread('qualy.png')
data = data_channel_ctx.get_data_from_image(image)
```

Output:

``` bash
{
    'gp_name': 'FORMULA 1 LENOVO BRITISH GRAND PRIX 2022',
    'session_type': 'qualy',
    'time_left': '2:43',
    'classification': [
        {'position': '1', 'name': 'VER', 'lap_time': '1:42.996', 'gap': 'LEADER', 'current': {'tyre': 'I', 'time': '1:17.935'}, 'sectors': ['32.102', '45.833', '']},
        {'position': '2', 'name': 'HAM', 'lap_time': '1:43.250', 'gap': '+0.254', 'current': {'tyre': 'I', 'time': '1:14.233'}, 'sectors': ['32.443', '41.790', '']},
        {'position': '3', 'name': 'RUS', 'lap_time': '1:43.896', 'gap': '+0.900', 'current': {'tyre': 'I', 'time': '3Z2.442'}, 'sectors': ['32.442', '', '']},
        {'position': '4', 'name': 'NOR', 'lap_time': '1:44.319', 'gap': '+1.323', 'current': {'tyre': 'I', 'time': '1:17.157'}, 'sectors': ['33.447', '43.710', '']},
        {'position': '5', 'name': 'PER', 'lap_time': '1:44.809', 'gap': '+1.813', 'current': {'tyre': 'I', 'time': '34.936'}, 'sectors': ['34.936', '', '']}, 
        {'position': '6', 'name': 'LEC', 'lap_time': '1:44.844', 'gap': '+1.848', 'current': {'tyre': 'I', 'time': '1:14.197'}, 'sectors': ['32.405', '41.792', '']},
        {'position': '7', 'name': 'ALO', 'lap_time': '1:45.088', 'gap': '+2.092', 'current': {'tyre': 'I', 'time': '32.417'}, 'sectors': ['32.417', '', '']},
        {'position': '8', 'name': 'SAI', 'lap_time': '1:45.264', 'gap': '+2.268', 'current': {'tyre': 'I', 'time': ''}, 'sectors': ['34.160', '42.055', '29.049']},
        {'position': '9', 'name': 'ZHO', 'lap_time': '1:46.293', 'gap': '+3.297', 'current': {'tyre': 'I', 'time': '33.447'}, 'sectors': ['33.447', '', '']},
        {'position': '10', 'name': 'LAT', 'lap_time': '2:24.425', 'gap': '+41.429', 'current': {'tyre': 'I', 'time': '1:27.985'}, 'sectors': ['38.591', '49.394', '']},
        ...
    ]
}
```

#### Race
``` python
from pyf1tv import DataChannelContext
from pyf1tv.season_2022 import RaceGraphics2022

import cv2

data_channel_ctx = DataChannelContext(RaceGraphics2022())
image = cv2.imread('race.png')
data = data_channel_ctx.get_data_from_image(image)
```

Output:

``` bash
{
    'gp_name': 'FORMULA 1 ROLEX GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2022',
    'session_type': 'race'
    'classification': [
        {'position': '1', 'name': 'VER', 'gap': 'LEADER', 'interval': '', 'last_lap': '1:19.309', 'sectors': ['25.648', '28.265', '']},
        {'position': '2', 'name': 'PER', 'gap': '+12.040', 'interval': '+12.040', 'last_lap': '1:19.436', 'sectors': ['25.415', '27.308', '']},
        {'position': '3', 'name': 'NOR', 'gap': '+22.882', 'interval': '+10.185', 'last_lap': '1:22.408', 'sectors': ['25.819', '', '']},
        {'position': '4', 'name': 'RUS', 'gap': '+28.951', 'interval': '+6.004', 'last_lap': '1:21.704', 'sectors': ['26.010', '', '']},
        {'position': '5', 'name': 'BOT', 'gap': '+30.563', 'interval': '+1.612', 'last_lap': '1:21.854', 'sectors': ['25.990', '', '']},
        {'position': '6', 'name': 'TSU', 'gap': '+50.472', 'interval': '+20.252', 'last_lap': '1:21.332', 'sectors': ['25.837', '28.227', '27.268']},
        {'position': '7', 'name': 'VET', 'gap': '+51.049', 'interval': '+0.577', 'last_lap': '1:21.527', 'sectors': ['26.115', '28.078', '27.334']},
        {'position': '8', 'name': 'MAG', 'gap': '+58.306', 'interval': '+7.668', 'last_lap': '1:21.464', 'sectors': ['26.103', '28.146', '27.215']},
        {'position': '9', 'name': 'LEC', 'gap': '+59.522', 'interval': '+1.216', 'last_lap': '1:34.673', 'sectors': ['', '', '']},
        {'position': '10', 'name': 'STR', 'gap': '+1:08.183', 'interval': '+10.143', 'last_lap': '1:22.251', 'sectors': ['26.264', '28.239', '']},
        ...
    ]
}
