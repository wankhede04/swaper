from brownie import accounts, Swapper, interface
import datetime
import time
import calendar
import os
from dotenv import load_dotenv 

# Define the test function for the Swapper contract
def test_swapper():
    load_dotenv('../')
    # Deploy the Swapper contract with accounts[0] (the first account)
    swapOptimal = Swapper.deploy({'from': accounts[0]})
    
    # Define ERC20 token contracts for USDC, USDT, and WETH
    USDC = interface.IERC20(os.getenv('USDC'))
    USDT = interface.IERC20(os.getenv('USDT'))
    WETH = interface.IERC20(os.getenv('WETH'))
    
    # Print the address of account
    print(accounts[0].address)
    
    # Deposit WETH to the Swapper contract
    WETH.deposit({'from': accounts[0], 'amount': 1000000000000000000000, 'gas_price': 1000000000})
    
    # Get current UTC time
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    
    # Approve WETH tokens for the Swapper contract
    WETH.approve(swapOptimal.address, 20000000000000000000, {'from': accounts[0], 'gas_price': 1000000000})
    
    # Perform WETH -> USDT swap using the swapOptimalWETHForUSDT function
    swapOptimal.swapOptimalWETHForUSDT(1000000000000000, 1000000000000, accounts[0].address, utc_time + 50000, {'from': accounts[0], 'gas_price': 1000000000, 'allow_revert': True})
    
    # Approve USDT tokens for the Swapper contract
    USDT.approve(swapOptimal.address, 2000000, {'from': accounts[0], 'gas_price': 1000000000})
    
    # Perform USDT -> WETH swap using the swapOptimalUSDTForWETH function
    swapOptimal.swapOptimalUSDTForWETH(100000, 100000, accounts[0].address, utc_time + 50000, {'from': accounts[0], 'gas_price': 1000000000, 'gas_limit': 1000000000, 'allow_revert': True})
