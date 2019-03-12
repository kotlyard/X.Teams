

import 'https://cdn.jsdelivr.net/gh/ethereum/web3.js/dist/web3.min.js';

const testnet = 'https://ropsten.infura.io/';
const web3 = new Web3(new Web3.providers.HttpProvider(testnet));
var current_wallet = null;



function getBalance(address) {
	var balance = web3.eth.getBalance(address);
	balance = web3.toDecimal(balance);
	return (balance / 1000000000000000000);
}


function random32bit() {
    let u = new Uint32Array(1);
    window.crypto.getRandomValues(u);
    let str = u[0].toString(16).toUpperCase();
    return '00000000'.slice(str.length) + str;
}


function createWallet()
{
	current_wallet = web3.eth.accounts.wallet.create(1);
	document.getElementById("private_key").innerHTML = "Your private key: " + current_wallet[0].privateKey;
	document.getElementById("public_address").innerHTML = "Your public address: " + current_wallet[0].address;
}

function sendEther(account, to, amount) {
	return (true);
}



