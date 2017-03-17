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
    if( data.status != 'ok') {
        $("#dxcc").val(null)
        $("#dxcc").trigger("chosen:updated");
        $("#cqz").val(null);
        $("#ituz").val(null);
	    return;
	    }
    $("#dxcc").val(data.dxcc);
    $("#dxcc").trigger("chosen:updated");
    $("#cqz").val(data.cqz);
    $("#ituz").val(data.ituz);
}

function update_date_on() {
	var d=new Date();
	$("#date_on").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	$("#time_on").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
}

function call_change() {
    call = $("#call").val().trim();
    if(!call) {
        $("#previou_table > tbody").empty();
        return;
    }
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
    freq = parseFloat($("#freq").val().trim());
    if(!freq) return;
    $.ajax({
	    type:'POST',
		url: '/api/get_band',
		data: JSON.stringify({"freq": freq}),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			if( jsn.status != 'ok')
	            return;
            $("#band").val(jsn.band);
            $("#band").trigger("chosen:updated");
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function form_to_json() {
    var obj = {};
    if(parseInt($("#profile").val().trim()) >= 0)
        obj["profile"] = parseInt($("#profile").val().trim());
    if(parseInt($("#group").val().trim()) >= 0)
        obj["group"] = parseInt($("#group").val().trim());
    if($("#call").val().trim() != "")
        obj["call"] = $("#call").val().trim();
    if($("#date_on").val().trim() != "" && $("#time_on").val().trim() != "")
        obj["datetime_on"] = $("#date_on").val().trim() + 'T' +$("#time_on").val().trim();
    if($("#rst_sent").val().trim() != "")
        obj["rst_sent"] = $("#rst_sent").val().trim();
    if($("#stx_string").val().trim() != "")
        obj["stx_string"] = $("#stx_string").val().trim();
    if($("#rst_rcvd").val().trim() != "")
        obj["rst_rcvd"] = $("#rst_rcvd").val().trim();
    if($("#srx_string").val().trim() != "")
        obj["srx_string"] = $("#srx_string").val().trim();
    if($("#gridsquare").val().trim() != "")
        obj["gridsquare"] = $("#gridsquare").val().trim();
    if(parseInt($("#dxcc").val().trim()))
        obj["dxcc"] = parseInt($("#dxcc").val().trim());
    if($("#name").val().trim() != "")
        obj["name"] = $("#name").val().trim();
    if($("#qth").val().trim() != "")
        obj["qth"] = $("#qth").val().trim();
    if($("#comment").val().trim() != "")
        obj["comment"] = $("#comment").val().trim();
    if(parseInt($("#mode").val().trim()))
        obj["mode"] = parseInt($("#mode").val().trim());
    if(parseInt($("#band").val().trim()))
        obj["band"] = parseInt($("#band").val().trim());
    if(parseFloat($("#freq").val().trim()))
        obj["freq"] = parseFloat($("#freq").val().trim());
    if($("#state").val().trim() != "")
        obj["state"] = $("#state").val().trim();
    if($("#cnty").val().trim() != "")
        obj["cnty"] = $("#cnty").val().trim();
    if(parseInt($("#cqz").val().trim()))
        obj["cqz"] = parseInt($("#cqz").val().trim());
    if(parseInt($("#ituz").val().trim()))
        obj["ituz"] = parseInt($("#ituz").val().trim());
    if($("#iota").val().trim() != "")
        obj["iota"] = $("#iota").val().trim();
    if($("#sota_ref").val().trim() != "")
        obj["sota_ref"] = $("#sota_ref").val().trim();
    if($("#qsl_via").val().trim() != "")
        obj["qsl_via"] = $("#qsl_via").val().trim();
    if(parseInt($("#profile").val().trim()))
        obj["profiles"] = parseInt($("#profile").val().trim());
    return JSON.stringify(obj);
}

function reset_form(preset = {}) {
    if(preset["profile"]) $("#profile").val(preset["profile"]);
    else $("#profile").val(0);
    $("#profile").removeClass("error")
    $("#profile").trigger("chosen:updated");
    if(preset["group"]) $("#group").val(preset["group"]);
    else $("#group").val(0);
    $("#group").removeClass("error")
    $("#group").trigger("chosen:updated");
    if(preset["call"]) $("#call").val(preset["call"]);
    else $("#call").val(null)
    $("#call").removeClass("error")
    if(preset["datetime_on"]) {
	    var d=new Date(preset["datetime_on"]);
	    $("#date_on").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	    $("#time_on").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
    }
    else {
        $("#date_on").val(null);
        $("#time_on").val(null);
    }
    $("#date_on").removeClass("error")
    $("#time_on").removeClass("error")
    if(preset["rst_sent"]) $("#rst_sent").val(preset["rst_sent"]);
    else $("#rst_sent").val(null);
    $("#rst_sent").removeClass("error")
    if(preset["stx_string"]) $("#stx_string").val(preset["stx_string"]);
    else $("#stx_string").val(null);
    $("#stx_string").removeClass("error")
    if(preset["rst_rcvd"]) $("#rst_rcvd").val(preset["rst_rcvd"]);
    else $("#rst_rcvd").val(null);
    $("#rst_rcvd").removeClass("error")
    if(preset["srx_string"]) $("#srx_string").val(preset["srx_string"]);
    else $("#srx_string").val(null);
    $("#srx_string").removeClass("error")
    if(preset["gridsquare"]) $("#gridsquare").val(preset["gridsquare"]);
    else $("#gridsquare").val(null);
    $("#gridsquare").removeClass("error")
    if(preset["dxcc"]) $("#dxcc").val(preset["dxcc"]);
    else $("#dxcc").val(null);
    $("#dxcc").removeClass("error")
    $("#dxcc").trigger("chosen:updated");
    if(preset["name"]) $("#name").val(preset["name"]);
    else $("#name").val(null);
    $("#name").removeClass("error")
    if(preset["qth"]) $("#qth").val(preset["qth"]);
    else $("#qth").val(null);
    $("#qth").removeClass("error")
    if(preset["comment"]) $("#comment").val(preset["comment"]);
    else $("#comment").val(null);
    $("#comment").removeClass("error")
    if(preset["mode"]) $("#mode").val(preset["mode"]);
    else $("#mode").val(null);
    $("#mode").removeClass("error")
    $("#mode").trigger("chosen:updated");
    if(preset["band"]) $("#band").val(preset["band"]);
    else $("#band").val(null);
    $("#band").removeClass("error")
    $("#band").trigger("chosen:updated");
    if(preset["freq"]) $("#freq").val(preset["freq"]);
    else $("#freq").val(null);
    $("#freq").removeClass("error")
    if(preset["state"]) $("#state").val(preset["state"]);
    else $("#state").val(null);
    $("#state").removeClass("error")
    if(preset["cnty"]) $("#cnty").val(preset["cnty"]);
    else $("#cnty").val(null);
    $("#cnty").removeClass("error")
    if(preset["cqz"]) $("#cqz").val(preset["cqz"]);
    else $("#cqz").val(null);
    $("#cqz").removeClass("error")
    if(preset["ituz"]) $("#ituz").val(preset["ituz"]);
    else $("#ituz").val(null);
    $("#ituz").removeClass("error")
    if(preset["iota"]) $("#iota").val(preset["iota"]);
    else $("#iota").val(null);
    $("#iota").removeClass("error")
    if(preset["sota_ref"]) $("#sota_ref").val(preset["sota_ref"]);
    else $("#sota_ref").val(null);
    $("#sota_ref").removeClass("error")
    if(preset["qsl_via"]) $("#qsl_via").val(preset["qsl_via"]);
    else $("#qsl_via").val(null);
    $("#qsl_via").removeClass("error")
}

function qso_add(set_dxcc=false) {
	$.ajax({
	    type:'POST',
		url: '/api/addqso',
		data: form_to_json(),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
		    console.log("Add QSO: " + jsn.status);
			if( jsn.status != 'ok') {
			    $.each(jsn.wrong_values, function(i, item) {
			        $('#' + item).addClass('error');
			    });
	            return;
	        }
	        reset_form(jsn.preset);
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function update_time_and_add_qso() {
	update_date_on();
	qso_add();
}

function call_enter_key_press() {
	update_date_on();
	qso_add(true);
}

$(document).ready(function() {
    $("#mode").chosen({width: "140px"})
    $("#band").chosen({width: "140px"})
    $("#dxcc").chosen({width: "233px", allow_single_deselect: true})
    $("#profile").chosen({width: "140px"})
    $("#group").chosen({width: "140px"})

    $("#call").keypress(function(e) {
		if (e.keyCode == 13) e.preventDefault();
	});
	$("#call").keyup(function(e) {
		if (e.keyCode == 13) call_enter_key_press(); //enter
		else if (e.keyCode == 32) {					 //space
			$("#rst_rcvd").focus();
		}
	});
	$("#call").keydown(function(e) {
		if (e.keyCode == 32) e.preventDefault();
	});
	$("#call").change(call_change);

    $("#date_on_button").click(update_date_on);
	$("#date_on").blur(function() {
		if ($("#date_on").val().length == 0) update_date_on();
	});
	$("#time_on").blur(function() {
		if ($("#time_on").val().length == 0) update_date_on();
	});

    $("#rst_rcvd").keyup(function(e) {
		if (e.keyCode == 32) $("#srx_string").focus(); //space
	});
    $("#rst_rcvd").keydown(function(e) {
		if (e.keyCode == 32) e.preventDefault();
	});

	$("#srx_string").keypress(function(e) {
		if (e.keyCode == 13) e.preventDefault();
	});
	$("#srx_string").keyup(function(e) {
		if (e.keyCode == 13) call_enter_key_press();
	});

	$("#freq").change(freq_change);

	$("#add_button").click(qso_add);
	$("#updatetimeandadd_button").click(update_time_and_add_qso);
});
