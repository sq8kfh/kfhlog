function ord (string) {
  // http://kevin.vanzonneveld.net
  // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // +   bugfixed by: Onno Marsman
  // +   improved by: Brett Zamir (http://brett-zamir.me)
  // +   input by: incidence
  // *     example 1: ord('K');
  // *     returns 1: 75
  // *     example 2: ord('\uD800\uDC00'); // surrogate pair to create a single Unicode character
  // *     returns 2: 65536
  var str = string + '',
    code = str.charCodeAt(0);
  if (0xD800 <= code && code <= 0xDBFF) { // High surrogate (could change last hex to 0xDB7F to treat high private surrogates as single characters)
    var hi = code;
    if (str.length === 1) {
      return code; // This is just a high surrogate with no following low surrogate, so we return its value;
      // we could also throw an error as it is not a complete character, but someone may want to know
    }
    var low = str.charCodeAt(1);
    return ((hi - 0xD800) * 0x400) + (low - 0xDC00) + 0x10000;
  }
  if (0xDC00 <= code && code <= 0xDFFF) { // Low surrogate
    return code; // This is just a low surrogate with no preceding high surrogate, so we return its value;
    // we could also throw an error as it is not a complete character, but someone may want to know
  }
  return code;
}

function toRad(value) {
    /** Converts numeric degrees to radians */
    return value * Math.PI / 180;
}

function toDeg(value) {
   return value * 180 / Math.PI;
}

function calcdisazi(grid1, grid2) {
	var lon1 = (ord(grid1[0]) - ord('A')) * 20 - 180;
	var lat1 = (ord(grid1[1]) - ord('A')) * 10 - 90;
	lon1 += (ord(grid1[2]) - ord('0')) * 2;
	lat1 += (ord(grid1[3]) - ord('0')) * 1;

	if (grid1.length > 4) {
		lon1 += ((ord(grid1[4])) - ord('a')) * 5/60;
		lat1 += ((ord(grid1[5])) - ord('a')) * 2.5/60;
		lon1 += 2.5/60;
		lat1 += 1.25/60;
	}
	else {
		lon1 += 1;
		lat1 += 0.5;
	}

	var lon2 = (ord(grid2[0]) - ord('A')) * 20 - 180;
	var lat2 = (ord(grid2[1]) - ord('A')) * 10 - 90;
	lon2 += (ord(grid2[2]) - ord('0')) * 2;
	lat2 += (ord(grid2[3]) - ord('0')) * 1;

	if (grid2.length > 4) {
		lon2 += ((ord(grid2[4])) - ord('a')) * 5/60;
		lat2 += ((ord(grid2[5])) - ord('a')) * 2.5/60;
		lon2 += 2.5/60;
		lat2 += 1.25/60;
	}
	else {
		lon2 += 1;
		lat2 += 0.5;
	}

	var R = 6371; // km
	var dLat = toRad(lat2-lat1);
	var dLon = toRad(lon2-lon1);
	lat1 = toRad(lat1);
	lat2 = toRad(lat2);

	//var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
	//        Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
	//var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
	//var d = R * c;

	var d2 = Math.acos(Math.sin(lat1)*Math.sin(lat2) + 
                  Math.cos(lat1)*Math.cos(lat2) *
                  Math.cos(lon2-lon1)) * R;

	var d= Math.acos(Math.sin(lat1)*Math.sin(lat2) + 
                  Math.cos(lat1)*Math.cos(lat2) *
                  Math.cos(dLon)) * R;

	var y = Math.sin(dLon) * Math.cos(lat2);
	var x = Math.cos(lat1)*Math.sin(lat2) -
        Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
	var brng = toDeg(Math.atan2(y, x));

	//return d.toFixed(2);
	return {'dis':d.toFixed(2), 'az':brng.toFixed(1)};
}
//calcdisazi('KO10cc','KO10cc');

function calc() {
	var grid = $("#loc1").val().trim();

	var lon1 = (ord(grid[0]) - ord('A')) * 20 - 180;
	var lat1 = (ord(grid[1]) - ord('A')) * 10 - 90;
	lon1 += (ord(grid[2]) - ord('0')) * 2;
	lat1 += (ord(grid[3]) - ord('0')) * 1;

	if (grid.length > 4) {
		lon1 += ((ord(grid[4])) - ord('A')) * 5/60;
		lat1 += ((ord(grid[5])) - ord('A')) * 2.5/60;
		lon1 += 2.5/60;
		lat1 += 1.25/60;
	}
	else {
		lon1 += 1;
		lat1 += 0.5;
	}

	$("#loc1lon").val(lon1);
	$("#loc1lat").val(lat1);

	var grid2 = $("#loc2").val().trim();

	var lon2 = (ord(grid2[0]) - ord('A')) * 20 - 180;
	var lat2 = (ord(grid2[1]) - ord('A')) * 10 - 90;
	lon2 += (ord(grid2[2]) - ord('0')) * 2;
	lat2 += (ord(grid2[3]) - ord('0')) * 1;

	if (grid2.length > 4) {
		lon2 += ((ord(grid2[4])) - ord('A')) * 5/60;
		lat2 += ((ord(grid2[5])) - ord('A')) * 2.5/60;
		lon2 += 2.5/60;
		lat2 += 1.25/60;
	}
	else {
		lon2 += 1;
		lat2 += 0.5;
	}

	$("#loc2lon").val(lon2);
	$("#loc2lat").val(lat2);

	var R = 6371; // km
	var dLat = toRad(lat2-lat1);
	var dLon = toRad(lon2-lon1);
	lat1 = toRad(lat1);
	lat2 = toRad(lat2);

	//var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
	//        Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
	//var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
	//var d = R * c;

	var d2= Math.acos(Math.sin(lat1)*Math.sin(lat2) + 
                  Math.cos(lat1)*Math.cos(lat2) *
                  Math.cos(lon2-lon1)) * R;



	var y = Math.sin(dLon) * Math.cos(lat2);
	var x = Math.cos(lat1)*Math.sin(lat2) -
        Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
	var brng = toDeg(Math.atan2(y, x));

	$("#dis").val(d2.toFixed(2));
	$("#az").val(brng.toFixed(1));
}

$(document).ready(function() {
	$("#loc1").change(calc);
	$("#loc2").change(calc);
});