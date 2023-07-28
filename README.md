# Optimal Swapper
## Smart Contracts 
First part will be implement a smart contract that can allow you to buy or sell on
WETH/USDT pool on Arbitrum on the following dex. You can use any tool for contract
deployment.
- Arbidex V3
- DODO
- Sushiswap

## get_price
This part contains a python script to provide with optimal amounts to swap with Arbidex and SushiSwap respectively.
Input:
- Amount to be swapped
- Path(USDT to WETH or WETH to USDT)

Output provides with dictionary describing ratio to swap in:

Example:
```
{'sushi': 0.3, 'arbi': 0.7}
```

## main
This python scripts calls `get_price` to fetch best ratio for swap, and then calls the contract to swap amounts.
It asks for the following inputs:
- Private key for swapper
- Choice(for Path of swap)
- Swapper address
- Amount

## Calculation for optimal price
The current implementation involves making calls to rpc for current return amount for provided input after dividing it into 100 parts and calling for a all ratios, and then chooses the maximum output.

## A Better approach for getting optimal price
​
`(x + dx) * (y - dy) = k`

where x and y are reserves before swap in a pool

dx is the amount of token we want to swap and dy is the amount of other token to be recieved after swap
​

this equation simplifies to,

​
`dy = y * dx / (x + dx)`

​
Taking swap fee into account this turns out to

​
`dy = y * (1 - fee) * dx / (x + (1 - fee) * dx)`

​
This is applicable for both DEXs, let's consider both of them.

​
for 1st DEX: `dy1 = y1 * R * dx1 / (x1 + R * dx1)`

​
where `1- fee = R`

we can have similar equation for both DEXs (substituting 1 by 2).
​also, `dx1 + dx2 = A` (amount of swap)
​
using this and above equation
​
substituting` dx2 = A - dx1`

​
`dy2 = y2 * R * (A - dx1) / (x2 + R * (A - dx1))`

​
Adding dy1 and dy2

​
`dy1 + dy2 = y1 * R * dx1 / (x1 + R * dx1) + y2 * R * (A - dx1) / x2 + R (A - dx1)`

​
We now need to find max of dy1 + dy2 for some value of dx1, rest all values are constant
​

NOTE: I was exploring this approach and found that if we used constant product formula AMMs (V2's) then this could be in scope of this test task, but in V3 AMMs the liquidity can change based on tick change which further breaks this equation. This takes it out of scope for a test assignment.

## My approach to the problem
- I started with writing contract to perform swaps, I implemented the function to swap on both dexs for USDC to WETH and vice versa. And also implemented DODO swap for conversion from USDC to USDT or vice versa according to the call recieved.
- I decided to use forked chain for performing trasactions and deploying contracts.

#### *Note1
Arbidex was not working as the number of call limits for Arbidex's getProfit was set to 1000, and EVM stack space is a total of 1024 elements. And hence sending tryArbitrage in loop and providing the related error.

- So to solve this problem I decided to implement my contract such that it contains try catch, in case if arbidex fails to swap the whole amount will be swapped by sushi only.
- Hence presenting the contracts available in this repo.

## Running the scripts
To run the available scripts use brownie, for example
```
$ brownie run sciripts/main.py
```
#### Extra scripts:
- deposit to weth
- deploy the contract
- approve contract to transfer WETH and USDT/USDC

## Test
To run the above tests one needs to run the following commands
```
$ brownie test
```

*Note: to run the above commands with your specified network: add the following flag to commands:
```
--network <the network you have added to brownie>
```
