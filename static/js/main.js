function show_model(url) {
    $.post(
        url,
        show_model_data
    );
}

function change_field(field, model_name) {
    $.ajax(
    {
        url: '/change_field/' + model_name + '/',
        type: 'POST',
        data : {'field_name_id': field.name, 'new_value': field.value },
        success:function(data, textStatus, jqXHR)
        {
            if (!data.success) {
                alert(data.msg);
            }
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            console.log('error');
            console.log(jqXHR);
        }
    });
}

function get_field_class(field_type) {
    var field_class = 'none';
    switch (field_type)
        {
            case 'CharField':
                field_class = 'char';
                break;
            case 'IntegerField':
                field_class = 'int';
                break;
            case 'DateField':
                field_class = 'date';
                break
        }
    return field_class;
}

function submit_form() {
    var postData = $('#form').serializeArray();
    var formURL = $('#form').attr("action");
    $.ajax(
    {
        url: formURL,
        type: "POST",
        data : postData,
        success:function(data, textStatus, jqXHR)
        {
            if (!data.success) {
                alert(data.msg);
            }
            if (!data.model_name) return;
            show_model('/model_view/' + data.model_name + '/');
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            console.log('error');
        }
    });
    return false;
}

function show_model_data(data) {
    $('ul span').each(function(i) {
        if ($(this).attr('id') == data.model_name) $(this).addClass('selected');
        else $(this).removeClass('selected');
    });

    $('#content').empty();
    var td_head = '';
    for (var m = 0; m < data.meta.length; m++) {
        td_head += '<td>' + data.meta[m].field_title + '</td>';
    }
    var tr_records = '';
    for (var r = 0; r < data.records.length; r++) {
        var td_record = '';
        for (var m = 0; m < data.meta.length; m++) {
            td_record += '<td>';
            var field_class = get_field_class(data.meta[m].field_type);
            switch (data.meta[m].field_name)
            {
                case 'id':
                    td_record += data.records[r][data.meta[m].field_name];
                    break;
                default:
                    td_record += '<input class="' + field_class +
                                 '" name="' + data.meta[m].field_name + ',' +
                                 data.records[r]['id'] +'" value="' +
                                 data.records[r][data.meta[m].field_name] +
                                 '" type="text" onchange="change_field(this,\'' + data.model_name + '\');">';
                    break;
            }
            td_record += '</td>';
        }
        tr_records += '<tr>' + td_record + '</tr>'
    }
    $('#content').append('<table border=1><tr>' + td_head + '</tr>' + tr_records + '</table>');

    $('#add').empty();
    $('#add').append('<h1>Новая запись "' + data.model_title + '"</h1>');
    var form = '<form id="form" action="/add_record/' + data.model_name + '/" onsubmit="return submit_form();">';
    for (var m = 0; m < data.meta.length; m++) {
        if (data.meta[m].field_name == 'id') continue;
        var field_class = get_field_class(data.meta[m].field_type);
        form += '<p>' + data.meta[m].field_title + ': <input class="' + field_class +
                '" name="' + data.meta[m].field_name + '" value="" type="text"></p>';
    }
    form += '<input value="Добавить" type="submit">';
    $('#add').append(form);
    $('.date').datepicker({dateFormat: "yy-mm-dd"});
}
