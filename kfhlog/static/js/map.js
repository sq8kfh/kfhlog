function show_itu() {
    profile = null;
    group = null;
    if(parseInt($("#profile").val().trim()) >= 0)
        profile = parseInt($("#profile").val().trim());
    if(parseInt($("#group").val().trim()) >= 0)
        group = parseInt($("#group").val().trim());
    $.ajax({
	    type:'POST',
		url: '/api/made_itu',
		data: JSON.stringify({"profile": profile, "group": group}),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			if( jsn.status != 'ok') {
			    alert("Error")
	            return;
	        }
	        D=document.getElementById("map");
            SVGDoc = D.getSVGDocument();
	        $.each(jsn.itu, function(ituIndex, itu_zone) {
		        SVGDoc.getElementById('itu_' + itu_zone).classList.add('red');
            });
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function map_load() {
    D=document.getElementById("map");
	SVGDoc = D.getSVGDocument();
	var countryElements = SVGDoc.getElementById('itu').childNodes;
	var countryCount = countryElements.length;
	for (var i = 0; i < countryCount; i++) {
		countryElements[i].onmouseover = function() {
		    document.getElementById("itu_zone").value = this.getAttribute('data-zone');
	    }
	    countryElements[i].onclick = function() {
	        window.location.href = "log?ituz=" + this.getAttribute('data-zone');
	    }
	}
	//SVGDoc.getElementById('itu_18').classList.add('red');
	//SVGDoc.getElementById('itu_33').classList.add('red');
	show_itu();
}

function update_preset() {
    preset = {}
    preset['profile'] = parseInt($('#profile').val().trim());
    preset['group'] = parseInt($('#group').val().trim());
    $.ajax({
	    type:'POST',
		url: '/api/set_map_preset',
		data: JSON.stringify(preset),
		contentType: 'application/json; charset=utf-8',
	});
}

function profilegroup_change() {
    update_preset();
}

$(document).ready(function() {
    $("#profile").change(profilegroup_change);
    $("#group").change(profilegroup_change);
});
