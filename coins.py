# AUTHOR: JAKE FOGEL
# STUDENT ID: 261085935

import requests

def dict_to_query(dicti):
    """(dict) -> str
    Takes dictionary (dicti) and formats it in API url format, with data
    in the correct order

    >>> dict_to_query({'email': 'example@mcgill.ca', 'token': 'ABC'})
    'email=example@mcgill.ca&token=ABC'
    >>> dict_to_query({'email': 'jacob.fogel@mcgill.ca', 'token': 'valid_token'})
    'email=example@mcgill.ca&token=ABC'
    >>> dict_to_query('hi')
    AssertionError: Improper dictionary format
    """
    
    if type(dicti) != dict:
        raise AssertionError('Improper dictionary format')
    
    output = ''
    for i, key in enumerate(dicti):
        output += str(key) + '=' + str(dicti[key])
        if i != len(dicti) - 1:
            output += '&'
    
    return output

class Account():
    """A class representing a user accessing the comp202coin API

    Instance Attributes:
    * email: str
    * token: str
    * balance: int
    * request_log: list
    Class Attributes:
    * API_URL: str
    """
    
    API_URL = 'https://coinsbot202.herokuapp.com/api/'
    
    def __init__(self, email, token):
        """(str, str) -> NoneType
        Initializes an Account object
        
        >>> my_acct = Account("example@mcgill.ca", "ABC")
        >>> my_acct.balance
        -1
        >>> my_acct = Account("jacob.fogel@mail.mcgill.ca", "valid_token")
        AssertionError: Please enter email and token of valid types!
        >>> my_acct = Account("jacob.fogel@mail.concordia.ca", 'valid_token')
        AssertionError: Please enter a valid email!
        """
        
        if type(email) != str or type(token) != str:
            raise AssertionError('Please enter email and token of valid types!')
        if email[-9:] != 'mcgill.ca':
            raise AssertionError('Please enter a valid email!')
        self.email = email
        self.token = token
        self.balance = -1
        self.request_log = []
        
    def __str__(self):
        """() -> str
        Returns string to be outputted whem Account object is printed
        
        >>> my_acct = Account("jacob.fogel@mail.mcgill.ca", "valid_token")
        >>> print(my_acct)
        jacob.fogel@mail.mcgill.ca has balance 400293049023904023940239
        >>> my_acct = Account("valid_email", "valid")
        >>> print(my_acct)
        valid_email has balance corresponding_balance
        >>> my_acct = Account("testemail@mcgill.ca", "valid_token")
        >>> print(my_acct)
        testemail@mcgill.ca has balance valid_token
        """
        return str(self.email) + ' has balance ' + str(self.balance)

    def call_api(self, endpoint, req_dict):
        """(str, dict) -> dict<str>
        Takes a valid endpoint and request dictionary and calls the comp202coin API
        returning the returned message and status information in a dictionary
        
        >>> my_acct = Account("example@mcgill.ca", "ABC")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        1
        >>> my_acct = Account("jacob.fogel@mcgill.ca", "valid_token")
        >>> my_acct.call_api(balance, {'email': my_acct.email})
        AssertionError: Please enter endpoint and request dictionary inputs of the valid types! (str, dict)
        >>> my_acct = Account("valid_email", "valid_token")
        >>> my_acct.call_api("shmalance", {'email': my_acct.email})
        AssertionError: Please enter an enpoint that is "balance" or "transfer"
        """
        
        if type(endpoint) != str or type(req_dict) != dict:
            raise AssertionError('Please enter endpoint and request dictionary inputs of the valid types! (str, dict)')
        
        if endpoint not in ['balance', 'transfer']:
            raise AssertionError('Please enter an enpoint that is "balance" or "transfer"')
        
        req_dict['token'] = self.token

        request_url = Account.API_URL + endpoint + '?' + dict_to_query(req_dict)
        
        result = requests.get(url=request_url).json()
        
        if result['status'] != 'OK':
            raise AssertionError(result['message'])
        
        return result
        
    def retrieve_balance(self):
        """() -> int
        Accessess the comp202coin API to return the balance of a specific user
        Account object
        
        >>> my_acct = Account("example@mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        1
        >>> my_acct = Account("valid_email", "valid_token")
        >>> my_acct.retrieve_balance()
        valid_balance
        >>> my_acct = Account("jacob.fogel@mail.mcgill.ca", "valid_token")
        984098509380934802804985092845029834509823405982093485092834590
        """
        user_dict = {'email': self.email, 'token': self.token}
        
        balance_result = self.call_api('balance', user_dict)
        
        new_balance = int(balance_result['message'])
        
        self.balance = new_balance
        
        return new_balance
    
    def transfer(self, coins, email):
        """(int, str) -> str
        Accesses the comp202con API to transfer comp202coins from the user account
        to the specified recipient
        
        >>> Account("example@mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        25
        >>> my_acct.transfer(25, "example2@mail.mcgill.ca")
        'You have transferred 25 coins of your balance of 25 coins to alexa.infelise@mail. mcgill.ca. Your balance is now 0.'
        >>> Account("example@mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        -1
        >>> my_acct.transfer(200, "example2@mail.mcgill.ca")
        AssertionError: User balance (-1) is not sufficient for transfer
        >>> Account("example@mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        200
        >>> my_acct.transfer(200, "example@mail.mcgill.ca")
        AssertionError: Please ensure your email is not your own, and is in valid mcgill.ca form
        """
        if type(coins) != int or type(email) != str:
            raise AssertionError('Please enter coin amount and emial of the valid types! (int, str)')
        if email[-9:] != 'mcgill.ca' or self.email == email:
            raise AssertionError('Please ensure your email is not your own, and is in valid mcgill.ca form')
        if self.balance == -1:
            raise AssertionError('User balance (-1) is not sufficient for transfer')
        if  coins <= 0:
            raise AssertionError('Please enter a valid, non-negative number of coins to transfer')
        if  self.balance < coins:
            raise AssertionError('Insufficient funds for transfer!')
                
        transfer_dict = {'withdrawal_email': self.email, 'token': self.token, 'deposit_email': email, 'amount': str(coins)}
        
        transfer_result = self.call_api('transfer', transfer_dict)
        
        return transfer_result['message']