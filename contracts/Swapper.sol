// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import '../interfaces/IERC20.sol';
import '../interfaces/IRouterSushi.sol';
import '../interfaces/IRouterArbidex.sol';
import '../interfaces/IRouterDODO.sol';

contract Swapper {
    IERC20 public constant WETH = IERC20(0x82aF49447D8a07e3bd95BD0d56f35241523fBab1);

    IERC20 public constant USDC = IERC20(0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8);

    IRouterArbidex internal constant _ARBIDEX_ROUTER = IRouterArbidex(0x7238FB45146BD8FcB2c463Dc119A53494be57Aac);

    IRouterSushi internal constant _SUSHI_ROUTER = IRouterSushi(0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506);

    IRouterDODO internal constant _DODO_ROUTER = IRouterDODO(0x88CBf433471A0CD8240D2a12354362988b4593E5);

    address public DODO_USDT_USDC_PAIR = 0xe4B2Dfc82977dd2DCE7E8d37895a6A8F50CbB4fB;
    
    IERC20 public constant USDT = IERC20(0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9);

    function swapOptimalWETHForUSDT(uint256 amount1, uint256 amount2, address to, uint256 deadline) external {
        WETH.transferFrom(msg.sender, address(this), amount1 + amount2);
        WETH.approve(address(_ARBIDEX_ROUTER), amount1);
        address[] memory path = new address[](2);
        path[0] = address(WETH);
        path[1] = address(USDC);
        uint256 returnAmount = 0;
        if(amount1 > 0){
            try _ARBIDEX_ROUTER.swapExactTokensForTokens(amount1, 0, path, address(this), deadline) returns (uint256[] memory amounts){
                if(amount1 > 0){
                    returnAmount += amounts[1];
                }
            } catch  {
                amount2 += amount1;
            }
        }
        if(amount2 > 0){
            WETH.approve(address(_SUSHI_ROUTER), amount2);
            returnAmount += _SUSHI_ROUTER.swapExactTokensForTokens(amount2, 0, path, address(this), deadline)[1];
        }
        address[] memory pair = new address[](1);
        pair[0] = DODO_USDT_USDC_PAIR;
        USDC.approve(0xA867241cDC8d3b0C07C85cC06F25a0cD3b5474d8, returnAmount);
        uint256 usdtAmount = _DODO_ROUTER.dodoSwapV1(address(USDC), address(USDT), returnAmount, (returnAmount * 95) / 100, pair, 1, true, deadline);
        USDT.transfer(to, usdtAmount);
    }

    function swapOptimalUSDTForWETH(uint256 amount1, uint256 amount2, address to, uint256 deadline) external {
        USDT.transferFrom(msg.sender, address(this), amount1 + amount2);
        USDT.approve(0xA867241cDC8d3b0C07C85cC06F25a0cD3b5474d8, amount1 + amount2);
        address[] memory pair = new address[](1);
        pair[0] = DODO_USDT_USDC_PAIR;
        uint256 usdcAmount = _DODO_ROUTER.dodoSwapV1(address(USDT), address(USDC), amount1 + amount2, ((amount1 + amount2) * 95) / 100, pair, 0, true, deadline);
        address[] memory path = new address[](2);
        path[0] = address(USDC);
        path[1] = address(WETH);
        if(amount2  < usdcAmount)
            amount1 -= usdcAmount - amount2;
        else
            amount2 -= usdcAmount -amount1;
        uint256 returnAmount = 0;
        USDC.approve(address(_ARBIDEX_ROUTER), amount1);
        if(amount1 > 0){
            try _ARBIDEX_ROUTER.swapExactTokensForTokens(amount1, 0, path, to, deadline) returns (uint256[] memory amounts){
                if(amount1 > 0){
                    returnAmount += amounts[1];
                }
            } catch  {
                amount2 += amount1;
            }
        }
        if(amount2 > 0){
            USDC.approve(address(_SUSHI_ROUTER), amount2);
            returnAmount += _SUSHI_ROUTER.swapExactTokensForTokens(amount2, 0, path, to, deadline)[1];
        }
    }
}