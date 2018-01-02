function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function load_qso(id) {
    $('form#qso #qso_id').val(id);
    $.ajax({
    type:'POST',
	url: '/api/get_qso',
	data: JSON.stringify({"id": id}),
	contentType: 'application/json; charset=utf-8',
	success: function(jsn) {
		if( jsn.status != 'ok') {
            return;
        }
        $.each(jsn.qso, function(i, item) {
            $("form#qso #qso_" + i).val(item);
        });
        if(jsn.qso.call)
            $("form#qso a#qso_qrz").attr("href", "https://www.qrz.com/db/" + jsn.qso.call)
        if(jsn.qso.datetime_on) {
            var d=new Date(jsn.qso.datetime_on);
	        $("form#qso #qso_date_on").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	        $("form#qso #qso_time_on").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
	    }

	    $("form#qso #qso_profile").trigger("change");
	},
	error: function(jqXHR, textStatus, errorThrown) {
   		alert( "Bad request: " + jqXHR.responseText);
   	},
	});
}

function close_qso() {
    $('#qso_modal').hide();
    $(document).off('keyup');
    $('form#qso #qso_opennewwindow_button').off('click');
    $('form#qso #qso_cancel_button').off('click');
}

function open_qso(id) {
    $('#qso_modal').show();
    $('form#qso #qso_cancel_button').click(close_qso);
    $('form#qso #qso_opennewwindow_button').click(function() {
        window.open("/qso/" + id);
        close_qso();
    });
    $(document).keyup(function(e) {
		if (e.keyCode == 27) {
		    close_qso();
		}
	});
	load_qso(id);
}

$(document).ready(function() {
    $("form#qso #qso_profile").change(function() {
        $("form#qso #qso_gridsquare_info").val($("form#qso #qso_profile").find(':selected').data('gridsquare'));
        $("form#qso #qso_call_info").val($("form#qso #qso_profile").find(':selected').data('call'));
        $("form#qso #qso_gridsquare").trigger("change");
    });

    $("form#qso #qso_gridsquare_info").val($("form#qso #qso_profile").find(':selected').data('gridsquare'));
    $("form#qso #qso_call_info").val($("form#qso #qso_profile").find(':selected').data('call'));

    $("form#qso #qso_gridsquare").change(function() {
        if($("form#qso #qso_gridsquare").val().trim() == '') {
            $("form#qso #qso_loc_info").val("-- km, -- °");
        }
        else if ($("form#qso #qso_gridsquare_info").val().trim() != '') {
		    var tmp = calcdisazi($("form#qso #qso_gridsquare_info").val().trim(), $("form#qso #qso_gridsquare").val().trim());
		    $("form#qso #qso_loc_info").val(" " + tmp.dis + "km, " + tmp.az + "°");
		}
	});

    $('form#qso #qso_update_button').click(function() {
        var obj = {}
        if($("form#qso #qso_date_on").val().trim() != "" && $("form#qso #qso_time_on").val().trim() != "")
            obj["datetime_on"] = $("form#qso #qso_date_on").val().trim() + 'T' +$("form#qso #qso_time_on").val().trim();
        obj["comment"] = $("form#qso #qso_comment").val().trim();

        $('form#qso input[type=text]').each(function() {
            this.id = this.id.replace(/^qso_/,'');
            obj[this.id] = this.value.trim();
        });
        $('form#qso input[type=number]').each(function() {
            parfun = parseInt;
            id = this.id.replace(/^qso_/,'');
            if (id == 'freq' || id == 'freq_rx' || id == 'tx_pwr')
                parfun = parseFloat;
            if(parfun(this.value.trim()) >= 0)
                obj[id] = parfun(this.value.trim());
            else
                obj[id] = null;
        });
        $('form#qso input[type=hidden]').each(function() {
            id = this.id.replace(/^qso_/,'');
            if(parseInt(this.value.trim()) >= 0)
                obj[id] = parseInt(this.value.trim());
            else
                obj[id] = null;
        });
        $('form#qso select').each(function() {
            id = this.id.replace(/^qso_/,'');
            if (id == 'cont' && this.value.trim() != '')
                obj[id] = this.value.trim();
            else {
                if(parseInt(this.value.trim()) >= 0)
                    obj[id] = parseInt(this.value.trim());
                else if (this.value.trim() != '')
                    obj[id] = this.value.trim();
                else
                     obj[id] = null;
            }
        });
        $.ajax({
            type:'POST',
            url: '/api/update_qso',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            success: function(jsn) {
                console.log("Update QSO: " + jsn.status);
                if( jsn.status != 'ok') {
                    return;
                }
                close_qso();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert( "Bad request: " + jqXHR.responseText);
            },
        });
    });
});
