function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function set_previous_qso(data) {
	$("#previou_table > tbody").empty();
	if( data.status != 'ok')
	    return;
	$.each(data.qso, function(i, item) {
		$('#previou_table > tbody').append('<tr><td>' + item[0] + '</td><td>' + item[1] + '</td><td>' + item[2] + '</td></tr>');
	});
}

function set_dxcc(data) {
    if( data.status != 'ok')
	    return;
    $("#dxcc_select").val(data.dxcc);
    $("#dxcc_select").trigger("chosen:updated");
    $("#cqz_input").val(data.cqz);
    $("#ituz_input").val(data.ituz);
}

function update_date_on() {
	var d=new Date();
	$("#date_on_date").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	$("#date_on_time").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
}

function call_change() {
    call = $("#call_input").val().trim();
    $.ajax({
	    type:'POST',
		url: '/api',
		data: JSON.stringify({"find_prefix": {"call": call}, "get_previous": {"call": call}}),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			set_previous_qso(jsn.get_previous);
			set_dxcc(jsn.find_prefix);
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function freq_change() {
    freq = $("#freq_input").val().trim();
    $.ajax({
	    type:'POST',
		url: '/api/get_band',
		data: JSON.stringify({"freq": freq}),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			if( jsn.status != 'ok')
	            return;
            $("#band_select").val(jsn.band);
            $("#band_select").trigger("chosen:updated");
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function call_enter_key_press() {
	/*update_rst_r();
	update_rst_t();
	update_date_on();
	$.ajax({
		url: '/api/setdxccandaddqso/',
		type: 'POST',
		data: $("#id_qsoaddform").serialize(),
		success: function(jsn) {
			console.log("Set Dxcc and add QSO with: " + $("#id_callsign").val().trim());
			init_form(jsn.content.init_form);
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});*/
}

$(document).ready(function() {
    $("#mode_select").chosen()
    $("#band_select").chosen({width: "95%"})
    $("#dxcc_select").chosen({allow_single_deselect: true})

    $("#call_input").keypress(function(e) {
		if (e.keyCode == 13) e.preventDefault();
	});
	$("#call_input").keyup(function(e) {
		if (e.keyCode == 13) call_enter_key_press(); //enter
		else if (e.keyCode == 32) {					 //space
			$("#srx_string_input").focus();
		}
	});
	$("#call_input").keydown(function(e) {
		if (e.keyCode == 32) e.preventDefault();
	});
	$("#call_input").change(call_change);

    $("#date_on_button").click(update_date_on);
	$("#date_on_date").blur(function() {
		if ($("#date_on_date").val().length == 0) update_date_on();
	});
	$("#date_on_time").blur(function() {
		if ($("#date_on_time").val().length == 0) update_date_on();
	});

	/*$("#id_srx").keypress(function(e) {
		if (e.keyCode == 13) e.preventDefault();
	});
	$("#id_srx").keyup(function(e) {
		if (e.keyCode == 13) call_enter_key_press();
	});*/

	$("#freq_input").change(freq_change);
});
