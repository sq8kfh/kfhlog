from pyramid_rpc.xmlrpc import xmlrpc_method


@xmlrpc_method(method='log.get_record', endpoint='xmlrpc')
def log_get_record(request, call):
    uid = request.matchdict['uid']
    print('log.get_record', uid, call)
    return 'NO_RECORD'
    # return '<NAME:4>name<QTH:3>qth<STATE:5>state<VE_PROV:4>cnty<COUNTRY:9>dxcc name<GRIDSQUARE:6>KN19EV<NOTES:5>notes'


@xmlrpc_method(method='log.check_dup', endpoint='xmlrpc')
def log_check_dup(request, call, mode=None, time_span=None, freq_hz=None, state=None, xchg_in=None):
    uid = request.matchdict['uid']
    print('log.check_dup', uid, call, mode, time_span, freq_hz, state, xchg_in)
    return 'true'


@xmlrpc_method(method='log.add_record', endpoint='xmlrpc')
def log_add_record(request, adif_record):
    uid = request.matchdict['uid']
    print('log.add_record', adif_record, uid)
    return '-'


@xmlrpc_method(method='system.methodHelp', endpoint='xmlrpc')
def system_methodhelp(request, method):
    uid = request.matchdict['uid']
    print('system.methodHelp', method, uid)
    return '-'


@xmlrpc_method(method='system.listMethods', endpoint='xmlrpc')
def system_listmethods(request):
    uid = request.matchdict['uid']
    print('system.listMethods', uid)
    return ['system.listMethods', 'system.methodHelp', 'log.add_record', 'log.check_dup', 'log.get_record']
