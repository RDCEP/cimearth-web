import itertools
a = []
for i in range(0,27):
	a.append(0)

d = {"one": a, "two": a, "three": a}

r = ['AFR','BRA', 'CAN', 'EAA', 'IND', 'JAP', 'LAM', 'MEX', 'MNA', 'OCN', 'REU', 'RUS', 'SEA', 'SOA', 'USA', 'WEU']

t = ['one', 'two', 'three']

def datToFile(imported):
	rowit, colit, dataArr = [], [], []
	dataset = {}
	for i in range(0,27): colit.append(i)
	for i in range(0,16): rowit.append(i)
	print rowit
	print colit

	for i in rowit:
		dataArr = []
		for j in colit:
			index = str(((i*j) + j))
			if index in imported[index][:(len(imported[index])-2)]:
				dataArr.append(imported[index])
		dataset[i] = dataArr

def datCheck(data):
	nums = []
	for i in range(0,431):
		nums.append(str(i))
	for i in nums:
		for j in data:
			if i in j[:len(i)] and len(i) == (len(j) - 2): # check if i is found in j after as many characters as i is long, and if i is as long as j without the "-1" on the end
				print 'yes: ' + i + ' in ' + j

def rowWrite(array):
	s = ''
	for i in range(0, (len(array))):
		if i < ((len(array))-1):
			if array[i] == '':
				s += '0 '
			else:
				s += (str(array[i]) + ' ')
		else:
			if array[i] == '':
				s += '0'
			else:
				s += (str(array[i]))
	return s

def dictRows(dict):
	row = ''
	for i in dict:
		row += (str(i) + ' ')
		row += (str(rowWrite(dict[i])))
		row += '\n'
	return row

def oneRow(key, val):
	result = ''
	result += (str(key) + ' ' + str(rowWrite(val)))
	return result

def df(dict, reference):
	zeros = a
	content = ''
	content += (rowWrite(range(0,27)) + ' :=\n')
	for i in reference:
		if dict.get(i) != None:
			content += (str(oneRow(i, dict[i])) + '\n')
		else:
			content += (str(oneRow(i, zeros)) + '\n')

	content = content[:-1]
	return content

def ddf(data):
	for i in data:
		if 'scenario' in i:
			scen = data[i]
			print 'ascef-1.5.5'
			print data['model']
			print(df(scen, r))
			print scen['Name']
			# ascefWrite('ascef-1.5.5', data['model'], df(scen, r), scen['Name'])


def getMidChar(s):
	t = s[(s.index('-')+1):]
	u = t[:-(len(t)-t.index('-'))]
	return u

# def parsePageData(data):
# 	for i in data:
# 		for j in r:
# 			if j in i[:-3]:
# 				#finish this so it makes dictionary entries of region => array of data points