# MeterMap

MeterMap maps clauses from a text corpus onto the metrical structure of a poem. 

The software works by parsing every clause and sentence in the input corpus for meter using [the CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict), parsing every line in the poem, and then finding clauses from the input corpus that match the meter of each line in the poem.

Using the [Pattern](http://www.clips.ua.ac.be/pages/pattern) library's sentiment analysis tool, clauses can be selected based on sentiment to create moody negative poems, uplifting positive ones, or anything in between. You can even cycle back and forth between positive and negative sentiment.

Rhyming tools are included as well, although that part of the software remains a work in progress. If you have ideas for improvements, please don't hesitate to [contact me](mailto:ross.goodwin@gmail.com).


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
	    [--rhyme=<scheme>]
	    [--spaced]
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

	  --cycle=<len>       Cycle from prevailing to opposite
	                      sentiment every <len> lines;
	                      requires --neg, --pos, or --neu

	  --rhyme=<scheme>    Attempt to make output poem rhyme;
	                      <scheme> can be set to auto or a
	                      scheme in the form ABABCDCD, etc.
	  
	  --spaced      Add spaces to front of some lines
	                in output, e.e. cummings style

	    sonnet      Value for <poem> that produces 14
	                lines in iambic pentameter

	    print       Value for <outfile> that prints to
	                terminal rather than writing to file

## Example Output

### William Faulkner + e.e. cummings

	           Outraged,
	           This time as 'too shocking.'
	    Paced by the turning outraged faces,
	     It's quite chilly this morning,
	      Wind-gnawed face and bleak,
	                I know I damn well hate you.
	               Destruction or grief or anguish:
	       For evil to come from evil.
	   The limp hard hand merely withdrew from his,
	 It was no more deadly; that was impossible.
	                                      Outraged,
	            As dull and uneventful as ever.
	                 Perhaps he knew no better anyway,
	                                   Outraged,
	     They were disappointed.
	             On the bowl of the cold cob pipe.
	             And then I saw that he was trembling,
	Muttered a shocking phrase.
	    We happen to know that the man is guilty.
	                Poor gentlemanly dull Johnny.
	              But he is afraid of living,
	                    Outraged,
	       She's frigid.
	         I wasn't even mad about that no more.
	Have sense enough to dive away from the propeller.
	         She's frigid.
	          And they was a little impatient with me.
	             It's that terrible Mr.
	Flashlights glared and winked along the base.

### David Foster Wallace + Dr. Seuss

	The mug has a hair-thin brown crack down one side,
	A skinny dog at his side, half in profile.
	According to Taylor's use of the word can,
	And his thoughts had drifted all over the place,
	Bent over and felt the wet grass with his hand.
	But I don't really know anything about it.
	I'm not sure whether they're called hoofs or feet on swine.
	Handcuffed to the corpse of his malevolent foe,
	Since for him it would be at worst somewhat dull.
	His legs look like he's about to wet himself.
	It seemed like it had to have been a bad sign,
	Often I was forced to avert my eyes from him,
	So fiercely as to incline us to say 'false.'
	According to Taylor's use of the word can,
	But I don't really know anything about it.
	The kind you have to convert and cook up yourself,
	Is identical to those worst dreams' form itself:
	Would refute fatalism with respect to the past,
	Or between false and self-contradictory ones,
	He spoke very little, just sat up with me.
	The bad ankle hasn't ached once this whole year.
	The mist of the pool's too-clean smell is in your eyes;
	This is awful news.'
	Instead of getting sick,
	Needs something to make himself dark, in the game.
	But that's not what I mean by driving the scene.
	Feminine past participle of dare,
	That either Q or Q must fail to occur.
	Would refute fatalism with respect to the past,
	Taylor has not engaged in linguistic reform.
	He kept asking them what they were afraid of.
	For just three weeks' rental of anything foreign.
	Though it's hard to figure out just what they're doing,
	And the burly guys manning the road's barricades.
	That either Q or Q must fail to occur.
	He'd mentioned the child-actor's name over and over.
	The sort of man who stands in one place all day.
	But born in the hated-by-you Ottawa,
	You are merely going with some cosmic flow.
	You are merely going with some cosmic flow.
	He talks on the phone at the office a lot.
	He spoke very little, just sat up with me.
	His police lock protruding into empty air,
	Mutton stuffed with foie gras, double chocolate rum cake.
	What matters, alas, is what this eros wrought.
	He kept asking them what they were afraid of.
	It seemed like it had to have been a bad sign,
	You just sit there and listen as hard as you can,
	I wouldn't want to go overboard with this thing,
	The whine of no real sleep for maybe five days,
	I could tell just by looking you weren't happy.
	Can we talk about it before you react?
	She's coming to Cleveland next Friday, it says.
	It's just before serious harvesting starts,
	Is there anything to say on this subject?
	Which at this age isn't that far behind them.'
	Though it's hard to figure out just what they're doing,
	You can tell it's spooky down here in the summer,
	The chasm he opened between her and I.
	You don't want her facial reaction described.
	He spoke very little, just sat up with me.
	And it rolls down the floor of the subway,
	The dead fields' total snow like a well-ironed sheet,
	The sense is ever so slightly sad.
	Because I allegedly have a disease?
	Because I allegedly have a disease?
	I don't really drink alcoholic stuff much,
	We've been at it maybe an hour and half,
	I go Fucking hang up on me why don't you,
	And apologized for interrupting his work,
	Hard dangerous spirals of brittle black hair.

### Charles Dickens + a sonnet

	The awful mountain-voices died away,
	The awful thinness of the fallen man,
	The perpetrator of the bloody smear,
	Before the Chicken's penetrating glance,
	And not in an exaggerated form,
	Adjusting it upon a dusty clock,
	And travelled slowly up a steep ascent.
	Without abatement of her awful stock,
	And draw the placid veil before her clear,
	In their unhealthy looks and feeble sight,
	And indicating nothing but the four,
	And keeps a wary eye upon the four.
	Behind protruding angles of the four,
	And with her secret weighing on her bright.