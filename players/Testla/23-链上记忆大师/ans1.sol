pragma solidity =0.8.17;

contract MemoryMaster {
    uint256 x;
    function memorize(uint256 n) public {
        x = n;
    }
    function recall() public returns (uint256) {
        return x;
    }
}
