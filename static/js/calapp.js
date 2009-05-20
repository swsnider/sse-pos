function checkForName(){
    var name = $("#name").val();
    $("#loader").show();
    $.get("/getNameJSON/" + name, 
        function(data, textStatus){
            data = eval('(' + data + ')');
            if (data.valid){
                $("#email").val(data.email)
                if (data.senior){
                    $("#senior").attr("checked", "checked")
                }else{
                    $("#senior").removeAttr("checked")
                }
                if (data.contacts != ''){
                    $("#addContact").before(data.contacts);
                }
            }
            $("#loader").hide();
        }, 'json'
    );
}

function newGuid()
{
   var guid = "";
   for (var i = 0; i < 32; i++)
      guid += Math.floor(Math.random() * 0xF).toString(0xF) + (i == 7 || i == 11 || i == 15 || i == 19 ? "-" : "")
   return guid;
}

function addRoutine(){
    var myGUID = newGuid();
    myGUID += "|routine";
    myGUID = '|' + myGUID;
    $("#add_routine").before('<tr id="'+ myGUID +'"><td><input type="text" name="startDate'+ myGUID +'" class="date-pick" /></td><td><select name="dayOfWeek'+ myGUID +'"><option value="None" selected="selected">Select</option><option value="monday">Monday</option><option value="tuesday">Tuesday</option><option value="monday">Wednesday</option><option value="monday">Thursday</option><option value="monday">Friday</option><option value="monday">Saturday</option></select></td><td><input type="text" name="start_time'+ myGUID +'" /></td><td><select name="start_pm'+ myGUID +'"><option value="am" selected="selected">am</option><option value="pm">pm</option></select></td><td><input type="text" name="end_time'+ myGUID +'" /></td><td><select name="end_pm'+ myGUID +'"><option value="am" selected="selected">am</option><option value="pm">pm</option></select></td><td><textarea name="notes'+ myGUID +'"></textarea></td><td><a style="color: red" href="#" onclick="deleteRow(\''+ myGUID +'\');">X</a></tr>');
    $('.date-pick').datePicker({clickInput:true});
}

function addExceptional(){
    var myGUID = newGuid();
    myGUID += "|exceptional";
    myGUID = '|' + myGUID;
    $("#add_exceptional").before('<tr id="'+ myGUID +'"><td><input type="text" name="date'+ myGUID +'" class="date-pick" /></td><td><input type="text" name="start_time'+ myGUID +'" /></td><td><select name="start_pm'+ myGUID +'"><option value="am" selected="selected">am</option><option value="pm">pm</option></select></td><td><input type="text" name="end_time'+ myGUID +'" /></td><td><select name="end_pm'+ myGUID +'"><option value="am" selected="selected">am</option><option value="pm">pm</option></select></td><td><a style="color: red" href="#" onclick="deleteRow(\''+ myGUID +'\');">X</a></tr>');
    $('.date-pick').datePicker({clickInput:true});
}

function addContact(){
    var myGUID = newGuid();
    myGUID += "|contact";
    myGUID = '|' + myGUID;
    $("#addContact").before('<tr id="'+ myGUID +'"><td><strong><label for="type'+ myGUID +'">Type of contact: </label></strong><input type="text" name="type'+ myGUID +'" /></td><td><strong><label for="value'+ myGUID +'">Contact info: </label></strong><input type="text" name="value'+ myGUID +'" /><td><a style="color:red" href="#" onclick="deleteRow(\''+ myGUID +'\');">X</a></tr>');
}

function deleteRow(guid){
    $("#"+ guid).remove();
}