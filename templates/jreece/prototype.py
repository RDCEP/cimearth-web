models = {
	'TRADE':'bta16x16',
	'BIO':'bio15x27',
	'LIFE':'dis16x16x21x12',
	'ENERGY':'elec16x24'
}

# get inputted values (model, name, description, all tax/year/region data points) from form website

def pageRecieve(data):

	# get inputted values (model, name, description, all tax/year/region data points) from form website
	ascefWrite('ascef-1.5.5', data['model'], data, data['name']) # call ascefWrite()
	# arguments to pass: 
	#		-model chosen from radio button --> model;
	#		-ascef-1.5.5 (probably what everyone will be using) --> ascef;
	#		-tax/year/region data points --> points (possibly formatted here or in ascefWrite());
	#		-name/id generated somewhere --> scen_id


def ascefWrite(ascef, model, points, scen_id):
	m = models[model]

	#must make files before writing to them

	tax = open("/Users/jackreece/Desktop/CI/SVN/ascef/releases/"+ascef+"/instances/"+m+"/scenarios/CO2_taxes/"+scen_id+".dat", "w")

	# "l" is for "leakage"
	l_dat = open("/Users/jackreece/Desktop/CI/SVN/ascef/releases/"+ascef+"/instances/"+m+"/scenarios/leakage/ampl_files/"+scen_id+".dat", 'w')
	l_cmd = open("/Users/jackreece/Desktop/CI/SVN/ascef/releases/"+ascef+"/instances/"+m+"/scenarios/leakage/ampl_files/"+scen_id+"_1.cmd", 'w')
	l_mod = open("/Users/jackreece/Desktop/CI/SVN/ascef/releases/"+ascef+"/instances/"+m+"/scenarios/leakage/ampl_files/"+scen_id+".mod", 'w')
	sh = open("/Users/jackreece/Desktop/CI/SVN/ascef/releases/"+ascef+"/"+scen_id+".sh", 'w')

	tax.write(points)
	l_dat.write("""
param CO2TaxTrend:
include scenarios/co2_taxes/%s.dat
;

""" % scen_id)

	l_cmd.write("""
#####
# Set Tax Rates for CO2
#####

let {r in Regions} Endogenous_QuantityTax[r,'CO2'] := CO2TaxTrend[r,tm];

""")
	l_mod.write("param CO2TaxTrend {Regions_All,0..26} default 0;")

	sh.write("""
setenv Scenario "{0}";
ampl {1}.cmd > instances/{1}/output/{0}.out;""".format(scen_id, m))
