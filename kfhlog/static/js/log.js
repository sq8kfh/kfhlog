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
                $('#log > tbody').append('<tr onclick="open_qso(' + item.id+ ')"><td>' + item.call + '</td><td>' + item.datetime_off + '</td><td>' + item.band_name + '</td><td>' + item.mode_name + '</td><td>' + item.rst_rcvd + '</td><td>' + item.rst_sent + '</td><td>' + item.dxcc_name + '</td></tr>');
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

    $('tr#headers span#' + sort_by + '_sort').addClass('icon-sort-alpha-desc');

    $("#sortby").val("-" + sort_by);
    $("#sortby").change();
}

$(document).ready(function() {
    changesort('datetime_off');
    $('#page').val(1);
    load_log();

    $('tr#filter input').each(function() {
        $(this).change(load_log);
    });
    $('tr#filter select').each(function() {
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
});
