python squad_whitespace.py data/json_original/dev-v1.1.json data/whitespace/dev_whitespace.json
python squad_whitespace.py data/json_original/train-v1.1.json data/whitespace/train_whitespace.json
python squadToFast.py data/whitespace/dev_whitespace.json data/result/dev.csv
python squadToFast.py data/whitespace/train_whitespace.json data/result/train.csv

