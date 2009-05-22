def add_routes(map):
    map.connect('/',controller="controllers:MainPage")
    map.connect('/login',controller="controllers:LoginPage")
    map.connect('/logout',controller="controllers:LogoutPage")
    map.connect('/new',controller="controllers:InsertPage")
    map.connect('/dump', controller="controllers:DumpPage")