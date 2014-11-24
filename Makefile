vector:
	python changing_environment_ga.py -c vector_config.ini

run:
	python changing_environment_ga.py -c config.ini

clean:
	rm *~ *.pyc *.csv

test:
	python -m unittest discover