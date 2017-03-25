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
		        $.each(r, function(colIndex, c) {
		            td = $("<t"+(colIndex == 0 ?  "h" : "d")+"/>").text(c);
		            if(colIndex > 1 && c != null) {
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

$(document).ready(function() {
    open_tab('general');
});
