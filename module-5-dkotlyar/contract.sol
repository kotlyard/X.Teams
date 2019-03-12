pragma solidity ^0.5.2;


library Roles {
    struct Role {
        mapping (address => bool) bearer;
    }

    /**
     * @dev give an account access to this role
     */
    function add(Role storage role, address account) internal {
        require(account != address(0));
        require(!has(role, account));

        role.bearer[account] = true;
    }

    /**
     * @dev remove an account's access to this role
     */
    function remove(Role storage role, address account) internal {
        require(account != address(0));
        require(has(role, account));

        role.bearer[account] = false;
    }

    /**
     * @dev check if an account has this role
     * @return bool
     */
    function has(Role storage role, address account) internal view returns (bool) {
        require(account != address(0));
        return role.bearer[account];
    }
}

contract MinterRole {
    using Roles for Roles.Role;

    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);

    Roles.Role private _minters;

    constructor () internal {
        _addMinter(msg.sender);
    }

    modifier onlyMinter() {
        require(isMinter(msg.sender));
        _;
    }

    function isMinter(address account) public view returns (bool) {
        return _minters.has(account);
    }

    function addMinter(address account) public onlyMinter {
        _addMinter(account);
    }

    function renounceMinter() public {
        _removeMinter(msg.sender);
    }

    function _addMinter(address account) internal {
        _minters.add(account);
        emit MinterAdded(account);
    }

    function _removeMinter(address account) internal {
        _minters.remove(account);
        emit MinterRemoved(account);
    }
}


/**
 * @title SafeMath
 * @dev Unsigned math operations with safety checks that revert on error
 */
library SafeMath {
    /**
     * @dev Multiplies two unsigned integers, reverts on overflow.
     */
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
        // benefit is lost if 'b' is also tested.
        // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522
        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b);

        return c;
    }

    /**
     * @dev Integer division of two unsigned integers truncating the quotient, reverts on division by zero.
     */
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        // Solidity only automatically asserts when dividing by 0
        require(b > 0);
        uint256 c = a / b;
        // assert(a == b * c + a % b); // There is no case in which this doesn't hold

        return c;
    }

    /**
     * @dev Subtracts two unsigned integers, reverts on overflow (i.e. if subtrahend is greater than minuend).
     */
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;

        return c;
    }

    /**
     * @dev Adds two unsigned integers, reverts on overflow.
     */
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);

        return c;
    }

    /**
     * @dev Divides two unsigned integers and returns the remainder (unsigned integer modulo),
     * reverts when dividing by zero.
     */
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0);
        return a % b;
    }
}

/**
 * @title ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function approve(address spender, uint256 value) external returns (bool);

    function transferFrom(address from, address to, uint256 value) external returns (bool);

    function totalSupply() external view returns (uint256);

    function balanceOf(address who) external view returns (uint256);

    function allowance(address owner, address spender) external view returns (uint256);

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

/**
 * @title Standard ERC20 token
 *
 * @dev Implementation of the basic standard token.
 * https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
 * Originally based on code by FirstBlood:
 * https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
 *
 * This implementation emits additional Approval events, allowing applications to reconstruct the allowance status for
 * all accounts just by listening to said events. Note that this isn't required by the specification, and other
 * compliant implementations may not do it.
 */
