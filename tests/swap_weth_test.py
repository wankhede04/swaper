from brownie import accounts, Swapper, interface
import datetime
import time
import calendar

def test_account_balance():
    swapOptimal = Swapper.deploy({'from':accounts[0]})
    print(accounts[0].balance())
    print(accounts[0].address)
    print(swapOptimal.address)
    
    USDC = interface.IERC20("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8")
    USDT = interface.IERC20("0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9")
    WETH = interface.IERC20("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1")
    print(WETH.balanceOf(accounts[0].address))
    #WETH.deposit({'from': accounts[0], 'amount': 1000000000000000000000, 'gas_price': 1000000000})

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    WETH.approve(swapOptimal.address, 20000000000000000000, {'from': accounts[0], 'gas_price': 1000000000})

    print("first")
    swapOptimal.swapOptimalWETHForUSDT(1000000000000000, 1000000000000, accounts[0].address, utc_time + 50000, {'from': accounts[0], 'gas_price': 1000000000, 'allow_revert': True})
    
    USDT.approve(swapOptimal.address, 2000000, {'from': accounts[0], 'gas_price': 1000000000})

    print("second")
    swapOptimal.swapOptimalUSDTForWETH(100000, 100000, accounts[0].address, utc_time + 50000, {'from': accounts[0], 'gas_price': 1000000000, 'gas_limit': 1000000000, 'allow_revert': True})
