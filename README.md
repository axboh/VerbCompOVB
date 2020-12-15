# VerbCompOVB
This is the suite of Python and R scripts, as well as the coded data, I use in my paper *ICE corpora, register, and omitted variable bias: 
A multidimensional perspective.*

The Python extraction script was run on the raw text (not POS-tagged) versions of the ten ICE corpora in the paper, but it should work with any corpus of English
text in case you are interested in reproducing the method.

After the automatic extraction of cases, a couple of manual coding steps are involved, such as excluding false positive and coding for semantic category and
Aktionsart ("type") of the matrix and complement verb. This information is already included in the file VComps_annotated_manual_reduce_analysis.csv,
but if you want to apply the analysis to different data sets, you will need to manually code for these variables.
