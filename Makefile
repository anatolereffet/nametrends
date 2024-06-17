#Globals

PYTHON_INTERPRETER = python3
DIR_PATH = $(shell pwd)

requirements:
	$(PYTHON_INTERPRETER) pip install -r requirements.txt

data:
	mkdir data
	wget https://perso.telecom-paristech.fr/eagan/class/igr204/data/dpt2020.csv -P $(DIR_PATH)/data

app:
	$(PYTHON_INTERPRETER) src/app/main.py