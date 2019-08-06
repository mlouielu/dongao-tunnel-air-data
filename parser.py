# -*- coding: utf-8 -*-
import json
import os
import re
import sys
from collections import defaultdict


# sensor[date] {
#  targets: {
#   vals: [values],
#   maximum: value,
#   minimum: value,
#   average: value
#  }
# }
#

T_MAPS = {
    'CO': 'co',
    '能見度': 'visibility',
    'NO': 'no',
    'NO2': 'no2',
    '風速': 'wind',
    '溫度': 'temp'
}


def get_sensor():
    return {i:
            {'vals': [], 'maximum': -1, 'minimum': -1, 'average': -1}
            for i in T_MAPS.values()}


def read_target(f, target, sensor):
    # Skip unit
    f.readline()
    for _ in range(24):
        sensor[target]['vals'].append(float(f.readline()))
    sensor[target]['average'] = float(f.readline())
    sensor[target]['maximum'] = float(f.readline())
    sensor[target]['minimum'] = float(f.readline())


def is_sensor_name(line):
    return re.match('\d[SN]-\d', line)


def is_date(line):
    return re.match('^\d{4}\/\d*\/\d*', line)


def to_json(filename):
    sensors = defaultdict(lambda: defaultdict(dict))
    with open(filename) as f:
        sensor = None
        sensor_name = None
        date = None
        v = []

        # Skip first line
        f.readline()
        while True:
            line = f.readline().strip()
            if not line:
                break
            if line.startswith('備註'):
                continue

            # Get sensor target
            if line in T_MAPS:
                # Renew sensor
                target = T_MAPS[line]
                if target == 'co':
                    if sensor:
                        v.append((sensor_name, sensor))
                    sensor = get_sensor()

                # Read sensor data
                read_target(f, target, sensor)

            # Get sensor name
            if is_sensor_name(line):
                sensor_name = line

            # Get date
            if is_date(line):
                date = line

            # Page end
            if line.startswith('台9線'):
                v.append((sensor_name, sensor))
                for name, sensor in v:
                    if not name:
                        print('[-] WTF? Sensor without name!!!')
                    sensors[name][date] = sensor
                v = []
                sensor_name = None
                sensor = None
    return sensors


def main(filenames):
    for filename in filenames:
        with open(f'{os.path.splitext(filename)[0]}.json', 'w') as f:
            json.dump(to_json(filename), f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main(sys.argv[1:])
