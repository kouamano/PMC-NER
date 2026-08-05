#!/usr/bin/env python3

import argparse
import sys
import stanza

parser = argparse.ArgumentParser()
parser.add_argument("--lang", default="en")
parser.add_argument(
    "--ner",
    action="store_true",
    help="Enable Named Entity Recognition"
)
args = parser.parse_args()

processors = ["tokenize", "pos", "lemma"]

if args.ner:
    processors.append("ner")

nlp = stanza.Pipeline(
    lang=args.lang,
    processors=",".join(processors),
    tokenize_pretokenized=False
)

text = sys.stdin.read()

doc = nlp(text)

# NER結果を Word に対応付け
ner_map = {}

if args.ner:
    for ent in doc.ents:
        for tok in ent.tokens:
            for w in tok.words:
                ner_map[id(w)] = ent.type

# ヘッダ
print("TEXT\tLEMMA\tUPOS\tXPOS\tNER\tEOS")

for sent in doc.sentences:

    last = len(sent.words) - 1

    for i, word in enumerate(sent.words):

        ner = ner_map.get(id(word), "O")
        eos = 1 if i == last else 0

        print(
            word.text,
            word.lemma,
            word.upos,
            word.xpos,
            ner,
            eos,
            sep="\t"
        )
