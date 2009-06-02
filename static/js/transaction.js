function enter_item(){
    var item = $('#item_id').value();
    alert(item);
    return false;
}
function process_input(some_input){
    $('#spinner').show();
    $.post("/api/transaction/add_item", {data: some_input}, function(data){
        $('#spinner').hide();
        data = eval('(' + data + ')');
        if (data.valid == 'true'){
            $('#tax_row').before(data.html);
            $('#total_row').replaceWith(data.total_row);
        }else{
            document.TextBoxMain.show_error();
        }
    });
}