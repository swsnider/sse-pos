function delete_color(key){
    $('<div id="dialog" title="Confirm delete"><p>Do you really want to delete this user?</p></div>').dialog({modal: true, buttons: {"No": function (){
        $(this).dialog("close");
    },"Yes": function(){
        $.post('/api/user/delete', {key: key}, function(data){
            data = eval('(' + data + ')');
            if (data.valid){
               $("#" + key).remove();
            }
        });
        $(this).dialog("close");
    }}
});
}