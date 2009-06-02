function delete_category(key){
    $('<div id="dialog" title="Confirm delete"><p>Do you really want to delete this category?</p></div>').dialog({modal: true, buttons: {"No": function (){
        $(this).dialog("close");
    },"Yes": function(){
        $.post('/api/category/delete', {key: key}, function(data){
            data = eval('(' + data + ')');
            if (data.valid){
               $("#" + key).remove();
            }
        });
        $(this).dialog("close");
    }}
});
}

function add_category(){
    $.post('/api/category/new_blank', function(data){
        data = eval('('+ data +')');
        if (data.valid){
            $('#add_new').before(data.html);
        }
    });
}

function commit_row(key){
    description = $('#'+key+'description').val();
    price = $('#'+key+'price').val();
    code = $('#'+key+'code').val();
    $.post('/api/category/update', {key: key, description: description, price: price, code: code}, function(data){
        data = eval('('+ data +')');
        if (data.valid){
            $('#'+key+'row').replaceWith(data.html)
        }
    });
}

function edit_row(key){
    $.get('/api/category/edit', {key: key}, function(data){
        data = eval('('+ data +')');
        if (data.valid){
            $('#'+key).replaceWith(data.html)
        }
    });
}