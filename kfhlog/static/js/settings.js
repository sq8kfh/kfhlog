function set_setting(inp, name) {
    $.ajax({
        type:'POST',
        url: '/api/set_setting',
        data: JSON.stringify({"name": name, "value": inp.value}),
        contentType: 'application/json; charset=utf-8',
        success: function(jsn) {
            if( jsn.status != 'ok') {
                get_setting(name);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert( "Bad request: " + jqXHR.responseText);
        },
    });
}

function get_setting(inp, name) {
    $.ajax({
        type:'POST',
        url: '/api/get_setting',
        data: JSON.stringify({"name": name}),
        contentType: 'application/json; charset=utf-8',
        success: function(jsn) {
            if( jsn.status != 'ok')
                return;
            inp.value = jsn.value;
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
    case 'profilestab':
        show_award('general')
        break;
    case 'groupstab':
        show_award('dxcc')
        break;
    case 'configtab':
        show_award('cq')
        break;
    }
}

$(document).ready(function() {
    open_tab('profilestab');
});
