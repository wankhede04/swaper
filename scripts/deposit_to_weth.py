from brownie import accounts, network, Swapper, interface
from web3 import Web3# Contract
liquidityWeth = [0,0,0]
liquidityUSDT = [0,0,0]
def main():
    USDC = interface.IERC20("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8")
    WETH = interface.IERC20("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1")
    swapper = accounts.add(input("Enter private key to deposit eth with: "))
    WETH.deposit({'from': swapper, 'amount': int(input("Enter amount to deposit: ")), 'gas_price': 1000000000})
    print(WETH.balanceOf(swapper))