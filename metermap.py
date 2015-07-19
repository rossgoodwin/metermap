# TODO
# [ ] Change last word of lines to make rhyme
#     Add --rhyme=<scheme> parameter
# [X] Change sonnet to poem parameter...
# [X] ...so that sonnets can rise or fall, etc.

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
    [--rhyme=<scheme>]
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

  --rhyme=<scheme>    Attempt to make output poem rhyme
                      <scheme> e.g. ABAB

    sonnet      Value for <poem> that produces 14
                lines in iambic pentameter

    print       Value for <outfile> that prints to
                terminal rather than writing to file

"""


from docopt import docopt
import json
import re
import sys
import math
from collections import defaultdict
import random
from random import choice as rc
from random import random as rnd
from random import randint as ri
from itertools import chain
from pattern.en import sentiment

# Init cmuDict
cmuDict = json.load( open('cmu_dict.json', 'r') )
# Init rhymeDict
rhymeDict = None

def flatten(listOfLists):
    "Flatten one level of nesting"
    return list(chain.from_iterable(listOfLists))

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

def get_num(phon):
    if phon[-1] in ['0', '1']:
        return phon[-1]
    else:
        return False

def get_word_meter(word):
    try:
        phons = cmuDict[word]
    except KeyError:
        phons = []
    return ''.join(filter(lambda x: x, map(get_num, phons)))

def get_meter(tokens):
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

def after_last_stressed_vowel(phons):
    vowel_phons = []
    for i in range(len(phons))[::-1]:
        if phons[i][-1] == '1':
            vowel_phons.append(i)
            return '_'.join(phons[i:])
        elif phons[i][-1] == '0':
            vowel_phons.append(i)
    if vowel_phons:
        ix = vowel_phons[0]
        return '_'.join(phons[ix:])
    else:
        return ''

def rhyme_finder(word):
    phons = cmuDict[word]
    rhyme_part = after_last_stressed_vowel(phons)
    candidates = rhymeDict[rhyme_part][:]
    
    def same_prior_phon(w):
        p = cmuDict[w]
        rhyme_phons = rhyme_part.split('_')
        tgtPhons = p[:-len(rhyme_phons)]
        if tgtPhons:
            tgtPhon = tgtPhons[-1]
        else:
            tgtPhon = []
        orgPhons = phons[:-len(rhyme_phons)]
        if orgPhons:
            orgPhon = orgPhons[-1]
        else:
            orgPhon = []        
        return tgtPhon != orgPhon
    
    candidates = filter(same_prior_phon, candidates)
    return candidates


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

    # Make meter dictionary and token dictionary
    meterDict = defaultdict(list)
    tokenDict = dict()
    for i in range(len(sentenceMeters)):
        meterDict[sentenceMeters[i]].append(sentences[i])
        tokenDict[sentences[i]] = sentenceTokens[i]

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
    if arg_dict['<poem>'] == 'sonnet':
        tgtMeters = ['0101010101' for _ in range(14)]
        tgtLines = meterDict['0101010101']
        tgtLinesBySent = sorted(tgtLines, key=lambda x: sentiment(x)[0])
    else:
        tgtMeters = process_poem(arg_dict['<poem>'])

    def pick_sentiment(c, i, s):
        # Sonnet
        if arg_dict['<poem>'] == 'sonnet':
            pos = i % len(c)
            
            # ADD CYCLE HERE
            if arg_dict['--cycle'] is not None:
                cyclen = int(arg_dict['--cycle'])
                pos = i % cyclen
                # Negative to positive
                if arg_dict['--pos']:
                    ix = int( scale(pos, (0.0, float(cyclen-1)), (0.0, float(len(tgtLinesBySent)-1))) )
                # Positive to negative
                elif arg_dict['--neg']:
                    ix = int( scale(pos, (0.0, float(cyclen-1)), (float(len(tgtLinesBySent)-1), 0.0)) )
                # Back and forth
                elif arg_dict['--neu']:
                    if pos <= (cyclen-1)/2.0:
                        ix = int( scale(pos, (0.0, float(cyclen-1)/2.0), (0.0, float(len(tgtLinesBySent)-1))) )
                    else:
                        ix = int( scale(pos, (float(cyclen-1)/2.0, float(cyclen-1)), (float(len(tgtLinesBySent)-1), 0.0)) )
                else:
                    raise Exception("--cycle requires choice of --pos, --neg, or --neu")

                return tgtLinesBySent[ix]


            elif arg_dict['--pos']:
                # CHANGE ALL TO REFLECT THIS....
                tgtLinesAdjust = tgtLinesBySent[-14:]
                return tgtLinesAdjust[pos]
            elif arg_dict['--neg']:
                tgtLinesAdjust = tgtLinesBySent[14::-1]
                return tgtLinesAdjust[pos]
            elif arg_dict['--rise']:
                tgtLinesAdjust = tgtLinesBySent[:14]
                return tgtLinesAdjust[pos]
            elif arg_dict['--fall']:
                tgtLinesAdjust = tgtLinesBySent[:-14:-1]
                return tgtLinesAdjust[pos]              

            else:
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


    def rhyme_map(ll):
        # In case global...
        lines = ll

        # Build Markov model
        all_tokens = flatten(sentenceTokens)
        nGramDict = defaultdict(list)
        for i in range(1, len(all_tokens)-1):
            nGramDict[(all_tokens[i-1], all_tokens[i])].append(all_tokens[i+1])

        # Get 2D list of tokens for each line
        tokens_lines = map(lambda x: tokenDict[x], lines)
        # Get original enders
        original_enders = map(lambda x: x[-1], tokens_lines)

        # Grab 2nd and 3rd to last words to feed into
        # Markov model
        seeds_lines = map(lambda x: tuple(x[-3:-1]), tokens_lines)
        # Get lists of possible line-ending words for each seed line
        line_enders = map(
            lambda i: filter(
                lambda y: (len(get_word_meter(y)) < 2 and \
                len(get_word_meter(original_enders[i])) < 2) or \
                get_word_meter(y) == get_word_meter(original_enders[i]),
                nGramDict[seeds_lines[i]]
            ),
            range(len(seeds_lines))
        )

        # Get possible rhyming words for each end word
        def try_find_rhyme(word, i):
            try:
                output = rhyme_finder(word)
            except KeyError:
                output = []
            return filter(
                lambda x: (len(get_word_meter(x)) < 2 and \
                len(get_word_meter(original_enders[i])) < 2) or \
                get_word_meter(x) == get_word_meter(original_enders[i]),
                output
            )

        # Rhyme possibilities for each line ending possibility
        rhyme_poss =  map(
            lambda i: map(lambda x: try_find_rhyme(x, i), line_enders[i]),
            range(len(line_enders))
        )

        # rhyme_poss = 
        #     filter(lambda x: get_word_meter(x) == get_word_meter(original_enders[i]),
        #         map(try_find_rhyme, line_enders[i])) for i in range(len(line_enders))
        # ]

        def intersect_words(i):
            coords = defaultdict(list)
            # i: current line for ender candidates
            # j: current line for rhyming candidates
            for j in range(len(lines)):
                if i == j:
                    pass
                else:
                    # k: current endword in line_enders[i]
                    for k in range(len(line_enders[i])):
                        inter = set(line_enders[j]) & set(rhyme_poss[i][k])
                        for word in inter:
                            coords[line_enders[i][k]].append((j, word))

                    # for k in range(len(line_enders[i])):
                    #     for word in rhyme_poss[i][k]:
                    #         if word in line_enders[j]:
                    #             coords[line_enders[i][k]].append((j, word))
            return coords
        
        # Match rhyme possibilities to line enders
        candidates = map(intersect_words, range(len(lines))) # now a list of dicts

        def best_candidate(interDict):
            def variance(tuplist):
                # Determines number of lines affected
                count = 0
                seen = []
                for ix, word in tuplist:
                    if ix in seen:
                        pass
                    else:
                        count += 1
                    seen.append(ix)
                return count

            try:
                best = max(interDict.iteritems(), key=lambda x: variance(x[1]))
            except ValueError:
                # max arg is empty sequence
                best = (None, None)
            return best

        # Find one with most possibilities
        choices = map(best_candidate, candidates)

        # Starting point
        enders = map(lambda x: x[-1], tokens_lines)

        # Iterate and make changes
        swapped = []
        record = []
        for i in range(len(lines)):
            if choices[i][0] is not None:
                enders[i] = choices[i][0]
                for ix, swapTo in choices[i][1]:
                    if not ix in swapped:
                        enders[ix] = swapTo
                        record.append((i, ix))
                        swapped.extend([i, ix])

        # Replace lines with new enders
        lines = map(
            lambda i: lines[i].replace(original_enders[i], enders[i]),
            range(len(lines))
        )

        return lines, record


    def rearrange(lines, scheme, rec):
        scheme = list(scheme.lower())

        groupsDict = {}
        for i, j in rec:
            if i in groupsDict:
                groupsDict[i].append(j)
            elif j in groupsDict:
                groupsDict[j].append(i)
            else:
                groupsDict[i] = [i, j]

        # print rec
        # print groupsDict
        # print groupsDict.items()

        groups = map(lambda x: list(set(x[1])), groupsDict.items())

        groups = sorted(groups, key=lambda x: len(x))
        scheme_groups = sorted(list(set(scheme)), key=lambda x: scheme.count(x))
        scheme_group_dict = {x:scheme.count(x) for x in list(set(scheme))}

        # print groups
        # print scheme_groups
        # print scheme_group_dict

        new_lines = ["" for _ in range(len(lines))]
        orphanLineIndices = list(set(range(len(lines))) - set(flatten(groups)))
        while groups and scheme_groups:
            curGroup = groups.pop()
            curX = scheme_groups.pop()
            for i in range(len(scheme)):
                if scheme[i] == curX:
                    try:
                        curI = curGroup.pop()
                    except IndexError:
                        pass
                    else:
                        new_lines[i] = lines[curI]
            if curGroup:
                orphanLineIndices.extend(curGroup)

        # print new_lines

        if groups:
            for g in groups:
                orphanLineIndices.extend(g)

        for i in range(len(new_lines)):
            if not new_lines[i]:
                ix = orphanLineIndices.pop()
                new_lines[i] = lines[ix]

        return new_lines


    # BACK TO MAIN FUNCTION...
    
    if arg_dict['--rhyme'] is not None:
        global rhymeDict
        rhymeDict = json.load( open('rhyme_dict.json', 'r') )
        final_lines, record = rhyme_map(final_lines)
        if arg_dict['--rhyme'].lower() != 'auto':
            final_lines = rearrange(final_lines, arg_dict['--rhyme'], record)


    # Fix capitalization, punctuation,
    # ensure last line ends with period
    final_lines = map(line_fix, final_lines)
    final_lines = last_line_fix(final_lines)

    return final_lines


if __name__ == '__main__':
    # Process docopt args
    wargv = docopt(__doc__, version='MeterMap v0.2')

    # Meter map
    lines = meter_map(wargv)

    # Print or write to file
    if wargv["<outfile>"] == "print":
        print "\n".join(lines)
    else:
        with open(wargv["<outfile>"], 'w') as outfile:
            outfile.write("\n".join(lines))

