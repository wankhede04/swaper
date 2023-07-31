# Import necessary modules and libraries
from brownie import accounts, network, Swapper, interface, Contract
from web3 import Web3
import datetime
import time
import calendar
import os
from dotenv import load_dotenv 

# Define the main function that will be executed when the script is run
def main():
    load_dotenv('../')
    # Define ERC20 token contracts for USDC and WETH
    USDC = interface.IERC20(os.getenv('USDC'))
    WETH = interface.IERC20(os.getenv('WETH'))

    # Add an Ethereum account for swapping
    swapper = accounts.add(input("Enter private key for the address that wants to swap: "))

    # Get current UTC time
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    # Get the user's choice for the swap
    choice = int(input("Enter your choice of swap:\n 1)WETH -> USDC \n2)USDC -> WETH \n(1 or 2): "))

    # Get the SwapOptimal contract
    swapOptimal = Contract.from_abi("SwapOptimal", input("Enter the address of SwapOptimalContract: "), SwapOptimal.abi)

    # Get the amount the user wants to swap
    amountIn = int(input("Enter the amount you want to swap: "))

    # Initialize the transaction variable
    tx = "Wrong choice"

    # Check the user's choice and perform the respective swap
    if choice == 1:
        # Get the optimal combo for WETH -> USDC swap
        combo = get_optimal_combo(amountIn, [WETH.address, USDC.address])
        
        # Execute the swapOptimalWETHForUSDC function
        tx = swapOptimal.swapOptimalWETHForUSDC(amountIn * get_optimal_combo['arbi'], amountIn - get_optimal_combo['arbi'] * amountIn, swapper.address, utc_time + 50000, {'from': swapper, 'max_fee': 21000000000, 'priority_fee': 21000000000, 'gas_limit': 21000000000, 'allow_revert': True})
    elif choice == 2:
        # Get the optimal combo for USDC -> WETH swap
        combo = get_optimal_combo(amountIn, [USDC.address, WETH.address])
        
        # Execute the swapOptimalUSDCForWETH function
        tx = swapOptimal.swapOptimalUSDCForWETH(amountIn * get_optimal_combo['arbi'], amountIn - get_optimal_combo['arbi'] * amountIn, swapper.address, utc_time + 50000, {'from': swapper, 'gas_price': 1000000000})
    
    # Print the transaction hash
    print(tx)

# Function to get the optimal swap combo for given input amount and path
def get_optimal_combo(amountIn, path):
    # Define router addresses for Arbidex and SushiSwap
    routerArbidexAddress = os.getenv('ARBROUTER')
    routerSushiAddress = os.getenv('SUSHIROUTER')

    # Create instances of the Arbidex and SushiSwap routers
    routerArbidex = interface.IRouterArbidex(routerArbidexAddress)
    routerSushi = interface.IRouterSushi(routerSushiAddress)

    # Determine the slot size and maximum slot
    slot = 0
    maxSlot = 0

    if amountIn > 100:
        slot = amountIn / 100
        maxSlot = 100
    else:
        slot = 1
        maxSlot = amountIn

    # Initialize variables to find optimal combo
    max = 0
    iterMax = 0
    sushiMax = 0
    arbiMax = 0

    # Loop through the possible iterations to find the optimal combo
    for iter in range(1, maxSlot):
        firstAmount = slot * iter
        temp = routerArbidex.getAmountsOut(firstAmount, path)[1]
        temp += routerSushi.getAmountsOut(amountIn - firstAmount, path)[1]

        if temp > max:
            max = temp
            arbiMax = firstAmount
            sushiMax = amountIn - firstAmount

    # Get the amounts out for the full swap on Arbidex and SushiSwap
    fullArbidex = routerArbidex.getAmountsOut(amountIn, path)[1]
    fullSushi = routerSushi.getAmountsOut(amountIn, path)[1]

    # Compare full swap amounts to determine the optimal combo
    if fullSushi > fullArbidex:
        if fullSushi > max:
            return {'sushi': 1, 'arbi': 0}

    if fullSushi < fullArbidex:
        if fullArbidex > max:
            return {'sushi': 0, 'arbi': 1}

    sushiRatio = (float(sushiMax)) / amountIn
    return {'sushi': sushiRatio, 'arbi': 1 - sushiRatio}
