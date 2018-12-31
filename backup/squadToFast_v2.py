import sys
import json
import csv
import copy

def get_word_index(context, answer_start, answer_text):
	words = context.split(' ')
	char_index = 0
	word_index = 0
	while (char_index < answer_start):
		char_index += len(words[word_index]) + 1
		word_index += 1

	#answer_text_2 = ' '.join(words[word_index : word_index + len(answer_text.split(' '))])
    #print (answer_text + '|||' + answer_text_2)
    #assert(answer_text.lower() == answer_text_2.lower())
	return(word_index, word_index + len(answer_text.split(' ')))


infilename = sys.argv[1]
outfilename = sys.argv[2]


with open(infilename) as data_file:
	json_data = json.load(data_file)

csv_data = open(outfilename, 'w', newline='')
writer = csv.DictWriter(csv_data, delimiter = ',', fieldnames=['story_id', 'story_text', 'question', 'answer_token_ranges'])
writer.writeheader()

for datum in json_data["data"]:
	for paragraphs in datum["paragraphs"]:
		context = paragraphs["context"]
		for qas in paragraphs["qas"]:
			question = qas["question"]
			qas_id = qas["id"]
			for answers in qas["answers"]:
				char_startindex = answers["answer_start"]
				answer_text = answers["text"]
				char_endindex = char_startindex+len(answer_text)
			
				(word_startindex, word_endindex) = get_word_index(context, char_startindex, answer_text)

				context_copy = copy.deepcopy(context)
				addedSpaceNum =0
				for i in range(len(context)):
					if(context[i] != ' ' and (not context[i].isalnum())):
						if(i>0 and context_copy[i+addedSpaceNum-1]!=' '):
							context_copy = context_copy[:i+addedSpaceNum]+' '+context_copy[i+addedSpaceNum:]
							if(char_startindex>=i):
								word_startindex += 1
							if(char_endindex>=i):
								word_endindex += 1
							addedSpaceNum+=1
						if(i<len(context)-1 and context_copy[i+addedSpaceNum+1]!=' '):
							context_copy = context_copy[:i+addedSpaceNum+1]+' '+context_copy[i+addedSpaceNum+1:]
							if(char_startindex>i):
								word_startindex += 1
							if(char_endindex>i):
								word_endindex += 1
							addedSpaceNum+=1
				answer_wordrange_string = str(word_startindex) + ':' + str(word_endindex)
				writer.writerow({'story_id': qas_id, 'story_text': context_copy, 'question': question, 'answer_token_ranges': answer_wordrange_string})
				if(context_copy.split()[word_startindex:word_endindex]!=answer_text):
					print("|"+answer_text+"|\t|"+context_copy.split()[word_startindex:word_endindex]+"|")


		    
    #paragraph = datum["paragraphs"][0]
    #context = paragraph["context"].replace('\n', '\\n')
    #qas = paragraph["qas"][0]
    #answers = qas["answers"]
    #qas_id = qas["id"]
    #question = qas["question"]
    #if answers == []:
    #    print (qas_id)
    #    continue
    #answer_start = answers[0]["answer_start"]
    #answer_text = answers[0]["text"]

#    (answer_startindex, answer_endindex) = get_word_index(context, answer_start, answer_text)
#    answer_wordrange_string = str(answer_startindex) + ':' + str(answer_endindex)
#    writer.writerow({'story_id': qas_id, 'story_text': context, 'question': question, 'answer_token_ranges': answer_wordrange_string})

