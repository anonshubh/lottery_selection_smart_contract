from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_price_feed"], {"from": account}
    )
    lottery_fee = lottery.getEntranceFee()
    # assert lottery_fee > Web3.toWei(0.014, "ether")
    # assert lottery_fee < Web3.toWei(0.022, "ether")
