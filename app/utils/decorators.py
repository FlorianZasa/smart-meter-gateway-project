from functools import wraps
from flask import request, abort
import ipaddress
from config import Config

def lan_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = ipaddress.ip_address(request.remote_addr)
        if client_ip.is_loopback:
            # Allow access from loopback address
            return f(*args, **kwargs)
        lan_networks = get_lan_networks()
        if not any(client_ip in network for network in lan_networks):
            abort(403, description="Access denied from WAN")
        return f(*args, **kwargs)
    return decorated_function

def wan_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = ipaddress.ip_address(request.remote_addr)
        if client_ip.is_loopback:
            # Allow access from loopback address
            return f(*args, **kwargs)
        lan_networks = get_lan_networks()
        if any(client_ip in network for network in lan_networks):
            abort(403, description="Access denied from LAN")
        return f(*args, **kwargs)
    return decorated_function

def get_lan_networks():
    lan_ranges = Config.LAN_IP_RANGES
    return [ipaddress.ip_network(network.strip()) for network in lan_ranges.split(',')]