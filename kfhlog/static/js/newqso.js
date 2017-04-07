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
		$('#previou_table > tbody').append('<tr onclick="open_qso(' + item[0]+ ')"><td>' + item[1] + '</td><td>' + item[2] + '</td><td>' + item[3] + '</td></tr>');
	});
}

function set_dxcc(data) {
    if( data.status != 'ok') {
        $("form#newqso #dxcc").val(null)
        $("form#newqso #dxcc").trigger("chosen:updated");
        $("form#newqso #cqz").val(null);
        $("form#newqso #ituz").val(null);
        $("form#newqso #cont").val(null);
        $("form#newqso #cont").trigger("chosen:updated");
	    return;
	}
    $("form#newqso #dxcc").val(data.dxcc);
    $("form#newqso #dxcc").trigger("chosen:updated");
    $("form#newqso #cqz").val(data.cqz);
    $("form#newqso #ituz").val(data.ituz);
    $("form#newqso #cont").val(data.cont);
    $("form#newqso #cont").trigger("chosen:updated");
}

function update_date_on() {
	var d=new Date();
	$("form#newqso #date_on").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	$("form#newqso #time_on").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
}

function call_change() {
    call = $("form#newqso #call").val().trim();
    if(!call) {
        $("#previou_table > tbody").empty();
        $("form#newqso a#qrz").attr("href", "https://www.qrz.com/db/");
		set_dxcc({"status": "error"});
        return;
    }
    $("form#newqso a#qrz").attr("href", "https://www.qrz.com/db/" + call)
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
    freq = parseFloat($("form#newqso #freq").val().trim());
    if(!freq) return;
    $.ajax({
	    type:'POST',
		url: '/api/get_band',
		data: JSON.stringify({"freq": freq}),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			if( jsn.status != 'ok')
	            return;
            $("form#newqso #band").val(jsn.band);
            $("form#newqso #band").trigger("chosen:updated");
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function state_change() {
    $("form#newqso #state_info").val(null)
    var dxcc = $("form#newqso #dxcc").val();
    var state = $("form#newqso #state").val().trim();
    if(dxcc > 0 && state != '') {
        $.ajax({
            type:'POST',
            url: '/api/get_state',
            data: JSON.stringify({"dxcc": dxcc, "state": state}),
            contentType: 'application/json; charset=utf-8',
            success: function(jsn) {
                if( jsn.status != 'ok')
                    return;
                $("form#newqso #state_info").val(jsn.state.name);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert( "Bad request: " + jqXHR.responseText);
            },
        });
	}
}

function form_to_json() {
    var obj = {};
    if($("form#newqso #date_on").val().trim() != "" && $("form#newqso #time_on").val().trim() != "")
        obj["datetime_on"] = $("form#newqso #date_on").val().trim() + 'T' +$("form#newqso #time_on").val().trim();
    if($("form#newqso #comment").val().trim() != "")
        obj["comment"] = $("form#newqso #comment").val().trim();

    $('form#newqso input[type=text]').each(function() {
        if(this.value.trim() != "")
            obj[this.id] = this.value.trim();
    });
    $('form#newqso input[type=number]').each(function() {
        parfun = parseInt;
        if (this.id == 'freq' || this.id == 'freq_rx' || this.id == 'tx_pwr')
            parfun = parseFloat;
        if(parfun(this.value.trim()) >= 0)
            obj[this.id] = parfun(this.value.trim());
    });
    $('form#newqso input[type=hidden]').each(function() {
        if(parseInt(this.value.trim()) >= 0)
            obj[this.id] = parseInt(this.value.trim());
    });
    $('form#newqso select').each(function() {
        if (this.id == 'cont' && this.value.trim() != '')
            obj[this.id] = this.value.trim();
        else {
            if(parseInt(this.value.trim()) >= 0)
                obj[this.id] = parseInt(this.value.trim());
        }
    });
    return JSON.stringify(obj);
}

function reset_form(preset = {}) {
    $('form#newqso input[type!=button]').each(function() {
        $(this).val(preset[this.id] ? preset[this.id] : null);
        $(this).removeClass("error");
    });
    $("form#newqso a#qrz").attr("href", "https://www.qrz.com/db/" + preset['call'] ? preset['call'] : '')
    if(preset['datetime_on']) {
        var d=new Date(preset['datetime_on']);
	    $("form#newqso #date_on").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	    $("form#newqso #time_on").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
    }
    $('form#newqso select').each(function() {
        if(this.id == 'profile' || this.id == 'group')
            $(this).val(preset[this.id] ? preset[this.id] : 0);
        else
            $(this).val(preset[this.id] ? preset[this.id] : null);
        $(this).removeClass("error");
        $(this).trigger("chosen:updated");
    });
    $("form#newqso #comment").val(preset['comment'] ? preset['comment'] : null);
    $("form#newqso #comment").removeClass("error");
    $("#previou_table > tbody").empty();
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
			        $('form#newqso #' + item).addClass('error');
			        //TODO show error on chosen don't work
			        //$('form#newqso #' + item).trigger("chosen:updated");
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
    $("form#newqso #mode").chosen({width: "140px", inherit_select_classes: true});
    $("form#newqso #band").chosen({width: "140px", inherit_select_classes: true});
    $("form#newqso #cont").chosen({width: "140px", allow_single_deselect: true, disable_search_threshold: 10});
    $("form#newqso #dxcc").chosen({width: "233px", allow_single_deselect: true});
    $("form#newqso #profile").chosen({width: "140px"});
    $("form#newqso #group").chosen({width: "140px"});

    $("form#newqso #call").keypress(function(e) {
		if (e.keyCode == 13) e.preventDefault();
	});
	$("form#newqso #call").keyup(function(e) {
		if (e.keyCode == 13) call_enter_key_press(); //enter
		else if (e.keyCode == 32) {					 //space
			$("form#newqso #rst_rcvd").focus();
		}
	});
	$("form#newqso #call").keydown(function(e) {
		if (e.keyCode == 32) e.preventDefault();
	});
	$("form#newqso #call").change(call_change);

    $("form#newqso #date_on_button").click(update_date_on);
	$("form#newqso #date_on").blur(function() {
		if ($("form#newqso #date_on").val().length == 0) update_date_on();
	});
	$("form#newqso #time_on").blur(function() {
		if ($("form#newqso #time_on").val().length == 0) update_date_on();
	});

    $("form#newqso #rst_rcvd").keyup(function(e) {
		if (e.keyCode == 32) $("form#newqso #srx_string").focus(); //space
	});
    $("form#newqso #rst_rcvd").keydown(function(e) {
		if (e.keyCode == 32) e.preventDefault();
	});

	$("form#newqso #srx_string").keypress(function(e) {
		if (e.keyCode == 13) e.preventDefault();
	});
	$("form#newqso #srx_string").keyup(function(e) {
		if (e.keyCode == 13) call_enter_key_press();
	});

    $("form#newqso #rst_rcvd_button").click(function() {
        $("form#newqso #rst_rcvd").val($("form#newqso #mode").find(':selected').data('def_rst'));
    });

    $("form#newqso #rst_sent_button").click(function() {
        $("form#newqso #rst_sent").val($("form#newqso #mode").find(':selected').data('def_rst'));
    });

	$("form#newqso #freq").change(freq_change);

    $("form#newqso #state").change(state_change);

    $("form#newqso #profile").change(function() {
        $("form#newqso #gridsquare_info").val($("form#newqso #profile").find(':selected').data('gridsquare'));
        $("form#newqso #gridsquare").trigger("change");
    });
    $("form#newqso #gridsquare_info").val($("form#newqso #profile").find(':selected').data('gridsquare'));

    $("form#newqso #gridsquare").change(function() {
        if($("form#newqso #gridsquare").val().trim() == '') {
            $("form#newqso #loc_info").val("-- km, -- °");
        }
        else if ($("form#newqso #gridsquare_info").val().trim() != '') {
		    var tmp = calcdisazi($("form#newqso #gridsquare_info").val().trim(), $("form#newqso #gridsquare").val().trim());
		    $("form#newqso #loc_info").val(" " + tmp.dis + "km, " + tmp.az + "°");
		}
	});

	$("form#newqso #add_button").click(qso_add);
	$("form#newqso #updatetimeandadd_button").click(update_time_and_add_qso);
});
