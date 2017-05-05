function null_formatter(val) {
    if ( typeof(val) !== "undefined" && val !== null )
        return val;
    return '';
}

function load_log() {
    obj = {}
    /*if($("form#newqso #date_on").val().trim() != "" && $("form#newqso #time_on").val().trim() != "")
        obj["datetime_on"] = $("form#newqso #date_on").val().trim() + 'T' +$("form#newqso #time_on").val().trim();
    if($("form#newqso #comment").val().trim() != "")
        obj["comment"] = $("form#newqso #comment").val().trim();
    */
    $('tr#filters input[type=text]').each(function() {
        if(this.value.trim() != "")
            obj[this.id] = this.value.trim();
    });
    /*$('form#newqso input[type=number]').each(function() {
        parfun = parseInt;
        if (this.id == 'freq' || this.id == 'freq_rx' || this.id == 'tx_pwr')
            parfun = parseFloat;
        if(parfun(this.value.trim()) >= 0)
            obj[this.id] = parfun(this.value.trim());
    });
    $('form#newqso input[type=hidden]').each(function() {
        if(parseInt(this.value.trim()) >= 0)
            obj[this.id] = parseInt(this.value.trim());
    });*/
    $('tr#filters select').each(function() {
        if (this.id == 'cont_filter' && this.value.trim() != '')
            obj[this.id] = this.value.trim();
        else {
            if(parseInt(this.value.trim()) >= 0)
                obj[this.id] = parseInt(this.value.trim());
        }
    });

    obj["sortby"] = $("#sortby").val();

    obj["pagesize"] = $('#pagesize').val();
    obj["page"] = $('#page').val();

    if(parseInt($("#profile").val().trim()) >= 0)
        obj["profile"] = parseInt($("#profile").val().trim());
    if(parseInt($("#group").val().trim()) >= 0)
        obj["group"] = parseInt($("#group").val().trim());

    $.ajax({
	    type:'POST',
		url: '/api/get_log',
		data: JSON.stringify(obj),
		contentType: 'application/json; charset=utf-8',
		success: function(jsn) {
			if( jsn.status != 'ok')
	            return;
	        $("#log > tbody").empty();
            $.each(jsn.log, function(i, item) {
                $('#log > tbody').append('<tr onclick="open_qso(' + item.id+ ')"><td>' +
                item.call + '</td><td>' +
                null_formatter(item.datetime_on).replace('T', ' ')  + '</td><td>' +
                null_formatter(item.datetime_off).replace('T', ' ') + '</td><td>' +
                item.band_name + '</td><td>' +
                item.mode_name + '</td><td>' +
                item.rst_rcvd + '</td><td>' +
                item.rst_sent + '</td><td>' +
                null_formatter(item.dxcc_name) + '</td><td>' +
                null_formatter(item.cont) + '</td><td>' +
                null_formatter(item.ituz) + '</td><td>' +
                null_formatter(item.cqz) + '</td></tr>');
            });
            $('#pagecount').val(jsn.pagecount);
            $('.showcolcheckbox').each(function() {
                var e = jQuery.Event('change');
                $(this).trigger(e, [false]);
            });
		},
		error: function(jqXHR, textStatus, errorThrown) {
      		alert( "Bad request: " + jqXHR.responseText);
    	},
	});
}

function changesort(sort_by) {
    $('tr#headers span').each(function() {
        $(this).removeClass('icon-sort-alpha-asc');
        $(this).removeClass('icon-sort-alpha-desc');
    });

    if ($("#sortby").val() == sort_by) {
        $('tr#headers span#' + sort_by + '_sort').addClass('icon-sort-alpha-desc');
        $("#sortby").val('-' + sort_by);
    }
    else {
        $('tr#headers span#' + sort_by + '_sort').addClass('icon-sort-alpha-asc');
        $("#sortby").val(sort_by);
    }
    $("#sortby").change();
}

function update_preset() {
    preset = {}
    preset['profile'] = parseInt($('#profile').val().trim());
    preset['group'] = parseInt($('#group').val().trim());
    preset['show_datetime_off'] = $('#show_datetime_off').is(':checked');
    preset['show_band'] = $('#show_band').is(':checked');
    preset['show_mode'] = $('#show_mode').is(':checked');
    preset['show_rst_rcvd'] = $('#show_rst_rcvd').is(':checked');
    preset['show_rst_send'] = $('#show_rst_send').is(':checked');
    preset['show_dxcc'] = $('#show_dxcc').is(':checked');
    preset['show_cont'] = $('#show_cont').is(':checked');
    preset['show_ituz'] = $('#show_ituz').is(':checked');
    preset['show_cqz'] = $('#show_cqz').is(':checked');
    $.ajax({
	    type:'POST',
		url: '/api/set_log_preset',
		data: JSON.stringify(preset),
		contentType: 'application/json; charset=utf-8',
	});
}

function profilegroup_change() {
    load_log();
    update_preset();
}

$(document).ready(function() {
    changesort('datetime_on');
    changesort('datetime_on');
    $('#page').val(1);

    $("#profile").change(profilegroup_change);
    $("#group").change(profilegroup_change);

    $('tr#filters input').each(function() {
        $(this).change(load_log);
    });
    $('tr#filters select').each(function() {
        $(this).change(load_log);
    });

    $("#sortby").change(load_log);

    $('#pagesize').change(load_log);
    $('#page').change(load_log);

    $('#first').click(function() {
        $('#page').val(1);
        $('#page').change();
    });
    $('#prev').click(function() {
        if (parseInt($('#page').val()) > 1) {
            $('#page').val(parseInt($('#page').val())-1);
            $('#page').change();
        }
    });
    $('#next').click(function() {
        $('#page').val(parseInt($('#page').val())+1);
        $('#page').change();
    });
    $('#last').click(function() {
        $('#page').val(parseInt($('#pagecount').val()));
        $('#page').change();
    });

    function make_show_checkbox(selector, col) {
        $(selector).change(function (event, up_preset = true) {
            if ($(selector).is(':checked')) {
                $('#log tr td:nth-child(' + col + ')').show();
                $('#log tr th:nth-child(' + col + ')').show();
            }
            else {
                $('#log tr td:nth-child(' + col + ')').hide();
                $('#log tr th:nth-child(' + col + ')').hide();
            }
            if(up_preset) update_preset();
        });
        $(selector).attr("checked", $(selector).is(':checked'));
    }

    make_show_checkbox("#show_datetime_off", 3);
    make_show_checkbox("#show_band", 4);
    make_show_checkbox("#show_mode", 5);
    make_show_checkbox("#show_rst_rcvd", 6);
    make_show_checkbox("#show_rst_send", 7);
    make_show_checkbox("#show_dxcc", 8);
    make_show_checkbox("#show_cont", 9);
    make_show_checkbox("#show_ituz", 10);
    make_show_checkbox("#show_cqz", 11);
    $('.showcolcheckbox').each(function() {
        var e = jQuery.Event('change');
        $(this).trigger(e, [false]);
    });

    load_log();
});
