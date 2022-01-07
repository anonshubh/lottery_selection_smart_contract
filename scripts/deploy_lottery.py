from brownie import Lottery,network,config
from .helpers import get_account, get_contract


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config['networks'][network.show_active()]["fee"],
        config['networks'][network.show_active()]["keyHash"],
        {"from":account},
        publish_source = config['networks'][network.show_active()].get("verify",False)
    )
    print("Deployed Lottery!")


def main():
    deploy_lottery()
