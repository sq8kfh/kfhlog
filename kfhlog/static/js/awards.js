function show_award(award) {
    $("div#" + award + " > table > tbody").empty();
    profile = null;
    group = null;
    if(parseInt($("#profile").val().trim()) >= 0)
        profile = parseInt($("#profile").val().trim());
    if(parseInt($("#group").val().trim()) >= 0)
        group = parseInt($("#group").val().trim());
    $.ajax({
	    type:'POST',
		url: '/api/award_' + award,
		data: JSON.stringify({"profile": profile, "group": group}),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			if( jsn.status != 'ok') {
			    alert("Error")
	            return;
	        }
	        $.each(jsn[award], function(rowIndex, r) {
		        tr = $('<tr>');
		        $.each(r, function(colIndex, d) {
		            c = null;
		            l = null;
		            if (d != null) {
		                c = d['data']
		                l = d['href']
		            }
		            ch = 0;
		            if (award == 'dxcc') ch = 1;

		            td = $("<t"+(colIndex <= 0 ?  "h" : "d")+"/>")
		            if (l != null) {
		                href = $("<a href=\""+l+"\" />")
		                if (c === "") href.text("?")
		                else href.text(c);
		                td.append(href);
		            }
		            else {
		                if (c === "") td.text("?")
		                else td.text(c);
                    }
		            if(colIndex > ch && c != null) {
		                if(c === "")
		                    td.addClass('green');
		                else
    		                td.addClass('red');
		            }
		            tr.append(td);
                });
                $("div#" + award + " > table > tbody").append(tr)
	        });
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function open_tab(tab) {
    $('#tabs > div').each(function () {
        $( this ).css("display", "none");
    });
    $('#' + tab).css("display", "block");
    switch (tab) {
    case 'general':
        show_award('general')
        break;
    case 'dxcc':
        show_award('dxcc')
        break;
    case 'cq':
        show_award('cq')
        break;
    case 'itu':
        show_award('itu')
        break;
    }
}

function update_preset() {
    preset = {}
    preset['profile'] = parseInt($('#profile').val().trim());
    preset['group'] = parseInt($('#group').val().trim());
    $.ajax({
	    type:'POST',
		url: '/api/set_awards_preset',
		data: JSON.stringify(preset),
		contentType: 'application/json; charset=utf-8',
	});
}

function profilegroup_change() {
    open_tab('general');
    update_preset();
}

$(document).ready(function() {
    $("#profile").change(profilegroup_change);
    $("#group").change(profilegroup_change);

    open_tab('general');
});
