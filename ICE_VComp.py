#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
### This is the script I used for feature extraction for my paper     ###
### on verb complementation and omitted variable bias. If you use     ###
### this script, please consider citing:                              ###
### Bohmann, Axel. Forthcoming. ICE corpora, register, and omitted    ###
###     variable bias: A multidimensional perspective. In M. Krug,    ###
###     O. Schützler, F. Vetter & V. Werner (eds.). Perspectives on   ###
###     Contemporary English. Bamberg Studies in English Linguistics. ###
###     Berlin et al.: Peter Lang                                     ###
#########################################################################


assert len(sys.argv) == 2, 'Please provide a valid directory name to the corpus data (and no other arguments) in addition to the program name'
assert os.path.isdir(sys.argv[1]), 'Argument is not a valid directory'
rootdir = sys.argv[1]


corpus = nltk.corpus.PlaintextCorpusReader(rootdir.rstrip("/")+"/", ".*txt")
text_files = corpus.fileids()

### allow for "not" between verb and complement

afford_re = r"\b(afford)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
bear_re = r"\bcan(?:not|'t)?\s(bear)()\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
begin_re = r"\b(beg)([aiu]n(?:ning|s)?)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b" ## add negative lookahead to prevent "beginning to the end", "beginning to a new.."
bother_re = r"\b(bother)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
cease_re = r"\b(ceas)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
choose_re = r"\b(cho)(o?se[ns]?|osing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
continue_re = r"\b(continu)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
dare_re = r"\b(dar)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
deserve_re = r"\b(deserv)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
enjoy_re = r"\b(enjoy)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
expect_re = r"\b(expect)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
hate_re = r"\b(hat)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
help_re = r"(?<!can't\s|cannot)\b(help)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b" ### needs to allow for insertion of obj PN "Help me x"
intend_re = r"\b(intend)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
like_re = r"\b(lik)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
love_re = r"\b(lov)(e[ds]?|ing)\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
neglect_re = r"\b(neglect)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
offer_re = r"\b(offer)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b" ### needs to allow for insertion of obj PN "Help me x"
prefer_re = r"\b(prefer)(red|s|r?ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
pretend_re = r"\b(pretend)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
start_re = r"\b(start)(ed|s|ing)?\s(?!(?:any|some|every|no)thing)(to|\w+ing)\b"
try_re = r"\b(tr)(y(?:ing)?|ie[ds])\s(?!(?:any|some|every|no)thing)(to|and|\w+ing)\b"


REs = [afford_re, bear_re, begin_re, bother_re, cease_re, choose_re, continue_re,
      dare_re, deserve_re, enjoy_re, expect_re, hate_re, help_re, intend_re, like_re,
      love_re, neglect_re, offer_re, prefer_re, pretend_re, start_re, try_re]

country_codes = {"Canada":"CA",
                 "GB": "GB",
                 "HongKong": "HK",
                 "India": "IN",
                 "Ireland": "IE",
                 "Jamaica": "JM",
                 "New Zealand": "NZ",
                 "Phillipines": "PH",
                 "Singapore": "SG",
                 "USA": "US"}


def transform_group(triple):
    verb, inf, comp = triple[0], triple[1], triple[2]
    if verb == "beg":
        verb = "begin"
    elif verb in ["ceas", "continu", "dar", "deserv", "hat", "lik", "lov"]:
        verb = verb + "e"
    elif verb == "cho":
        verb = "choose"
    elif verb == "tr":
        verb = "try"
    if inf.endswith("ing"):
        inf = "ing"
    elif inf in ["", "in", "e", "ose", "y"]:
        inf = "pres"
    elif inf in ["ed", "se", "sen", "an", "un", "red", "ied"]:
        inf = "past"
    elif inf.endswith("s"):
        inf = "thirdSG"
    if comp.endswith("ing"):
        comp2 = "ing"
    elif com = "and":
        comp2 = "and"
    else:
        comp2 = "to"
    return (verb, inf, comp2, comp)

scores = {}
with open("FactorScores.csv") as s:
    for line in s.readlines():
        items = [x.strip('"') for x in line.split()]
        scores[items[0]] = "\t".join(items[1:])


def write_results(filename, outfile):
    country, ICEcat, ID = filename.split("-")
    with open(os.path.join(rootdir, filename), "r", errors='ignore') as f:
        text = f.read()
    for pattern in REs:
        hits = re.findall(pattern, text)
        for hit in hits:
            res = transform_group(hit)
            outfile.write("-".join([country_codes[country],ICEcat,ID]) + "\t" + country + "\t" + ICEcat + "\t" + 
                          ID.strip(".txt") + "\t" + res[0] + "\t" + res[1] + "\t" + res[2] + "\t" + res[3] +"\t"+
                          scores["-".join([country_codes[country],ICEcat,ID])]+"\n")
    


# Create the file to write to and a header line with colnames
with open("VComp.txt","w") as p:
    p.write("file\tcountry\tcategory\tID\tverb\tinflection\tcomplement\tcomplementFull\tPA1\tPA2\tPA3\tPA4\tPA5\tPA6\tPA7\tPA8\tPA9\tPA10\tcountry\tmodality\tcategory\tcircle\tregion\tphase\n")
    for text_file in text_files:
        write_results(text_file, p)

