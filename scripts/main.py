from brownie import accounts, network, SwapOptimal, interface, Contract
from web3 import Web3
import datetime
import time
import calendar
#import get_price
liquidityWeth = [0,0,0]
liquidityUSDT = [0,0,0]
def main():
    USDC = interface.IERC20("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8")
    WETH = interface.IERC20("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1")
    
    swapper = accounts.add(input("Enter private key for address which wants to swap: "))

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    
    choice = int(input("Enter your choice, what you want to swap:\n 1)WETH -> USDC \n2)USDC -> WETH \n(1 or 2): "))
    
    swapOptimal = Contract.from_abi("SwapOptimal", input("Enter address of SwapOptimalContract: "), SwapOptimal.abi)
    
    amountIn = int(input("Enter amount you want to swap: "))

    tx = "Wrong choice"
    if choice == 1:
        combo = get_optimal_combo(amountIn, [WETH.address, USDC.address])
        tx = swapOptimal.swapOptimalWETHForUSDC(amountIn * get_optimal_combo['arbi'], amountIn - get_optimal_combo['arbi'] * amountIn, swapper.address, utc_time + 50000, {'from': swapper, 'max_fee': 21000000000, 'priority_fee': 21000000000, 'gas_limit': 21000000000, 'allow_revert': True})
    if choice == 2:
        combo = get_optimal_combo(amountIn, [USDC.address, WETH.address])
        tx = swapOptimal.swapOptimalUSDCForWETH(amountIn * get_optimal_combo['arbi'], amountIn - get_optimal_combo['arbi'] * amountIn, swapper.address, utc_time + 50000, {'from': swapper, 'gas_price': 1000000000})
    print(tx)

def get_optimal_combo(amountIn, path):
    routerArbidexAddress = "0x7238FB45146BD8FcB2c463Dc119A53494be57Aac"
    routerSushiAddress = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"
    
    routerArbidex = interface.IRouterArbidex(routerArbidexAddress)
    routerSushi = interface.IRouterSushi(routerSushiAddress)

    slot=0
    maxSlot = 0
    
    if(amountIn > 100):
        slot = amountIn/100;
        maxSlot = 100
    else:
        slot=1
        maxSlot=amountIn
    
    max = 0
    iterMax = 0
    sushiMax = 0
    arbiMax = 0
    for iter in range(1, maxSlot):
        firstAmount = (slot * (iter))
        temp = routerArbidex.getAmountsOut(firstAmount, path)[1]
        temp += routerSushi.getAmountsOut(amountIn - firstAmount, path)[1]
        
        if temp > max:
            max = temp
            arbiMax = firstAmount
            sushiMax = amountIn - firstAmount
    
    fullArbidex = routerArbidex.getAmountsOut(amountIn, path)[1]
    fullSushi = routerSushi.getAmountsOut(amountIn, path)[1]
    
    if fullSushi > fullArbidex:
        if fullSushi > max:
            return {'sushi': 1, 'arbi': 0}
    
    if fullSushi < fullArbidex:
        if fullArbidex > max:
            return {'sushi': 0, 'arbi': 1}

    sushiRatio = (float(sushiMax))/amountIn
    return {'sushi': sushiRatio, 'arbi': 1 - sushiRatio}