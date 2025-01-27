# Import

from GoPhishConnector import gp_connect, gp_delete_campaign


def del_gp():
    gp_api = gp_connect()
    gp_delete_campaign(gp_api)


if __name__ == "__main__":
    del_gp()
