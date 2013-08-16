var regionsArr = new Array('AFR','BRA', 'CAN', 'EAA', 'IND', 'JAP', 'LAM', 'MEX', 'MNA', 'OCN', 'REU', 'RUS', 'SEA', 'SOA', 'USA', 'WEU');
var dropdown = '';
var years = new Array();
// var selIndex = new Array('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p')
for (var i=4; i<=30; i++) {
  years.push(2000 + i);
}

for (var n=0; n<(regionsArr.length); n++) {
    dropdown += "<option value='"+regionsArr[n]+"'>" + regionsArr[n] + "</option>";
  }

function gridDraw() {
  var cols = years.length;
  var rows = 1;

  // document.write("<form>");
  for (var i=0; i<=rows; i++) {
    document.write("<ul class='grid'>"); // Mainly in place for styling purposes
    if (i!=0) {
      document.write("<span class='row'>");
      document.write("<input type=button class='rmRow' value=' X '>");
      document.write("<select class='select' name='select'>"+dropdown+"</select>"); // Draws dropdown menus

      // document.write("<span class='checkspan'><input type='checkbox' class='check'>"); // Left over from when countries
      // document.write(String(countries[(i-1)])+"</span>");                              // were shown as checkboxes
      
    }
    for (var j=0; j<cols; j++) {
      if (i == 0 && j == 0) {
        document.write("<span class='yearspan'>");
        for (var y=0; y<years.length; y++) {
          document.write("<span class='year'>"+years[y]+"</span>");
        }
        document.write("</span>");
      }
      else if (i==0) {

      }
      else if (j==(cols - 1)) {
        document.write("<input type='text' name='" + String(years[j]) + "' value=0>"); // '"+ String(((i - 1) * cols) + j) +"'
        document.write("</span>");
      }
      else {
        document.write("<input type='text' name='" + String(years[j]) + "' value=0>");
      }
    }
    document.write("</ul>");
  }
  // document.write("</form>");

}