# Import necessary modules and libraries
from brownie import accounts, network, Swapper, interface
from web3 import Web3
import os
from dotenv import load_dotenv 

# Define the main function that will be executed when the script is run
def main():
    # Add an Ethereum account for deploying the Swapper contract
    deployer = accounts.add(input("Enter the private key to deploy the contract with: "))

    # Deploy the Swapper contract
    # The Swapper contract is deployed using the `Swapper.deploy()` function
    # 'from' specifies the Ethereum account that will be used for deploying the contract
    # 'gas_price' sets the gas price for the transaction
    tx = Swapper.deploy({'from': deployer, 'gas_price': 100000000})

    # Print the transaction receipt after deploying the contract
    print(tx)