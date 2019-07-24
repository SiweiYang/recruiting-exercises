init:
	virtualenv -p python3 venv; . venv/bin/activate; pip install -r requirements.txt; pip install .

example:
	. venv/bin/activate; python inventoryallocator/__init__.py '{ apple: 1 }' '[{ name: owd, inventory: { apple: 1 } }]'

test:
	. venv/bin/activate; PYTHONPATH=. pytest --cov=inventoryallocator tests -svv
