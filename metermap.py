# Copyright (C) 2015  Ross Goodwin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can contact Ross Goodwin at ross.goodwin@gmail.com or address 
# physical correspondence and verbal abuse to:

# Ross Goodwin c/o ITP
# 721 Broadway
# 4th Floor
# New York, NY 10003

"""MeterMap

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

"""


from docopt import docopt
from progressbar import ProgressBar
import json
import re
import sys
import math
from collections import defaultdict
from random import choice as rc
from random import random as rnd
from random import randint as ri
from pattern.en import sentiment

cmuDict = json.load( open('cmu_dict.json', 'r') )

def mult_replace(s, repldict):
    for k in repldict:
        s = s.replace(k, repldict[k])
    return s

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def tokenize(s):
    slower = s.lower()
    return re.findall(r"\b[\w']+\b", slower)


def get_meter(tokens):
    def get_num(phon):
        if phon[-1] in ['0', '1']:
            return phon[-1]
        else:
            return False
    def get_word_nums(phons):
        word_meter = []
        for p in phons:
            foo = get_num(p)
            if foo:
                word_meter.append(foo)
            else:
                pass
        return ''.join(word_meter)
    try:
        phonsets = map(lambda x: cmuDict[x], tokens)
    except KeyError:
        phonsets = []
    meter = map(get_word_nums, phonsets)
    return ''.join(meter)
    

def line_fix(l):
    quote_repl = {'\"': ""}
    l = mult_replace(l, quote_repl)
    l = re.sub(r'\s+', ' ', l)
#     if l[-1] in [".", ";", ":", ",", "!", "?"]:
#         ch = rnd()
#         if ch < 0.5:
#             l = l[:-1]
    return l[0].upper() + l[1:]

def last_line_fix(fl):
    last_line = fl[-1]
    if last_line[-1] in [".", "!", "?"]:
        pass
    elif last_line[-1] in [";", ":", ","]:
        last_line = last_line[:-1] + "."
    else:
        last_line += "."
    return fl[:-1] + [last_line]


