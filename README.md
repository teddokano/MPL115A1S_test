# MPL115A1S_test

This is a simple evaluation of a pressure sensor: MPL115A1.  
The output data from MPL115A1 has noise. I just wanted to see the noise spectrum.  

**Conclusion**:  
The noise is nothong but just a white noise ;)

# Code

## `MPL115A1S_measure.py`
`MPL115A1S_measure.py` is [MicroPython](https://micropython.org) code which runs on [MIMXRT1050-EVKB](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1050-evaluation-kit:MIMXRT1050-EVK) or [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/).  
It will measure the pressure continuously and output result on screen and file. Output file name will be `mpl115.csv`.  
The original code was published on [GitHub-Gist](https://gist.github.com/teddokano/e1baaa01c05db6e7c5076ab738cace3c).  

## `plot.g`
`plot.g` is a tiny [gnuplot](http://www.gnuplot.info) script to plot a timedomain waveform.  
This can be executed by command of `gnuplot plot.g`.  
Output will be a PNG file named `mpl115_timedomain.png`. 

## `noise_analysis.py`
`noise_analysis.py` is a Python3 script to plot a specrtum figure.  
It will read data from file:`mpl115.csv` and show/write spectrum on screen and a file:`mpl115.csv.png`

# Data

## `mpl115.csv`
`mpl115.csv` is a sample data which was captured by `MPL115A1S_measure.py` with Raspberry Pi Pico.  
The file is CSV format with date-time, air pressure and index number information in a row. 
```
2023-06-08 03:13:05, 1001.639, 0
2023-06-08 03:13:05, 1000.912, 1
2023-06-08 03:13:05, 1002.07, 2
2023-06-08 03:13:05, 1001.639, 3
2023-06-08 03:13:05, 1000.481, 4
...
```

## `mpl115_timedomain.png`
`mpl115_timedomain.png` is an output of `plot.g`.  
![mpl115_timedomain.png](https://github.com/teddokano/MPL115A1S_test/blob/main/mpl115_timedomain.png)

## `mpl115.csv.png`
`mpl115.csv.png` is an output of `noise_analysis.py`.  
![mpl115.csv.png](https://github.com/teddokano/MPL115A1S_test/blob/main/mpl115.csv.png)
