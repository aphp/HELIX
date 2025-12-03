from oauthenticator.generic import GenericOAuthenticator
import os

if os.environ.get("OIDC_ENABLED", "false").lower() == "true":
    c.JupyterHub.authenticator_class = "generic-oauth"

c.JupyterHub.default_url = os.environ.get("JHUB_DEFAULT_URL", "/hub")

# OAuth2 application info
# -----------------------
c.GenericOAuthenticator.auto_login = True
c.GenericOAuthenticator.client_id = os.environ.get("OIDC_CLIENT_ID", "NOT_DEFINED")
c.GenericOAuthenticator.client_secret = os.environ.get(
    "OIDC_CLIENT_SECRET", "NOT_DEFINED"
)

# Identity provider info
# ----------------------
c.GenericOAuthenticator.authorize_url = os.environ.get(
    "OIDC_AUTHORIZE_URL", "NOT_DEFINED"
)
c.GenericOAuthenticator.token_url = os.environ.get("OIDC_TOKEN_URL", "NOT_DEFINED")
c.GenericOAuthenticator.oauth_callback_url = os.environ.get("OIDC_CALLBACK_URL", "NOT_DEFINED")


# What we request about the user
# ------------------------------
# scope represents requested information about the user, and since we configure
# this against an OIDC based identity provider, we should request "openid" at
# least.
#
#
c.GenericOAuthenticator.scope = os.environ.get("OIDC_REQUESTED_SCOPES", "openid").split(
    ", "
)
c.GenericOAuthenticator.username_claim = lambda userinfo: userinfo[
    os.environ.get("OIDC_USERNAME_CLAIM", "preferred_username")
].replace(" ", "-")
c.GenericOAuthenticator.auth_state_groups_key = lambda auth_state: auth_state[
    "oauth_user"
][os.environ.get("OIDC_CLAIM_GROUPS_KEY", "NOT_DEFINED")]

# Authorization
# -------------
c.GenericOAuthenticator.userdata_from_id_token = True
c.GenericOAuthenticator.manage_groups = True
c.GenericOAuthenticator.allowed_users = os.environ.get(
    "PROJECT", "collaboration"
).split(", ")
c.GenericOAuthenticator.allowed_groups = os.environ.get(
    "OIDC_ALLOWED_GROUPS", "NOT_DEFINED"
).split(", ")
c.GenericOAuthenticator.admin_groups = os.environ.get(
    "OIDC_ADMIN_GROUPS", "NOT_DEFINED"
).split(", ")

# Security
# --------
c.GenericOAuthenticator.validate_server_cert = True
c.GenericOAuthenticator.enable_pkce = True
