from bitcoinrpc.authproxy import AuthServiceProxy

from app.config import get_settings


def get_rpc_client() -> AuthServiceProxy:
    settings = get_settings()
    url = settings.bitcoin_rpc_url.replace("http://", "")
    rpc_url = f"http://{settings.bitcoin_rpc_user}:{settings.bitcoin_rpc_password}@{url}"
    return AuthServiceProxy(rpc_url, timeout=120)
