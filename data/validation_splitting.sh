#!/usr/bin/env bash
head -n 2400 derstandard_preprocessed.txt > news.train
head -n 2400 krone_preprocessed.txt >> news.train
head -n 2400 diepresse_preprocessed.txt >> news.train
tail -n 600 derstandard_preprocessed.txt > news.valid
tail -n 600 krone_preprocessed.txt >> news.valid
tail -n 600 diepresse_preprocessed.txt >> news.valid