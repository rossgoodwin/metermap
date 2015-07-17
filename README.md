# MeterMap

Maps clauses from a text corpus onto the metrical structure of a poem

## License

Copyright (C) 2015  Ross Goodwin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

You can contact Ross Goodwin at ross.goodwin@gmail.com or address 
physical correspondence and verbal abuse to:

	Ross Goodwin c/o ITP
	721 Broadway
	4th Floor
	New York, NY 10003

## Usage

Example usage:

`python metermap.py dickens.txt the_wasteland.txt output.txt --neg --cycle=12`

	Usage:
	  metermap.py <corpus> <poem> <outfile> 
	    [--lines]
	    [--neg | --pos | --neu]
	    [--rise | --fall | --maxlike | --cycle=<len>]
	  metermap.py --sonnet <corpus> <outfile>
	  metermap.py (-h | --help)
	  metermap.py --version

	Options:
	  -h --help     Show this screen.
	  --version     Show version.
	  --lines       Corpus separated by linebreaks
	  --neg         Negative sentiment prevails
	  --pos         Positive sentiment prevails
	  --neu         Neutral sentiment prevails
	  --rise        Rise from negative to positive
	  --fall        Fall from positive to negative
	  --maxlike     Maxium likelihood sentiment variance
	  --cycle=<len> Cycle from prevailing to opposite
	                sentiment every <len> lines;
	                requires --neg, --pos, or --neu

