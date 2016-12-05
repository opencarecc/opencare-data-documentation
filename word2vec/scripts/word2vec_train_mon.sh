#!/bin/sh

DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src

TEXT_DATA=$DATA_DIR/mon5.cln
VECTOR_DATA=$DATA_DIR/mon5.vec

pushd ${SRC_DIR} && make; popd

echo -- Training vectors...
time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 0 -size 200 -min-count 101 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
  

echo -----------------------------------------------------------------------------------------------------
echo -- distance...

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA

