function delete_color(key){
    $('<div id="dialog" title="Confirm delete"><p>Do you really want to delete this color?</p></div>').dialog({modal: true, buttons: {"No": function (){
        $(this).dialog("close");
    },"Yes": function(){
        $.post('/api/color/delete', {key: key}, function(data){
            data = eval('(' + data + ')');
            if (data.valid){
               $("#" + key).remove();
            }
        });
        $(this).dialog("close");
    }}
});
}

function add_color(){
    $.post('/api/color/new_blank', function(data){
        data = eval('('+ data +')');
        if (data.valid){
            $('#add_new').before(data.html);
        }
    });
}

function commit_row(key){
    color = $('#'+key+'color').val();
    discount = $('#'+key+'discount').val();
    code = $('#'+key+'code').val();
    $.post('/api/color/update', {key: key, color: color, discount: discount, code: code}, function(data){
        data = eval('('+ data +')');
        if (data.valid){
            $('#'+key+'row').replaceWith(data.html)
        }
    });
}

function edit_row(key){
    $.get('/api/color/edit', {key: key}, function(data){
        data = eval('('+ data +')');
        if (data.valid){
            $('#'+key).replaceWith(data.html)
        }
    });
}