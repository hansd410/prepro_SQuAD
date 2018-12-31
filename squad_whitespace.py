import sys
import json
import csv
import copy

infilename = sys.argv[1]
outfilename = sys.argv[2]


with open(infilename) as data_file:
	json_data = json.load(data_file)

whitespace_json_data = open(outfilename, 'w', newline='')

wholeAnswerCount = 0
wrongAnswerCount = 0
for datum in json_data["data"]:
	for paragraphs in datum["paragraphs"]:
		paragraphs["context"]=' '.join(paragraphs["context"].split())
		for qas in paragraphs["qas"]:
			question = qas["question"]
			qas["question"]=' '.join(qas["question"].split())

json.dump(json_data,whitespace_json_data)