def meter_map(arg_dict):
    # Open corpus file
    fileObj = open(arg_dict['<corpus>'], 'r')
    fileText = fileObj.read()
    fileObj.close()

    # Replace single quotes + convert to ascii
    single_quote_repl = dict([(u"\u2019", u"\'"), (u"\u2018", u"\'")])
    fixedText = mult_replace(fileText.decode('utf-8'), single_quote_repl)
    asciiText = fixedText.encode('ascii', 'ignore')

    if arg_dict['--lines']:
        # Strip whitespace from lines, return non-empty lines
        sentences = filter(
            lambda x: x,
            map(lambda y: y.strip(), asciiText.split('\n'))
        )
    else:
        # Grep for sentences and clauses
        complete_sents = map(lambda x: x.strip(),
            filter(lambda x: re.match('\w+', x),
                   re.findall(r"[A-Za-z\-'\"\s,;:]+[.?!][\s'\"]", asciiText)))

        clauses = map(lambda x: x.strip(),
            filter(lambda x: re.match('\w+', x),
                   re.findall(r"[A-Za-z\-'\"\s]+[.?!,;:][\s'\"]", asciiText)))

        sentences = complete_sents + clauses

    # Tokenize sentences
    sentenceTokens = map(tokenize, sentences)

    # Get meter of each sentence
    sentenceMeters = map(get_meter, sentenceTokens)

    # Make meter dictionary
    meterDict = defaultdict(list)
    for i in range(len(sentenceMeters)):
        meterDict[sentenceMeters[i]].append(sentences[i])

    def process_poem(poem_filename):
        # open file, read and strip lines
        tgtFileObj = open(poem_filename, 'r')
        tgtFileLines = map(lambda l: l.strip(), tgtFileObj.readlines())
        tgtFileObj.close()

        # Replace single quotes + convert to ascii
        tgtFileLines = map(lambda x: mult_replace(x.decode('utf8'), single_quote_repl), tgtFileLines)
        asciiTgtLines = map(lambda x: x.encode('ascii', 'ignore'), tgtFileLines)

        # Tokenize lines
        tgtTokenLines = map(tokenize, asciiTgtLines)

        # Return meter for each line
        return map(get_meter, tgtTokenLines)

    # Get meter for each line in poem
    if arg_dict['--sonnet']:
        tgtMeters = ['0101010101' for _ in range(14)]
    else:
        tgtMeters = process_poem(arg_dict['<poem>'])

    def pick_sentiment(c, i, s):
        # Sonnet
        if arg_dict['--sonnet']:
            pos = i % len(c)
            return c[pos]

        # Rising sentiment
        elif arg_dict['--rise']:
            by_sent = sorted(c, key=lambda x: sentiment(x)[0])
            ix = int( scale(i, (0.0, float(s-1)), (0.0, float(len(by_sent)-1))) )
            return by_sent[ix]

        # Falling sentiment
        elif arg_dict['--fall']:
            by_sent = sorted(c, key=lambda x: sentiment(x)[0])
            ix = int( scale(i, (0.0, float(s-1)), (float(len(by_sent)-1), 0.0)) )
            return by_sent[ix]

        # Cycling sentiment
        elif arg_dict['--cycle'] is not None:
            cyclen = int(arg_dict['--cycle'])
            pos = i % cyclen
            by_sent = sorted(c, key=lambda x: sentiment(x)[0])

            # Negative to positive
            if arg_dict['--pos']:
                ix = int( scale(pos, (0.0, float(cyclen-1)), (0.0, float(len(by_sent)-1))) )
            # Positive to negative
            elif arg_dict['--neg']:
                ix = int( scale(pos, (0.0, float(cyclen-1)), (float(len(by_sent)-1), 0.0)) )
            # Back and forth
            elif arg_dict['--neu']:
                if pos <= (cyclen-1)/2.0:
                    ix = int( scale(pos, (0.0, float(cyclen-1)/2.0), (0.0, float(len(by_sent)-1))) )
                else:
                    ix = int( scale(pos, (float(cyclen-1)/2.0, float(cyclen-1)), (float(len(by_sent)-1), 0.0)) )
            else:
                raise Exception("--cycle requires choice of --pos, --neg, or --neu")

            return by_sent[ix]

        elif arg_dict['--maxlike']:
            r = rnd()
            total = sum(map(lambda x: abs(sentiment(x)[0]), c))
            x = r * total
            for cand in c:
                x -= abs(sentiment(cand)[0])
                if x <= 0:
                    return cand
            return rc(c)

        else:
            # Purely positive, negative, or neutral
            if arg_dict['--pos']:
                return max(c, key=lambda x: sentiment(x)[0])
            elif arg_dict['--neg']:
                return min(c, key=lambda x: sentiment(x)[0])
            elif arg_dict['--neu']:
                by_sent = sorted(c, key=lambda x: sentiment(x)[0])
                return by_sent[len(by_sent)/2]
            # If no options, random lines
            else:
                return rc(c)

    # Eliminate empty meters and those not in meterDict
    cand_lines = filter(lambda x: x and meterDict[x], tgtMeters)

    # Pick lines based on sentiment
    final_lines = map(
        lambda x: pick_sentiment(meterDict[x[1]], x[0], len(cand_lines)), 
        enumerate(cand_lines)
    )

    # Fix capitalization, punctuation,
    # ensure last line ends with period
    final_lines = map(line_fix, final_lines)
    final_lines = last_line_fix(final_lines)

    return final_lines


if __name__ == '__main__':
    # Process docopt args
    wargv = docopt(__doc__, version='MeterMap v0.1')

    # Meter map
    lines = meter_map(wargv)

    # Print or write to file
    if wargv["<outfile>"] == "print":
        print "\n".join(lines)
    else:
        with open(wargv["<outfile>"], 'w') as outfile:
            outfile.write("\n".join(lines))

