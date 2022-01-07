# from eth_account import account
from brownie import (
    network,
    config,
    accounts,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken
)
from web3 import Web3

FORKED_LOCAL_ENV = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]

DECIMALS = 8
INITIAL_VALUE = 20000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENV) or (
        network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    return accounts.load("my-account")


contract_to_mock = {
    "eth_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract address from the brownie config
    if defined, otherwise it will deploy a mock version of that contract and
    return that mock contract

    Args:
        contract_name(string)

    Returns:
        brownie.network.contract.ProjectContract: this most recently deployed
        version of this contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({'from':account})
    VRFCoordinatorMock.deploy(link_token.address,{'from':account})
    print("Deployed Mocks")