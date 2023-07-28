// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

interface IPoolDodo {
    function sellBaseToken(
        uint256 amount,
        uint256 minReceiveQuote,
        bytes calldata data
    ) external returns (uint256);
}
//0xe4B2Dfc82977dd2DCE7E8d37895a6A8F50CbB4fB