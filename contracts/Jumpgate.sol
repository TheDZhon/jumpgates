// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/token/ERC20/ERC20.sol";

import "./AssetRecoverer.sol";
import "../interfaces/IWormholeTokenBridge.sol";

/// @title Jumpgate
/// @author mymphe
/// @notice Transfer an ERC20 token using a Wormhole token bridge with pre-determined parameters
/// @dev `IWormholeTokenBridge` and the logic in `_callBridgeTransfer` are specific to Wormhole Token Bridge
contract Jumpgate is AssetRecoverer {
    event JumpgateCreated(
        address indexed _token,
        address indexed _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee
    );

    event TokensBridged(
        address indexed _token,
        address indexed _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee,
        uint256 _amount,
        uint32 _nonce,
        uint64 _transferSequence
    );

    /// ERC20 token to be bridged
    IERC20 public immutable token;

    /// Wormhole token bridge
    IWormholeTokenBridge public immutable bridge;

    /// Wormhole id of the target chain
    uint16 public immutable recipientChain;

    /// bytes32-encoded recipient address on the target chain
    bytes32 public immutable recipient;

    /// Wormhole arbiter fee
    uint256 public immutable arbiterFee;

    constructor(
        address _token,
        address _bridge,
        uint16 _recipientChain,
        bytes32 _recipient,
        uint256 _arbiterFee
    ) {
        token = IERC20(_token);
        bridge = IWormholeTokenBridge(_bridge);
        recipientChain = _recipientChain;
        recipient = _recipient;
        arbiterFee = _arbiterFee;

        emit JumpgateCreated(
            _token,
            _bridge,
            _recipientChain,
            _recipient,
            _arbiterFee
        );
    }

    /// @notice transfer all of the tokens on this contract's balance to the cross-chain recipient
    /// @dev permissionless method; caller only pays for bridging gas
    function bridgeTokens() public {
        uint256 amount = token.balanceOf(address(this));
        token.approve(address(bridge), amount);
        uint64 sequence = _callBridgeTransfer(amount);

        emit TokensBridged(
            address(token),
            address(bridge),
            recipientChain,
            recipient,
            arbiterFee,
            amount,
            0,
            sequence
        );
    }

    /// @notice calls the transfer method on the bridge
    /// @dev implements the actual logic of the bridge transfer
    /// @param _amount amount of tokens to transfer
    function _callBridgeTransfer(uint256 _amount)
        private
        returns (uint64 sequence)
    {
        sequence = bridge.transferTokens(
            address(token),
            _amount,
            recipientChain,
            recipient,
            arbiterFee,
            0
        );
    }
}
