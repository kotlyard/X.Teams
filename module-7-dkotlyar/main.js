// let MetaCoin;
// let accounts
// let account

// const App = {
//    start: function () {
//        const self = this

//        // Bootstrap the MetaCoin abstraction for Use.
//        MetaCoin.setProvider(web3.currentProvider)

//        // Get the initial account balance so it can be displayed.
//        web3.eth.getAccounts(function (err, accs) {
//            if (err != null) {
//                alert('There was an error fetching your accounts.')
//                return
//            }

//            if (accs.length === 0) {
//                alert("Couldn't get any accounts! Make sure your Ethereum client is configured correctly.")
//                return
//            }

//            accounts = accs
//            account = accounts[0]

//            self.refreshBalance()
//        })
//    },

//    setStatus: function (message) {
//        const status = document.getElementById('status')
//        status.innerHTML = message
//    },

//    // refreshBalance: function () {
//    //     const self = this

//    //     //replace this address with your contracts address you get after migrating

//    //     var contractInstance = MetaCoin.at('0xf25186b5081ff5ce73482ad761db0eb0d25abfbf'); 
//    //     //use your contract address you'll get after deploying the contract i.e. running migrate

//    //     contractInstance.getBalance.call(account, { from: account })
//    //         .then(function (value) {
//    //             const balanceElement = document.getElementById('balance')
//    //             balanceElement.innerHTML = value.valueOf()
//    //         }).catch(function (e) {
//    //             console.log(e)
//    //             self.setStatus('Error getting balance; see log.')
//    //         });
//    // },

//    sendCoin: function () {
//        const self = this

//        const amount = parseInt(document.getElementById('amount').value)
//        const receiver = document.getElementById('receiver').value

//        this.setStatus('Initiating transaction... (please wait)')

//        let meta
//        MetaCoin.deployed().then(function (instance) {
//            meta = instance
//            return meta.sendCoin(receiver, amount, { from: account })
//        }).then(function () {
//            self.setStatus('Transaction complete!')
//            self.refreshBalance()
//        }).catch(function (e) {
//            console.log(e)
//            self.setStatus('Error sending coin; see log.')
//        })
//    }
// }

// window.App = App

// window.addEventListener('load', function () {
//    // Checking if Web3 has been injected by the browser (Mist/MetaMask)
//    if (typeof web3 !== 'undefined') {
//        console.warn(
//            'Using web3 detected from external source.' +
//            ' If you find that your accounts don\'t appear or you have 0 MetaCoin,' +
//            ' ensure you\'ve configured that source properly.' +
//            ' If using MetaMask, see the following link.' +
//            ' Feel free to delete this warning. :)' +
//            ' http://truffleframework.com/tutorials/truffle-and-metamask'
//        )
//        // Use Mist/MetaMask's provider
//        window.web3 = new Web3(web3.currentProvider)
//    } else {
//        console.warn(
//            'No web3 detected. Falling back to http://127.0.0.1:9545.' +
//            ' You should remove this fallback when you deploy live, as it\'s inherently insecure.' +
//            ' Consider switching to Metamask for development.' +
//            ' More info here: http://truffleframework.com/tutorials/truffle-and-metamask'
//        )
//        // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
//        window.web3 = new Web3(new Web3.providers.HttpProvider('http://127.0.0.1:9545'))
//    }

//    MetaCoin = window.web3.eth.contract(/*abi array here*/) ;
//    /* replace with your abi array, you can find it in the metacoin.json file in the /build folder after you run migration
//        [
//            {
//                "inputs": [],
//                "payable": false,
//                "stateMutability": "nonpayable",
//                "type": "constructor"
//            }
//            .
//            .
//            .
//            // 
//        ]
//    */
//    App.start()
// })