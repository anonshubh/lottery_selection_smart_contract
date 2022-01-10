from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpers import LOCAL_BLOCKCHAIN_ENV, fund_with_link, get_account
import pytest, time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    value = lottery.getEntranceFee() + 100000000
    lottery.enter({"from": account, "value": value})
    lottery.enter({"from": account, "value": value})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
