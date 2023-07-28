from brownie import accounts, network, Swapper, interface
from web3 import Web3# Contract
liquidityWeth = [0,0,0]
liquidityUSDT = [0,0,0]
def main():
    deployer = accounts.add(input("Enter private key to deploy contract with: "))
    tx = Swapper.deploy({'from': deployer, 'gas_price': 100000000})
    print(tx)