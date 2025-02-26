from aiohttp import request
import pytest
from brownie import Contract, Jumpgate, Destrudo, accounts
from utils.config import (
    ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    EASYTRACK,
    LDO_ADDRESS,
    LDO_HOLDER,
    MULTITOKEN_ID,
    NFT_ID,
    RARIBLE_MT_ADDRESS,
    RARIBLE_NFT_ADDRESS,
    REWARD_PROGRAMS_REGISTRY,
    SOLANA_RANDOM_ADDRESS,
    SOLANA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
    TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    VITALIK,
    WORMHOLE_TOKEN_BRIDGE_ADDRESS,
)
from utils.contract import (
    init_add_reward_program_evm_script_factory,
    init_easytrack,
    init_ldo,
    init_rarible_mt,
    init_rarible_nft,
    init_reward_programs_registry,
    init_top_up_reward_program_evm_script_factory,
)
from utils.encode import encode_terra_address


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def non_owner(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def stranger(accounts):
    return accounts[2]


# test as the owner and a non-owner
@pytest.fixture(scope="session", params=["owner", "non_owner"])
def sender(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(
    params=[
        (TERRA_WORMHOLE_CHAIN_ID, TERRA_RANDOM_ADDRESS),
        (SOLANA_WORMHOLE_CHAIN_ID, SOLANA_RANDOM_ADDRESS),
    ]
)
def deploy_params(request):
    return request.param


# ERC20
@pytest.fixture
def token():
    return init_ldo(LDO_ADDRESS)


@pytest.fixture
def token_holder(accounts):
    return accounts.at(LDO_HOLDER, force=True)


# ERC721
@pytest.fixture(scope="function")
def nft():
    return init_rarible_nft(RARIBLE_NFT_ADDRESS)


@pytest.fixture
def nft_id():
    return NFT_ID


@pytest.fixture(scope="function")
def nft_holder(accounts):
    return accounts.at(VITALIK, force=True)


# ERC1155
@pytest.fixture(scope="function")
def multitoken():
    return init_rarible_mt(RARIBLE_MT_ADDRESS)


@pytest.fixture
def multitoken_id():
    return MULTITOKEN_ID


@pytest.fixture(scope="function")
def multitoken_holder(accounts):
    return accounts.at(VITALIK, force=True)


@pytest.fixture(scope="function")
def destrudo(owner):
    return Destrudo.deploy({"from": owner})


@pytest.fixture
def token_holder(accounts):
    return accounts.at(LDO_HOLDER, force=True)


@pytest.fixture
def bridge(interface):
    return interface.IWormholeTokenBridge(WORMHOLE_TOKEN_BRIDGE_ADDRESS)


@pytest.fixture(scope="function")
def jumpgate(owner, token, bridge):
    return Jumpgate.deploy(
        token.address,
        bridge.address,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": owner},
    )


@pytest.fixture
def easytrack():
    return init_easytrack(EASYTRACK)


@pytest.fixture
def reward_programs_registry():
    return init_reward_programs_registry(REWARD_PROGRAMS_REGISTRY)


@pytest.fixture
def add_reward_program_evm_script_factory():
    return init_add_reward_program_evm_script_factory(
        ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY
    )


@pytest.fixture
def top_up_reward_program_evm_script_factory():
    return init_top_up_reward_program_evm_script_factory(
        TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY
    )
