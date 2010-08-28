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

function show_prices(key){
    $.get("/pricelist", function(data){
        $(data).dialog();
    });
}


CONST_VERSION = 8;
