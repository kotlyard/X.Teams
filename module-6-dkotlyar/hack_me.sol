// 0x57660d6E274e9D12afDA053125e78D5C9138f5D2 Metamask address
pragma solidity ^0.4.23;

contract SafeStorage {
	
	address [] public users;
	mapping (address => uint256) public balances;
	
	function deposit () public payable {
		if (balances[msg.sender] == 0) {
			users.push(msg.sender);
		}
		balances[msg.sender] += msg.value;
	}
	function withdrawAll() public {
		for (uint i = 0;i < users.length;i++) {
			users[i].transfer(balances[users[i]]);
	    }	
	}
	function BalnceOf(address _add) public view returns (uint) {
	    return (balances[_add]);
	}
	function getUsers() public view returns (address[]) {
	    return (users);
	}
}