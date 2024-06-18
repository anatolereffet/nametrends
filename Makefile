#Globals
PYTHON_INTERPRETER = python3
DIR_PATH = $(shell pwd)
GEOJSON_FILE = departement_avec_outremer_rapprochee.geojson

requirements:
	$(PYTHON_INTERPRETER) pip install -r requirements.txt

pull_data:
	@mkdir -p data
	@test -e $(DIR_PATH)/data/dpt2020.csv || wget https://perso.telecom-paristech.fr/eagan/class/igr204/data/dpt2020.csv -P $(DIR_PATH)/data
	@test -e $(DIR_PATH)/data/$(GEOJSON_FILE) || wget -O $(DIR_PATH)/data/$(GEOJSON_FILE) https://raw.githubusercontent.com/Kaosamami/france-geojson/main/departement_avec_outremer_rapprochée.geojson

clean_data:
	@$(PYTHON_INTERPRETER) src/process_data.py 

data: pull_data clean_data
	@echo "Data pulled and cleaned."

app:
	$(PYTHON_INTERPRETER) src/app/main.py