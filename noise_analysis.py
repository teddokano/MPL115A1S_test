#!/usr/bin/env python3

# Sample of getting power spectrum from CSV file

import	matplotlib.pyplot as plt
import	numpy as np
import	math
from scipy import signal
from scipy.fft import rfft, rfftfreq

import	functools
print	= functools.partial( print, flush = True )

FILENAME	= "mpl115.csv"
FS			= 10			# sampling rate

WINDOW	= "blackmanharris"

COLOR_NS14	= { "color": [ 0, 0, 1 ], "alpha": 0.9, "label": FILENAME }
LOGPLOT		= 0

def main():

	###
	###	data preparation
	###
	s	= np.loadtxt( "mpl115.csv", delimiter = ",", usecols = [ 1 ] )
	s	= s / s.max()
	
	
	w	= signal.get_window( WINDOW, len( s ) )
	wc	= len( s ) / sum( w ) 
	
	###
	###	calcuration
	###
	
	ps0	= rfft( s * w )

	rfft_freq	= rfftfreq( len( s ), d = 1.0 / FS )
	
	ps0	= power_spectrum( ps0, wc )
	
	ps0	= [ 10 * np.log10( x ) for x in ps0 ]
	
	###
	###	plotting result
	###
	
	fig	= plt.figure(figsize=(12, 8))
	bx	= fig.add_subplot(111)
	
	bx.set_ylim( [ -140, 0 ] )
	
	print( "plotting.. ", end = "" )

	if LOGPLOT:
		bx.semilogx( rfft_freq,	ps0 , **COLOR_NS14 )	
		bx.set_xlim( [0.001, FS / 2.0] )
	else:
		bx.plot( rfft_freq, ps0, **COLOR_NS14 )

	bx.legend( loc='upper right',  borderaxespad=1, fontsize=9 )

	bx.set_xlabel( "frequency [Hz]" )
	bx.set_ylabel( "power [dBFS]  (Full scale: max pressure value)" )

	bx.grid()

	print( "done" )
	
	print( "saving file.. ", end = "" )	
	plt.savefig( FILENAME + ".png", dpi=72 )
	print( "done" )
	print( "** close plot window to terminate execution **" )

	plt.show()

def power_spectrum( dat, wndw ):
	dat		= np.abs( dat ) ** 2
	dat	   /= ( len( dat ) ** 2 )
	dat    *= wndw
	dat[ 1 : -1 ]	*= 2
	
	return dat
	

if __name__ == "__main__":
	main()

