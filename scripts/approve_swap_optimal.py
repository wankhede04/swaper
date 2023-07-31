# Import necessary modules and libraries
from brownie import accounts, network, Swapper, interface
from web3 import Web3
import os
from dotenv import load_dotenv 

# Define the main function that will be executed when the script is run
def main():
    load_dotenv('../')
    print(os.getenv('USDC'))
    # Define ERC20 token contracts for USDC and WETH
    USDC = interface.IERC20(os.getenv('USDC'))
    WETH = interface.IERC20(os.getenv('WETH'))

    # Add an Ethereum account for approving the contract to spend tokens
    swapper = accounts.add(input("Enter the private key to approve tokens with: "))

    # Get the address of the Swapper contract
    swapOptimalAddress = input("Enter the address of SwapperContract: ")

    # Approve the Swapper contract to spend WETH tokens
    # Get the amount of WETH to approve from the user and approve it
    weth_approval_amount = int(input("Enter the amount of WETH to approve: "))
    tx = WETH.approve(swapOptimalAddress, weth_approval_amount, {'from': swapper, 'gas_price': 1000000000})

    # Approve the Swapper contract to spend USDC tokens
    # Get the amount of USDC to approve from the user and approve it
    usdc_approval_amount = int(input("Enter the amount of USDC to approve: "))
    tx = USDC.approve(swapOptimalAddress, usdc_approval_amount, {'from': swapper, 'gas_price': 1000000000})
