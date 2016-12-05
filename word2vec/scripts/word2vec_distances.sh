#!/bin/sh

DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src

TEXT_DATA=$DATA_DIR/mon5.cln
VECTOR_DATA=$DATA_DIR/mon5.vec

pushd ${SRC_DIR} && make; popd

echo -----------------------------------------------------------------------------------------------------
echo -- Querying word distances...

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA

