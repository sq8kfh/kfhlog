function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function load_qso(id) {
    $('form#qso #id').val(id);
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
            $("form#qso #" + i).val(item);
        });
        if(jsn.qso.call)
            $("form#qso a#qrz").attr("href", "https://www.qrz.com/db/" + jsn.qso.call)
        if(jsn.qso.datetime_on) {
            var d=new Date(jsn.qso.datetime_on);
	        $("form#qso #date_on").val(d.getUTCFullYear() + '-' + pad(1+d.getUTCMonth(),2) + '-' + pad(d.getUTCDate(),2));
	        $("form#qso #time_on").val(pad(d.getUTCHours(),2) + ':' + pad(d.getUTCMinutes(),2) + ':' +pad(d.getUTCSeconds(),2));
	    }
	},
	error: function(jqXHR, textStatus, errorThrown) {
   		alert( "Bad request: " + jqXHR.responseText);
   	},
	});
}

function close_qso() {
    $('#qso_modal').hide();
    $(document).off('keyup');
    $('form#qso #opennewwindow_button').off('click');
    $('form#qso #cancel_button').off('click');
}

function open_qso(id) {
    $('#qso_modal').show();
    $('form#qso #cancel_button').click(close_qso);
    $('form#qso #opennewwindow_button').click(function() {
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
    $('form#qso #update_button').click(function() {
        var obj = {}
        if($("form#qso #date_on").val().trim() != "" && $("form#qso #time_on").val().trim() != "")
            obj["datetime_on"] = $("form#qso #date_on").val().trim() + 'T' +$("form#qso #time_on").val().trim();
        obj["comment"] = $("form#qso #comment").val().trim();

        $('form#qso input[type=text]').each(function() {
            obj[this.id] = this.value.trim();
        });
        $('form#qso input[type=number]').each(function() {
            parfun = parseInt;
            if (this.id == 'freq' || this.id == 'freq_rx' || this.id == 'tx_pwr')
                parfun = parseFloat;
            if(parfun(this.value.trim()) >= 0)
                obj[this.id] = parfun(this.value.trim());
            else
                obj[this.id] = null;
        });
        $('form#qso input[type=hidden]').each(function() {
            if(parseInt(this.value.trim()) >= 0)
                obj[this.id] = parseInt(this.value.trim());
            else
                obj[this.id] = null;
        });
        $('form#qso select').each(function() {
            if (this.id == 'cont' && this.value.trim() != '')
                obj[this.id] = this.value.trim();
            else {
                if(parseInt(this.value.trim()) >= 0)
                    obj[this.id] = parseInt(this.value.trim());
                else
                    obj[this.id] = null;
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