contract ERC20 is IERC20 {
    using SafeMath for uint256;

    mapping (address => uint256) private _balances;

    mapping (address => mapping (address => uint256)) private _allowed;

    uint256 private _totalSupply;

    /**
     * @dev Total number of tokens in existence
     */
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    /**
     * @dev Gets the balance of the specified address.
     * @param owner The address to query the balance of.
     * @return An uint256 representing the amount owned by the passed address.
     */
    function balanceOf(address owner) public view returns (uint256) {
        return _balances[owner];
    }

    /**
     * @dev Function to check the amount of tokens that an owner allowed to a spender.
     * @param owner address The address which owns the funds.
     * @param spender address The address which will spend the funds.
     * @return A uint256 specifying the amount of tokens still available for the spender.
     */
    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowed[owner][spender];
    }

    /**
     * @dev Transfer token for a specified address
     * @param to The address to transfer to.
     * @param value The amount to be transferred.
     */
    function transfer(address to, uint256 value) public returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }

    /**
     * @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
     * Beware that changing an allowance with this method brings the risk that someone may use both the old
     * and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
     * race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
     * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
     * @param spender The address which will spend the funds.
     * @param value The amount of tokens to be spent.
     */
    function approve(address spender, uint256 value) public returns (bool) {
        _approve(msg.sender, spender, value);
        return true;
    }

    /**
     * @dev Transfer tokens from one address to another.
     * Note that while this function emits an Approval event, this is not required as per the specification,
     * and other compliant implementations may not emit the event.
     * @param from address The address which you want to send tokens from
     * @param to address The address which you want to transfer to
     * @param value uint256 the amount of tokens to be transferred
     */
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        _transfer(from, to, value);
        _approve(from, msg.sender, _allowed[from][msg.sender].sub(value));
        return true;
    }

    /**
     * @dev Transfer token for a specified addresses
     * @param from The address to transfer from.
     * @param to The address to transfer to.
     * @param value The amount to be transferred.
     */
    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0));

        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(from, to, value);
    }

    /**
     * @dev Internal function that mints an amount of the token and assigns it to
     * an account. This encapsulates the modification of balances such that the
     * proper events are emitted.
     * @param account The account that will receive the created tokens.
     * @param value The amount that will be created.
     */
    function _mint(address account, uint256 value) internal {
        require(account != address(0));

        _totalSupply = _totalSupply.add(value);
        _balances[account] = _balances[account].add(value);
        emit Transfer(address(0), account, value);
    }

    /**
     * @dev Approve an address to spend another addresses' tokens.
     * @param owner The address that owns the tokens.
     * @param spender The address that will spend the tokens.
     * @param value The number of tokens that can be spent.
     */
    function _approve(address owner, address spender, uint256 value) internal {
        require(spender != address(0));
        require(owner != address(0));

        _allowed[owner][spender] = value;
        emit Approval(owner, spender, value);
    }

}

/**
 * @title ERC20Mintable
 * @dev ERC20 minting logic
 */
contract ERC20Mintable is ERC20, MinterRole {
    /**
     * @dev Function to mint tokens
     * @param to The address that will receive the minted tokens.
     * @param value The amount of tokens to mint.
     * @return A boolean that indicates if the operation was successful.
     */
    function mint(address to, uint256 value) public onlyMinter returns (bool) {
        _mint(to, value);
        return true;
    }
}


contract Owner {
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor(address _owner) public {
        owner = _owner;
    }

    function changeOwner(address _newOwnerAddr) public onlyOwner {
        require(_newOwnerAddr != address(0));
        owner = _newOwnerAddr;
    }
}


