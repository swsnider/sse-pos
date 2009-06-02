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
        if (data.valid){
            $('#tax_row').before(data.html);
            $('#total_row').replaceWith(data.total_row);
        }else{
            document.TextBoxMain.show_error();
        }
    });
}

function cancel_trans(){
    $.get('/api/transaction/cancel', function (data){
        data = eval('(' + data + ')');
        if (data.valid)
            location.reload();
        else
            alert("Server Error!");
    });
}

function finalize_trans(){
    $.get('/api/transaction/finalize_step_1', function (data){
        data = eval('(' + data + ')');
        if (data.valid){
            real_total = (data.total).toFixed(2) - 0;
            customer_total = window.prompt("The total is $" + (data.total).toFixed(2) + ". Please enter the amount received from the customer.");
            if (customer_total == null){
                return;
            }
            customer_total = (customer_total - 0);
            while (customer_total < data.total){
                new_total = window.prompt("The remaining total is $" + (data.total - customer_total).toFixed(2) + ". Please enter the rest of the amount received from teh customer.");
                if (new_total == null){
                    return;
                }
                if (new_total == '') continue;
                customer_total += (new_total - 0);
            }
            alert("Please give the customer a total of $" + (customer_total - data.total).toFixed(2) + " in change.");
            $.post('/api/transaction/finalize_step_2', {customer_total: customer_total}, function(data2){
                data2 = eval('(' + data2 + ')');
                if (data2.valid){
                    location.reload();
                }else if (data2.is_error){
                    alert("A server error occurred! Please try later!");
                }else{
                    alert(data.payload);
                }
            });
        }else if (data.is_error){
            alert("A server error occurred! Please try later!");
        }else{
            alert(data.payload);
        }
    });
}