function set_setting(name) {
    $.ajax({
        type:'POST',
        url: '/api/set_setting',
        data: JSON.stringify({"name": name, "value": $("#setting_value").val()}),
        contentType: 'application/json; charset=utf-8',
        success: function(jsn) {
            if( jsn.status != 'ok') {
                edit_setting(name);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert( "Bad request: " + jqXHR.responseText);
        },
    });
}

function edit_setting(name) {
    $.ajax({
        type:'POST',
        url: '/api/get_setting',
        data: JSON.stringify({"name": name}),
        contentType: 'application/json; charset=utf-8',
        success: function(jsn) {
            if( jsn.status != 'ok')
                return;
            $("#setting_name").text(jsn.name);
            $("#setting_value").val(jsn.value);
            $("#setting_desc").text(jsn.desc);
            $("#setting_value").off("change");
            $("#setting_value").on("change", function () {
                set_setting(name);
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert( "Bad request: " + jqXHR.responseText);
        },
    });
}
