import csv
import requests
from pymongo import MongoClient
import click

# globle vars
default_url = "https://docs.google.com/spreadsheets/d/1MDTs7jD1D8fSlYfp3lBzCqk8U9F27QxF1PMN40nu454/export?format=csv"


# helper method
def get_attribute(name, sample, returnType='none', nullValue='null'):

	try:
		val = sample[name]
	except KeyError:
		return nullValue

	if returnType == 'str':
		try:
			return str(val)
		except (ValueError, TypeError) as e:
			return nullValue
	elif returnType == 'float':
		try:
			return float(val)
		except (ValueError, TypeError) as e:
			return nullValue
	elif returnType == 'int':
		try:
			return int(val)
		except (ValueError, TypeError) as e:
			return nullValue
	else:
		return val



# Generate ICDO <-> NCIT mapping
# key : ICDO_morph + ICDO_topo
# values : [NCIT.CODE, NCIT.TERM]


@click.command()
@click.option('-u', '--url', default=default_url, help='Get the mapping from an url')
@click.option('-f', '--file', help='Get the mapping from a file')
@click.option('-l', '--log', type=click.File('w'), default='log.txt', help='Generate a log file')
@click.option('-d', '--database', default='arraymap', help='Use a specific database')
@click.option('-c', '--collection', default='samples', help='Use a specific collection')
def cli(url, file, log, database, collection):


	"""
	This script convert the icdo morphology and icdo topology codes of a sample to
	generate new ncit code and ncit term.
	The mapping is based on a provided file with expected structure and format.
	"""

	######################
	# init the db handler
	######################
	client = MongoClient()
	if database not in client.database_names():
		click.echo(database + ' does not exist')
		sys.exit()
	if collection not in client[database].collection_names():
		click.echo(collection + ' does not exist')
		sys.exit()
	db = client['arraymap']['samples']





	# init variables
	ctr_h = 0 # hit counter
	mappings = {}
	no_samples = db.count()

	# read in the mapping from either an url or a file
	if file :
		with open(file) as f:
			reader = csv.reader(f)	
			for line in reader:
				key = line[2].strip() + line[4].strip()
				mappings[key] = [line[5], line[6]]
	else:
		csvf = requests.get(url)
		reader = csv.reader(csvf.content.decode('utf-8').splitlines(), delimiter=',')
		for line in reader:
			key = line[2].strip() + line[4].strip()
			mappings[key] = [line[5], line[6]]
	
	# pull mappings into a dictionary
	# key: ICDO_morphology + ICDO_topology
	# values: [NCIT.CODE, NCIT.TERM]



	# draw the progress bar
	with click.progressbar(db.find(), label='Processing', fill_char=click.style('>',fg='green'), length=no_samples) as bar:
		

		# Go through the database
		for sample in bar:

			# get icdo values
			icd_m = get_attribute('ICDMORPHOLOGYCODE', sample)
			icd_t = get_attribute('ICDTOPOGRAPHYCODE', sample)

			# if the sample has both icdo attributes
			if (icd_m != 'null') and (icd_t != 'null'):

				# build the key
				key = icd_m.strip() + icd_t.strip()

				# if the ICDOs match a key in the mapping
				if key in mappings:
					# assign ncit values
					ncit_code = mappings[key][0].strip()
					ncit_term = mappings[key][1].strip()

					# if the NCIT.CODE is in the neoplasm core set
					term_id = 'NCIT:' + ncit_code
					qy = client['progenetix']['classifications'].find_one({'term_id':term_id})
					if qy != None:

						# wrtie the NCIT values to database
						db.update(	{'UUID': get_attribute('UUID', sample)}, 
									{'$set': {	'NCIT:CODE': ncit_code, 
												'NCIT:TERM': ncit_term
											 }
									}
								 )

						# update counter
						ctr_h += 1
						click.echo('HIT ' + str(ctr_h) + ':' + '\t', nl=False, file=log)
					else:
						click.echo('MISS CORE SET:' + term_id + '\t', nl=False, file=log)
						# assign basic tissue type 
						

				else: 
					click.echo('MISS MAPPING:' + '\t', nl=False, file=log)
					# assign basic tissue type
					
			else:
				click.echo('MISS ICD:' + '\t', nl=False, file=log)
			click.echo(icd_m + ' ' + icd_t + ' ' + get_attribute('UUID', sample), file=log)

	# close databse connection
	client.close()



# main
if __name__ == '__main__':
    cli()
