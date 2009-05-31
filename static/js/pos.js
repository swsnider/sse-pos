function enter_item(){
    var item = $('#item_id').value();
    alert(item);
    return false;
}

function process_input(some_input){
    $('#spinner').show();
    $.post("/api/add_item", {data: some_input}, function(data){
        $('#spinner').hide();
        if (data.valid){
            $('#tax_row').before(data);
        }else{
            document.TextBoxMain.showError();
        }
    });
}