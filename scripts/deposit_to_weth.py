# Import necessary modules and libraries
from brownie import accounts, network, Swapper, interface
import os
from dotenv import load_dotenv 

# Define the main function that will be executed when the script is run
def main():
    load_dotenv('../')
    # Define ERC20 token contracts for USDC and WETH
    USDC = interface.IERC20(os.getenv('USDC'))
    WETH = interface.IERC20(os.getenv('WETH'))

    # Add an Ethereum account for depositing ETH
    swapper = accounts.add(input("Enter the private key to deposit ETH with: "))

    # Deposit WETH to the Swapper contract
    # Get the amount to deposit from the user and deposit it
    deposit_amount = int(input("Enter the amount of WETH to deposit: "))
    WETH.deposit({'from': swapper, 'amount': deposit_amount, 'gas_price': 1000000000})

    # Print the balance of WETH for the swapper account after the deposit
    print("WETH balance of the swapper account:", WETH.balanceOf(swapper))