from .campus import CampusCard


def get_token(phone, password, device_seed):
    stuobj = CampusCard(phone, password, device_seed).user_info
    if stuobj['login']:
        return stuobj["sessionId"]
    return None