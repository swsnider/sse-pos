def add_routes(map):
    map.connect('/',controller="controllers:GenericPages", action="index")
    map.connect('/receipt', controller="controllers:TransactionPage", action="receipt")
    map.connect("/pricelist", controller="controllers:GenericPages", action="pricelist")
    map.connect('/login',controller="controllers:GenericPages", action="login")
    map.connect('/do_login',controller="controllers:GenericPages", action="do_login")
    map.connect('/user_name',controller="controllers:GenericPages", action="user_name")
    map.connect('/logout',controller="controllers:GenericPages", action="logout")
    map.connect('/logout_pred',controller="controllers:GenericPages", action="logout_pred")
    map.connect('/transaction/:action', controller="controllers:TransactionPage", action="index")
    map.connect('/api/transaction/:action', controller="controllers:TransactionAPI")
    map.connect('/api/color/:action', controller="controllers:ColorAPI")
    map.connect('/api/category/:action', controller="controllers:CategoryAPI")
    map.connect('/api/user/:action', controller="controllers:UserAPI")
    map.connect('/denied', controller="controllers:GenericPages", action="denied")
    map.connect('/pos/:action', controller="controllers:PosPage", action="index")