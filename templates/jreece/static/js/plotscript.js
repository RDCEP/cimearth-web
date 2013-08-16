/*    
    [            						[
	  ['Year', 'Sales', 'Expenses'],	  ['Year', 'AFR', 'BRA', ...],
	  ['2004',  1000,      400],	  	  ['2004',  1000,  400, ...],
	  ['2005',  1170,      460],	  	  ['2005',  1170,  460, ...],
	  ['2006',  660,       1120],	      ['2006',  660,   1120, ...],
	  ['2007',  1030,      540]	  		  ['2007',  1030,  540, ...]
	]									]			

*/

/*	

	First, years are stored at the first indeces of all the sub-arrays.
 	
 		For each year in the row:
 			plot-array[year index][first index (i.e. "0")] gets year

 	Each row in question then gets a subsequent place in the first sub-array.

 		For each row:
 			plot-array[0][index of row] gets name of row

 	Last, subsequent sub-arrays get tax values of rows at the same indices as the rows have in the first sub-array.

		For each row:
			plot-array[year index][row index] gets "rows[row index][year index]" -- tax value of row at year

	For example,

		plot-array at index 1 is data for regions at the year "2004" (index 1 = the second index; 0, the first, holds headers)

		the array at (plot-array at index 1) at index *one* gets the value of the *first* region at
		the *first* index -- the tax data value of the first region in the first year, "2004"

		the array at (plot-array at index 1) at index *two* gets the value of the *second* region at
		the *first* index -- the tax data value of the *second region* in the *first* year, "2004"

*/

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

Object.indexArr = function(obj) {
	var i, a = new Array([], []);
	for (i in obj) {
		if (obj.hasOwnProperty(i)) {
			a[0].push(i);
			a[1].push(obj[i]);
		}
	}
	return a;
}

function makeArr(len, num) {
	var a = [];
	for (var i=0; i<len; i++) a.push(num);
	return a;
}

/* Create var "arr" */
var arr = []; for (var i=0; i<27; i++) arr.push(String(i+".0"));

var ones = []; for (var i=0; i<27; i++) ones.push("1.0");

/* Create var "zeros" */
var zeros = []; for (var i=0; i<27; i++) zeros.push(0.0);

function formatPoints(rows) {

	// var rows = new Object();
	// rows.AFR = makeArr(27, 5);
	// rows.BRA = makeArr(27, 3);
	// rows.CAN = makeArr(27, 5);
	// rows.EAA = makeArr(27, "foo");

	var years = []; for (var i=4; i<=30; i++) years.push(String(2000 + i));

	var plotArr = [["Years"]];

	/* 1). Assign years to the first indeces of all but the first sub-array */
	for (var i=0; i<years.length; i++) {
		plotArr[(i+1)] = [];
		plotArr[(i+1)][0] = years[i]; // "plotArr[i+1]" -- start at second sub-array, first holds units ("Years", "Regions", etc.)
	}

	/* 2). Assign region/header names in first array of "plotArr" */
	var k = 0;
	for (var i in rows) {
		plotArr[0][k+1] = i;
		k++;
	}

	var rowArrs = Object.indexArr(rows);

	for (var j=1; j<(years.length)+1; j++) {
		for (var i=0; i<rowArrs[1].length; i++) {
			plotArr[j][(i+1)] = parseInt(rowArrs[1][i][(j-1)]);
		}
	}

	return plotArr;

}
