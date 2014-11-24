vector:
	python changing_environment_ga.py -c vector_config.ini -o test_data

run:
	python changing_environment_ga.py -c config.ini -o test_data

clean:
	rm *~ *.pyc *.csv

test:
	python -m unittest discover