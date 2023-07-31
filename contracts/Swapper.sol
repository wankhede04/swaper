// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import '../interfaces/IERC20.sol';
import '../interfaces/IRouterSushi.sol';
import '../interfaces/IRouterArbidex.sol';
import '../interfaces/IRouterDODO.sol';

/// @title Swapper Contract for Token Swaps
contract Swapper {
    // Define constants for token addresses
    IERC20 public constant WETH = IERC20(0x82aF49447D8a07e3bd95BD0d56f35241523fBab1);
    IERC20 public constant USDC = IERC20(0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8);
    IERC20 public constant USDT = IERC20(0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9);

    // Define instances of different routers
    IRouterArbidex internal constant _ARBIDEX_ROUTER = IRouterArbidex(0x7238FB45146BD8FcB2c463Dc119A53494be57Aac);
    IRouterSushi internal constant _SUSHI_ROUTER = IRouterSushi(0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506);
    IRouterDODO internal constant _DODO_ROUTER = IRouterDODO(0x88CBf433471A0CD8240D2a12354362988b4593E5);

    // Address of the DODO USDT-USDC liquidity pool
    address public DODO_USDT_USDC_PAIR = 0xe4B2Dfc82977dd2DCE7E8d37895a6A8F50CbB4fB;
    
    /// @notice Swaps WETH for USDT
    /// @param amount1 The amount of WETH to be swapped through Arbidex router
    /// @param amount2 The amount of WETH to be swapped through SushiSwap router
    /// @param to The address to which the USDT tokens should be transferred
    /// @param deadline The deadline timestamp for the transaction
    function swapOptimalWETHForUSDT(uint256 amount1, uint256 amount2, address to, uint256 deadline) external {
        // Transfer WETH from the sender to this contract
        WETH.transferFrom(msg.sender, address(this), amount1 + amount2);
        
        // Approve Arbidex Router to spend WETH
        WETH.approve(address(_ARBIDEX_ROUTER), amount1);
        
        // Define the token path for the swap
        address[] memory path = new address[](2);
        path[0] = address(WETH);
        path[1] = address(USDC);
        
        // Variable to store the return amount of the swap
        uint256 returnAmount = 0;

        // Swap WETH for USDC using Arbidex Router
        if (amount1 > 0) {
            try _ARBIDEX_ROUTER.swapExactTokensForTokens(amount1, 0, path, address(this), deadline) returns (uint256[] memory amounts){
                // If the swap is successful, update the return amount
                returnAmount += amounts[1];
            } catch {
                // If the swap fails, add the remaining amount to amount2
                amount2 += amount1;
            }
        }

        // Swap remaining WETH for USDC using SushiSwap Router
        if (amount2 > 0) {
            // Approve SushiSwap Router to spend WETH
            WETH.approve(address(_SUSHI_ROUTER), amount2);
            // Perform the swap and update the return amount
            returnAmount += _SUSHI_ROUTER.swapExactTokensForTokens(amount2, 0, path, address(this), deadline)[1];
        }

        address[] memory pair = new address[](1);
        pair[0] = DODO_USDT_USDC_PAIR;

        // Approve DODO Router to spend USDC
        USDC.approve(0xA867241cDC8d3b0C07C85cC06F25a0cD3b5474d8, returnAmount);
        
        // Perform DODO swap from USDC to USDT
        uint256 usdtAmount = _DODO_ROUTER.dodoSwapV1(address(USDC), address(USDT), returnAmount, (returnAmount * 95) / 100, pair, 1, true, deadline);

        // Transfer the swapped USDT tokens to the recipient
        USDT.transfer(to, usdtAmount);
    }

    /// @notice Swaps USDT for WETH
    /// @param amount1 The amount of USDT to be swapped through DODO router
    /// @param amount2 The amount of USDT to be swapped through Arbidex and SushiSwap routers
    /// @param to The address to which the WETH tokens should be transferred
    /// @param deadline The deadline timestamp for the transaction
    function swapOptimalUSDTForWETH(uint256 amount1, uint256 amount2, address to, uint256 deadline) external {
        // Transfer USDT from the sender to this contract
        USDT.transferFrom(msg.sender, address(this), amount1 + amount2);
        
        // Approve DODO Router to spend USDT
        USDT.approve(0xA867241cDC8d3b0C07C85cC06F25a0cD3b5474d8, amount1 + amount2);
        
        // Define the token pair address for the DODO swap
        address[] memory pair = new address[](1);
        pair[0] = DODO_USDT_USDC_PAIR;
        
        // Swap USDT for USDC using DODO Router
        uint256 usdcAmount = _DODO_ROUTER.dodoSwapV1(address(USDT), address(USDC), amount1 + amount2, ((amount1 + amount2) * 95) / 100, pair, 0, true, deadline);
        
        // Define the token path for the swap
        address[] memory path = new address[](2);
        path[0] = address(USDC);
        path[1] = address(WETH);
        
        // Adjust the amounts for the Arbidex and SushiSwap swaps
        if (amount2 < usdcAmount) {
            amount1 -= usdcAmount - amount2;
        } else {
            amount2 -= usdcAmount - amount1;
        }

        // Variable to store the return amount of the swap
        uint256 returnAmount = 0;

        // Approve Arbidex Router to spend USDC
        USDC.approve(address(_ARBIDEX_ROUTER), amount1);
        
        // Swap USDC for WETH using Arbidex Router
        if (amount1 > 0) {
            try _ARBIDEX_ROUTER.swapExactTokensForTokens(amount1, 0, path, to, deadline) returns (uint256[] memory amounts){
                // If the swap is successful, update the return amount
                returnAmount += amounts[1];
            } catch {
                // If the swap fails, add the remaining amount to amount2
                amount2 += amount1;
            }
        }

        // Swap remaining USDC for WETH using SushiSwap Router
        if (amount2 > 0) {
            // Approve SushiSwap Router to spend USDC
            USDC.approve(address(_SUSHI_ROUTER), amount2);
            // Perform the swap and update the return amount
            returnAmount += _SUSHI_ROUTER.swapExactTokensForTokens(amount2, 0, path, to, deadline)[1];
        }
    }
}