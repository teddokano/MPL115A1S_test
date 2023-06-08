from	machine		import	SPI, Pin
from	utime		import	sleep, localtime
from	struct		import	unpack
import	os

class MPL115A1:
	def __init__( self, spi, cs ):
		self.spi	= spi
		self.cs		= cs
		self._get_coeff()
		
	def pressure( self ):
		self._cs_ctrl( 0 )
		self.spi.write( bytearray( [ 0x24, 0x00 ] ) )	
		self._cs_ctrl( 1 )

		sleep( 0.003 )

		p_adc, t_adc	= self._pressure_temp()
		
		p_comp	= self.a0 + (self.b1 + self.c12 * t_adc) * p_adc + self.b2 * t_adc
	 
		return p_comp * ((115 - 50) / 1023) + 50

	def _get_coeff( self ):
		data	= self._insert_zero_bytes( [ 0x88, 0x8A, 0x8C, 0x8E, 0x90, 0x92, 0x94, 0x96 ] )

		self._cs_ctrl( 0 )
		self.spi.write_readinto( data, data )
		self._cs_ctrl( 1 )
		
		self.a0, self.b1, self.b2, self.c12	= unpack( ">hhhh", self._collect_odd_bytes( data ) )
		
		self.a0		/= 2**3
		self.b1		/= 2**13
		self.b2		/= 2**14
		self.c12	/= 2**24

	def _pressure_temp( self ):
		data	= self._insert_zero_bytes( [ 0x80, 0x82, 0x84, 0x86  ] )
		
		self._cs_ctrl( 0 )
		self.spi.write_readinto( data, data )
		self._cs_ctrl( 1 )

		p, t	= unpack( ">HH", self._collect_odd_bytes( data ) )
		p	>>= 6
		t	>>= 6
		
		return ( p, t )

	def _collect_odd_bytes( self, data ):
		#	doing similar to data = data[1::2] because MicroPython doesn't support "::2"
		return bytearray( [ x for i, x in enumerate( data ) if i % 2 ] )

	def _insert_zero_bytes( self, data ):
		return bytearray( sum( [ [x, 0x00] for x in data ], [] ) + [ 0x00 ] )

	def _cs_ctrl( self, state ):
		if self.cs:
			self.cs.value( state )


def main():
	DEPTH		= 1
	LOG_FILE	= "mpl155.csv"
	SPI_FREQ	= 1000000

	if "MIMXRT" in os.uname().machine:
		spi		= SPI( 0, SPI_FREQ, cs = 0 )
		sensor	= MPL115A1( spi, None )
		led		= None
		
	elif "Raspberry Pi Pico" in os.uname().machine:
		spi		= SPI( 1, SPI_FREQ, sck = Pin( 10 ), mosi = Pin( 11 ), miso = Pin( 12 ) )
		sensor	= MPL115A1( spi, Pin( 13, Pin.OUT ) )
		led		= Pin( "LED", Pin.OUT )

	count	= 0

	while True:
		p	= 0;
		
		for i in range( DEPTH ):
			p	+= sensor.pressure()
	
			if led:
				led.value( i >> 4 & 0x1 )

		dt	= localtime()
		p_str	= "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}, {}, {}".format( dt[ 0 ], dt[ 1 ], dt[ 2 ], dt[ 3 ], dt[ 4 ], dt[ 5 ], p / DEPTH * 10, count )
		print( p_str )

		with open( "data.csv", "a" ) as f:
			print( p_str, file = f )

		count	+= 1

if __name__ == "__main__":
	main()