contract GreenX is Owner, ERC20Mintable {

    string public name = "Shitcoin";
    string public symbol = "SHT";
    uint32 public decimals = 18;
    
    mapping(address => uint256) internal balances;
    mapping(address => mapping (address => uint256)) internal allowed;

    address public portalAddress;
    address public adminAddress;
    address public walletAddress;
    address public founderAddress;
    address public teamAddress;
    address public reservedAddress;
    
    mapping(address => bool) public privateList;
    mapping(address => bool) public whiteList;
    mapping(address => uint256) public totalInvestedAmountOf;
    
    uint constant lockPeriod1 = 3 minutes; // 1st locked period for tokens allocation of founder and team
    uint constant lockPeriod2 = 6 minutes; // 2nd locked period for tokens allocation of founder and team
    uint constant lockPeriod3 = 12 minutes; // locked period for remaining sale tokens after ending ICO
    uint constant NOT_SALE = 0; // Not in sales
    uint constant IN_PRIVATE_SALE = 1; // In private sales
    uint constant IN_PRESALE = 2; // In presales
    uint constant END_PRESALE = 3; // End presales
    uint constant IN_1ST_ICO = 4; // In ICO 1st round
    uint constant IN_2ND_ICO = 5; // In ICO 2nd round
    uint constant IN_3RD_ICO = 6; // In ICO 3rd round
    uint constant END_SALE = 7; // End sales
    
    uint256 public constant salesAllocation = 300000000 * 10 ** 18; // tokens allocated for public sales
    uint256 public constant bonusAllocation = 20000000 * 10 ** 18; //  tokens allocated for token sale bonuses for early invester
    uint256 public constant reservedAllocation = 50000000 * 10 ** 18; //  tokens allocated for reserved
    uint256 public constant founderAllocation = 50000000 * 10 ** 18; // 50 mil tokens allocated for founders
    uint256 public AdvisorPartnerAllocation = 50000000 * 10 ** 18; //  tokens allocated for partners and advisor
    uint256 public constant teamAllocation = 80000000 * 10 ** 18; // tokens allocated for team
    
    //I am not  sure about it!
    uint256 public constant minInvestedCap = 3000 * 10 ** 18; // 3000 ether for softcap
    uint256 public constant minInvestedAmount = 0.0003 * 10 ** 18; // 0.2 dollars for mininum ether contribution per transaction 1 eth = 600 dollars

    uint saleState;
    uint256 totalInvestedAmount;
    uint public icoStartTime;
    uint public icoEndTime;
    bool public inActive;
    bool public isSelling;
    bool public isTransferable;
    uint public founderAllocatedTime = 1;
    uint public teamAllocatedTime = 1;
    uint256 public privateSalePrice;
    uint256 public preSalePrice;
    uint256 public icoStandardPrice;
    uint256 public ico1stPrice;
    uint256 public ico2ndPrice;
    uint256 public totalRemainingTokensForSales; // Total tokens remaining for sales
    uint256 public totalReservedAndBonusTokenAllocation; // Total tokens allocated for reserved and bonuses
    uint256 public totalLoadedRefund; // Total ether will be loaded to contract for refund
    uint256 public totalRefundedAmount; // Total ether refunded to investors
    
    event Transfer(address indexed from, address indexed to, uint256 value); //ERC20 event
    event Approval(address indexed owner, address indexed spender, uint256 value);//ERC20 event
    
    event AddToWhiteList(address investorAddress, bool isWhiteListed);  // Add investor's address to white list
    event RemoveFromWhiteList(address investorAddress, bool isWhiteListed);  // Remove investor's address from white list
    event AddToPrivateList(address investorAddress, bool isPrivateListed);  // Add investor's address to private list
    event RemoveFromPrivateList(address investorAddress, bool isPrivateListed);  // Remove investor's address from private list
    event StartPrivateSales(uint state); // Start private sales
    event StartPresales(uint state); // Start presales
    event EndPresales(uint state); // End presales
    event StartICO(uint state); // Start ICO sales
    event EndICO(uint state); // End ICO sales

    event SetPrivateSalePrice(uint256 price); // Set private sale price
    event SetPreSalePrice(uint256 price); // Set presale price
    event SetICOPrice(uint256 price); // Set ICO standard price

    event IssueTokens(address investorAddress, uint256 amount, uint256 tokenAmount, uint state); // Issue tokens to investor
    event RevokeTokens(address investorAddress, uint256 amount, uint256 tokenAmount, uint256 txFee); // Revoke tokens after ending ICO for incompleted KYC investors
    event AllocateTokensForFounder(address founderAddress, uint256 founderAllocatedTime, uint256 tokenAmount); // Allocate tokens to founders' address
    event AllocateTokensForTeam(address teamAddress, uint256 teamAllocatedTime, uint256 tokenAmount); // Allocate tokens to team's address
    event AllocateReservedTokens(address reservedAddress, uint256 tokenAmount); // Allocate reserved tokens
    event Refund(address investorAddress, uint256 etherRefundedAmount, uint256 tokensRevokedAmount); // Refund ether and revoke tokens for investors

    modifier isActive() {
        require(inActive == false);
        _;
    }

    modifier isInSale() {
        require(isSelling == true);
        _;
    }

    modifier transferable() {
        require(isTransferable == true);
        _;
    }

    modifier onlyOwnerOrAdminOrPortal() {
        require(msg.sender == owner || msg.sender == adminAddress || msg.sender == portalAddress);
        _;
    }

    modifier onlyOwnerOrAdmin() {
        require(msg.sender == owner || msg.sender == adminAddress);
        _;
    }
    constructor(address _walletAddr, address _adminAddr, address _portalAddr) public Owner(msg.sender) {
        require(_walletAddr != address(0));
        require(_adminAddr != address(0));
        require(_portalAddr != address(0));

        walletAddress = _walletAddr;
        adminAddress = _adminAddr;
        portalAddress = _portalAddr;
        inActive = true;
        totalInvestedAmount = 0;
        mint(msg.sender, 500000000 * 10 ** uint256(decimals));
        totalRemainingTokensForSales = salesAllocation;
        totalReservedAndBonusTokenAllocation = reservedAllocation + bonusAllocation;
        
    }
    
    //Fallback function for token purchasing
    function () external payable isActive isInSale {
        uint state = getCurrentState();
        require(state >= IN_PRIVATE_SALE && state < END_SALE, "one");
        require(msg.value >= minInvestedAmount, "two");

        bool isPrivate = privateList[msg.sender];
        if (isPrivate == true) {
            return issueTokenForPrivateInvestor(state);
        }
        if (state == IN_PRESALE) {
            return issueTokenForPresale(state);
        }
        if (IN_1ST_ICO <= state && state <= IN_3RD_ICO) {
            return issueTokenForICO(state);
        }
        revert();
    }
    
    //
    function getCurrentState() public view returns(uint256) {
        if (saleState == IN_1ST_ICO) {
            if (now > icoStartTime + 6 minutes) {
                return IN_3RD_ICO;
            }
            if (now > icoStartTime + 3 minutes) {
                return IN_2ND_ICO;
            }
            return IN_1ST_ICO;
        }
        return saleState;
    }
    
    //
    function issueTokenForPrivateInvestor(uint _state) private {
        uint256 price = privateSalePrice;
        issueToken(price, _state);
    }
    
    //
    function issueTokenForPresale(uint _state) private {
        uint256 price = preSalePrice;
        issueToken(price, _state);
    }
    
    // Issue tokens to normal investors through ICO rounds
    function issueTokenForICO(uint _state) private {
        uint256 price = icoStandardPrice;
        if (_state == IN_1ST_ICO) {
            price = ico1stPrice;
        } else if (_state == IN_2ND_ICO) {
            price = ico2ndPrice;
        }
        issueToken(price, _state);
    }
    
    // function trackdownInvestedEther() private {
        
    // }
    
    // Issue tokens to investors and transfer ether to wallet
    function issueToken(uint256 _price, uint _state) private {
        require(walletAddress != address(0));

        uint tokenAmount = msg.value.mul(_price).mul(10**18).div(1 ether);
        balances[msg.sender] = balances[msg.sender].add(tokenAmount);
        totalInvestedAmountOf[msg.sender] = totalInvestedAmountOf[msg.sender].add(msg.value);
        totalRemainingTokensForSales = totalRemainingTokensForSales.sub(tokenAmount);
        totalInvestedAmount = totalInvestedAmount.add(msg.value);
        // walletAddress.transfer(msg.value);
        emit IssueTokens(msg.sender, msg.value, tokenAmount, _state);
    }
    
    // Add to whiteList
    function addToWhitelist(address[] calldata _investorAddrs) external isActive onlyOwnerOrAdminOrPortal returns(bool) {
        for (uint256 i = 0; i < _investorAddrs.length; i++) {
            whiteList[_investorAddrs[i]] = true;
            emit AddToWhiteList(_investorAddrs[i], true);
        }
        return true;
    }
    
    // Remove from whiteList
    function removeFromWhiteList(address[] calldata _investorAddrs) external isActive onlyOwnerOrAdminOrPortal returns(bool) {
        for (uint256 i = 0; i < _investorAddrs.length; i++) {
            whiteList[_investorAddrs[i]] = false;
            emit RemoveFromWhiteList(_investorAddrs[i], false);
        }
        return true;
    }
    
    function addToPrivateList(address[] calldata _investorAddrs) external isActive onlyOwnerOrAdminOrPortal returns(bool) {
        for (uint256 i = 0; i < _investorAddrs.length; i++) {
            privateList[_investorAddrs[i]] = true;
            emit AddToPrivateList(_investorAddrs[i], true);
        }
        return true;
    }
    
    function removeFromPrivateList(address[] calldata _investorAddrs) external isActive onlyOwnerOrAdminOrPortal returns(bool) {
        for (uint256 i = 0; i < _investorAddrs.length; i++) {
            privateList[_investorAddrs[i]] = false;
            emit RemoveFromPrivateList(_investorAddrs[i], false);
        }
        return true;
    }
    
    // Start private sales
    function startPrivateSales() external isActive onlyOwnerOrAdmin returns (bool) {
        require(saleState == NOT_SALE);
        require(privateSalePrice > 0);

        saleState = IN_PRIVATE_SALE;
        isSelling = true;
        emit StartPrivateSales(saleState);
        return true;
    }

    // Start presales
    function startPreSales() external isActive onlyOwnerOrAdmin returns (bool) {
        require(saleState < IN_PRESALE);
        require(preSalePrice > 0);

        saleState = IN_PRESALE;
        isSelling = true;
        emit StartPresales(saleState);
        return true;
    }
    
      // End presales
    function endPreSales() external isActive onlyOwnerOrAdmin returns (bool) {
        require(saleState == IN_PRESALE);

        saleState = END_PRESALE;
        isSelling = false;
        emit EndPresales(saleState);
        return true;
    }

    // Start ICO
    function startICO() external isActive onlyOwnerOrAdmin returns (bool) {
        require(saleState == END_PRESALE);
        require(icoStandardPrice > 0);

        saleState = IN_1ST_ICO;
        icoStartTime = now;
        isSelling = true;
        emit StartICO(saleState);
        return true;
    }

    // End ICO
    function endICO() external isActive onlyOwnerOrAdmin returns (bool) {
        require(getCurrentState() == IN_3RD_ICO);
        require(icoEndTime == 0);

        saleState = END_SALE;
        isSelling = false;
        icoEndTime = now;
        emit EndICO(saleState);
        return true;
    }
    
    // Set private sales price
    function setPrivateSalePrice(uint256 _tokenPerEther) external onlyOwnerOrAdmin returns(bool) {
        require(_tokenPerEther > 0);

        privateSalePrice = _tokenPerEther;
        emit SetPrivateSalePrice(privateSalePrice);
        return true;
    }

    // Set presales price
    function setPreSalePrice(uint256 _tokenPerEther) external onlyOwnerOrAdmin returns(bool) {
        require(_tokenPerEther > 0);

        preSalePrice = _tokenPerEther;
        emit SetPreSalePrice(preSalePrice);
        return true;
    }

    // Set ICO price including ICO standard price, ICO 1st round price, ICO 2nd round price
    function setICOPrice(uint256 _tokenPerEther) external onlyOwnerOrAdmin returns(bool) {
        require(_tokenPerEther > 0);

        icoStandardPrice = _tokenPerEther;
        ico1stPrice = _tokenPerEther + _tokenPerEther * 20 / 100;
        ico2ndPrice = _tokenPerEther + _tokenPerEther * 10 / 100;
        emit SetICOPrice(icoStandardPrice);
        return true;
    }
    
    // Revoke tokens from incompleted KYC investors' addresses
    function revokeToken(address _noneKycAddr, uint256 _transactionFee) external onlyOwnerOrAdmin {
        require(_noneKycAddr != address(0));
        uint256 investedAmount = totalInvestedAmountOf[_noneKycAddr];
        uint256 totalRemainingRefund = totalLoadedRefund.sub(totalRefundedAmount);
        require(whiteList[_noneKycAddr] == false && privateList[_noneKycAddr] == false);
        require(investedAmount > 0, "amount is 0");
        require(totalRemainingRefund >= investedAmount);
        require(saleState == END_SALE);

        uint256 refundAmount = investedAmount.sub(_transactionFee);
        uint tokenRevoked = balances[_noneKycAddr];
        totalInvestedAmountOf[_noneKycAddr] = 0;
        balances[_noneKycAddr] = 0;
        totalRemainingTokensForSales = totalRemainingTokensForSales.add(tokenRevoked);
        totalRefundedAmount = totalRefundedAmount.add(refundAmount);
        // _noneKycAddr.transfer(refundAmount);
        emit RevokeTokens(_noneKycAddr, refundAmount, tokenRevoked, _transactionFee);
    }
    
    function activateContract() external onlyOwner{
        //or false
        inActive = false;
    }
    
    function deactivateContract() external onlyOwner {
        //or true
        inActive = true;
    }
    
    // Enable transfer feature of tokens
    function enableTokenTransfer() external isActive onlyOwner {
        isTransferable = true;
    }
    
    // Change ETH wallet
    function changeFundKeeper(address _newAddress) external onlyOwner {
        require(_newAddress != address(0));
        require(walletAddress != _newAddress);
        
        walletAddress = _newAddress;
    }
    
    // Change admin address
    function changeAdminAddress(address _newAddress) external onlyOwner {
        require(_newAddress != address(0));
        require(adminAddress != _newAddress);
        
        adminAddress = _newAddress;
    }
    
    //Change portal Address
    function ChangePortalAddress(address _newAddress) external onlyOwner {
        require(_newAddress != address(0));
        require(portalAddress != _newAddress);
        
        portalAddress = _newAddress;
        
    }
    
    //Change founder Address
    function ChangeFounderAddress(address _newAddress) external onlyOwner {
        require(_newAddress != address(0));
        require(founderAddress != _newAddress);
        
        founderAddress = _newAddress;
    }

    //Change team Address
    function ChangeTeamAddress(address _newAddress) external onlyOwner {
        require(_newAddress != address(0));
        require(teamAddress != _newAddress);
        
        teamAddress = _newAddress;
    }

    //Change reserved Address
    function ChangeReservedAddress(address _newAddress) external onlyOwner {
        require(_newAddress != address(0));
        require(teamAddress != _newAddress);
        
        reservedAddress = _newAddress;
    }
    
      // Allocate tokens for founder vested gradually for 1 year
    function allocateTokensForFounder() external isActive onlyOwnerOrAdmin {
        require(saleState == END_SALE);
        require(founderAddress != address(0));
        
        uint256 amount;
        if (founderAllocatedTime == 1) {
            amount = founderAllocation * 20/100;
            balances[founderAddress] = balances[founderAddress].add(amount);
            emit AllocateTokensForFounder(founderAddress, founderAllocatedTime, amount);
            founderAllocatedTime = 2;
            return;
        }
        if (founderAllocatedTime == 2) {
            require(now >= icoEndTime + lockPeriod1);
            amount = founderAllocation * 30/100;
            balances[founderAddress] = balances[founderAddress].add(amount);
            emit AllocateTokensForFounder(founderAddress, founderAllocatedTime, amount);
            founderAllocatedTime = 3;
            return;
        }
        if (founderAllocatedTime == 3) {
            require(now >= icoEndTime + lockPeriod2);
            amount = founderAllocation * 50/100;
            balances[founderAddress] = balances[founderAddress].add(amount);
            emit AllocateTokensForFounder(founderAddress, founderAllocatedTime, amount);
            founderAllocatedTime = 4;
            return;
        }
        revert();
    }

    // Allocate tokens for team vested gradually for 1 year
    function allocateTokensForTeam() external isActive onlyOwnerOrAdmin {
        require(saleState == END_SALE);
        require(teamAddress != address(0));
        uint256 amount;
        if (teamAllocatedTime == 1) {
            amount = teamAllocation * 20/100;
            balances[teamAddress] = balances[teamAddress].add(amount);
            emit AllocateTokensForTeam(teamAddress, teamAllocatedTime, amount);
            teamAllocatedTime = 2;
            return;
        }
        if (teamAllocatedTime == 2) {
            require(now >= icoEndTime + lockPeriod1);
            amount = teamAllocation * 30/100;
            balances[teamAddress] = balances[teamAddress].add(amount);
            emit AllocateTokensForTeam(teamAddress, teamAllocatedTime, amount);
            teamAllocatedTime = 3;
            return;
        }
        if (teamAllocatedTime == 3) {
            require(now >= icoEndTime + lockPeriod2);
            amount = teamAllocation * 50/100;
            balances[teamAddress] = balances[teamAddress].add(amount);
            emit AllocateTokensForTeam(teamAddress, teamAllocatedTime, amount);
            teamAllocatedTime = 4;
            return;
        }
        revert();
    }

    // Remaining tokens for sales will be locked by contract in 2 years
    function moveAllAvaibleToken(address _addr) external isActive onlyOwnerOrAdmin {
        require(_addr != address(0));
        require(saleState == END_SALE);
        require(totalRemainingTokensForSales > 0);
        require(now >= icoEndTime + lockPeriod3);
        
        balances[_addr] = balances[_addr].add(totalRemainingTokensForSales);
        totalRemainingTokensForSales = 0;
    }

    // Allocate reserved tokens
    function allocateReservedTokens(address _addr, uint _amount) external isActive onlyOwnerOrAdmin {
        require(saleState == END_SALE);
        require(_amount > 0);
        require(_addr != address(0));

        balances[_addr] = balances[_addr].add(_amount);
        totalReservedAndBonusTokenAllocation = totalReservedAndBonusTokenAllocation.sub(_amount);
        emit AllocateReservedTokens(_addr, _amount);
    }
    
}