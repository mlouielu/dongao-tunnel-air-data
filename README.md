Taiwan Dong'ao Tunnel (東澳隧道) Air Sensor Data Parser
=======================================================

data from: [蘇花公路山區路段改善空氣品質資料](https://thbu4.thb.gov.tw/modules/download/download_list?node=0344d360-96db-4119-8a89-27999a873f65&c=90abcc04-3253-4961-9ebe-f64c12e92aa4)


HOWTO
=====

```shell
$ find data -name "*.pdf" -exec pdftotext -r 150 {} \;
$ sed -i '/^$/d' data/*.txt
$ python parser.py data/*.txt
```

STRUCT
======

```
{
  sensor_name(str): dict, {
    date(str): dict, {
	  targets(str): dict {
	    vals(str): [list: float],
		average(str): float,
		maximum(str): float,
		minimum(str): float
      }
    }
  }
}

sensor_names = ['2N-1', '2N-2', '2N-4', '2N-6', '2N-8', '2N-9', '2S-1', '2S-2', '2S-4', '2S-6', '2S-8', '2S-9']
targets = ['co', 'no', 'no2', 'visibility', 'wind', 'temp']
unit = ['ppm', 'ppm', 'ppm', '1/M', 'M/sec', 'Celsius']
```
