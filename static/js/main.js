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