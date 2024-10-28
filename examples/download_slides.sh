#!/bin/bash

DIR="tcga/bladder"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/bladder.tsv -d $DIR


DIR="tcga/brain"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/brain.tsv -d $DIR

DIR="tcga/esophagus"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/esophagus.tsv -d $DIR

DIR="tcga/gallblader"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/gallblader.tsv -d $DIR

DIR="tcga/kidney"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/kidney.tsv -d $DIR

DIR="tcga/lymph_nodes"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/lymph_nodes.tsv -d $DIR

DIR="tcga/ovarian"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/ovarian.tsv -d $DIR

DIR="tcga/pancreas"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/pancreas.tsv -d $DIR

DIR="tcga/skin"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/skin.tsv -d $DIR

DIR="tcga/testis"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/testis.tsv -d $DIR

DIR="tcga/thyroid"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/thyroid.tsv -d $DIR

DIR="tcga/uterus"
if [ ! -d "$DIR" ]; then
  echo "dir = $DIR"
  mkdir -p "$DIR"
fi
./gdc-client download -m tcga/uterus.tsv -d $DIR
