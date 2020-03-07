#!/usr/bin/env bash

# ./path.sh
export PATH=/opt/kaldi/src/online2bin/:/opt/kaldi/src/latbin:$PATH

steps/online/nnet3/decode.sh --nj 1 --acwt 1.0 --post-decode-acwt 10.0 experiment/tdnn_7b_chain_online/graph/ transcriptions/ experiment/tdnn_7b_chain_online/decode

lattice-best-path --word-symbol-table=experiment/tdnn_7b_chain_online/graph/words.txt "ark:zcat experiment/tdnn_7b_chain_online/decode/lat.1.gz |" ark,t:- | utils/int2sym.pl -f 2- experiment/tdnn_7b_chain_online/graph/words.txt > transcriptions/guess.txt

rm -r experiment/tdnn_7b_chain_online/decode transcriptions/split1

echo
echo
echo

cat transcriptions/guess.txt

echo
echo
echo