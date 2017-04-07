from pyramid.authentication import AuthTktCookieHelper
from pyramid.security import (
    Authenticated,
    ACLAllowed,
    ACLDenied,
    Allow,
    Deny,
    Everyone,
    )
from .models import User


class KFHLogACLAuthorizationPolicy(object):
    acl = [
        (Allow, Authenticated, 'authenticated'),
    ]

    def permits(self, context, principals, permission):
        print('KFHLogACLAuthorizationPolicy.permits()', principals)
        for ace in self.acl:
            ace_action, ace_principal, ace_permissions = ace
            if ace_principal in principals:
                if permission in ace_permissions:
                    if ace_action == Allow:
                        return ACLAllowed(ace, self.acl, permission, principals, context)
                    else:
                        return ACLDenied(ace, self.acl, permission, principals, context)
        return ACLDenied('<default deny>', self.acl, permission, principals, context)

    def principals_allowed_by_permission(self, context, permission):
        raise NotImplementedError


class KFHLogAuthenticationPolicy(object):
    def __init__(self, secret):
        self.cookie = AuthTktCookieHelper(
            secret,
            cookie_name='auth_tkt',
            secure=False,
            include_ip=False,
            timeout=None,
            reissue_time=None,
            max_age=None,
            hashalg='sha512'
        )

    def unauthenticated_userid(self, request):
        result = self.cookie.identify(request)
        if result:
            return result['userid']

    def remember(self, request, userid, **kw):
        return self.cookie.remember(request, userid, **kw)

    def forget(self, request):
        return self.cookie.forget(request)

    def authenticated_userid(self, request):
        user = request.user
        if user:
            return user.name

    def effective_principals(self, request):
        principals = [Everyone]
        userid = self.authenticated_userid(request)
        if userid:
            principals.append(Authenticated)
            principals.append(userid)
        return principals


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user
    return None


def includeme(config):
    settings = config.get_settings()
    authn_policy = KFHLogAuthenticationPolicy(settings['auth.secret'])
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(KFHLogACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
