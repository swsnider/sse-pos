function enable_cache(){
if (!window.google || !google.gears) {
    return;
  }else{
var localServer = google.gears.factory.create('beta.localserver');
var store = localServer.createManagedStore('sse-pos-store');
store.manifestUrl = '/static/gears/manifest.json';
store.checkForUpdate();
}
}

function destroy_cache(){
    if (!window.google || !google.gears) {
    return;
  }else{
var localServer = google.gears.factory.create('beta.localserver');
var store = localServer.removeManagedStore('sse-pos-store');
window.location.reload();
}
}

function process_donation(){
    amt = prompt('Enter the amount of the donation');
    $.get('/donation/add', {amt: amt}, function (data){
        data = eval('(' + data + ')');
        if (data.valid)
            alert("Donation entered.");
        else
            alert("Server Error!");
    });
}
CONST_VERSION = 3;
