from mojang import API

api = API()


def get_skin(ign):
    try:
        uuid = api.get_uuid(ign)
    except:
        return [0,0]

    if not uuid:
        return [0,0]
    else:
        profile = api.get_profile(uuid)
        return [profile.skin_url, profile.skin_variant]
