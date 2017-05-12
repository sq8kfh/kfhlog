def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=00)

    config.add_xmlrpc_endpoint('xmlrpc', '/xmlrpc/{uid:[0-9]+}', request_method='POST')

    config.add_route('api', '/api/{api_func}', request_method='POST')
    config.add_route('mapi', '/api', request_method='POST')
    config.add_route('qso', '/qso/{qsoid:[0-9]+}')

    config.add_route('checkwp', '/check/{profile:[0-9]+}')
    config.add_route('check', '/check')
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('newqso', '/newqso')
    config.add_route('log', '/log')
    config.add_route('map', '/map')
    config.add_route('awards', '/awards')
    config.add_route('import', '/import')
    config.add_route('export', '/export')
    config.add_route('about', '/about')
