import json

from eth_account.datastructures import (
    SignedTransaction
)

from decimal import (
    Decimal,
    InvalidOperation
)

from .account import (
    get_balance,
    is_valid_address
)

from .numbers import (
    convert_one_to_atto
)

from .exceptions import (
    InvalidValidatorError,
    RPCError,
    RequestsError,
    RequestsTimeoutError
)

from .staking import (
    get_all_validator_addresses,
    get_validator_information
)

from .staking_structures import (
    Directive
)

from .staking_signing import (
    sign_staking_transaction
)

_default_endpoint = 'http://localhost:9500'
_default_timeout = 30

# TODO: Add unit testing
class Validator:

    name_char_limit = 140
    identity_char_limit = 140
    website_char_limit = 140
    security_contact_char_limit = 140
    details_char_limit = 280
    min_required_delegation = convert_one_to_atto(10000)        # in ATTO

    def __init__(self, address):
        if not isinstance(address, str):
            raise InvalidValidatorError(1, 'given ONE address was not a string')
        if not is_valid_address(address):
            raise InvalidValidatorError(1, f'{address} is not valid ONE address')
        self._address = address
        self._bls_keys = []

        self._name = None
        self._identity = None
        self._website = None
        self._details = None
        self._security_contact = None

        self._min_self_delegation = None
        self._max_total_delegation = None
        self._inital_delegation = None

        self._rate = None
        self._max_change_rate = None
        self._max_rate = None

    def _sanitize_input(self, data, check_str=False) -> str:
        """
        If data is None, return '' else return data

        Raises
        ------
        InvalidValidatorError if check_str is True and str is not passed
        """
        if check_str:
            if not isinstance(data, str):
                raise InvalidValidatorError(3, f'Expected data to be string to avoid floating point precision issues but got {data}')
        return '' if not data else str(data)

    def __str__(self) -> str:
        """
        Returns JSON string representation of Validator fields
        """
        info = self.export()
        for key, value in info.items():
            if isinstance(value, Decimal):
                info[key] = str(value)
        return json.dumps(info)

    def __repr__(self) -> str:
        return f'<Validator: {hex(id(self))}>'

    def get_address(self) -> str:
        """
        Get validator address

        Returns
        -------
        str
            Validator address
        """
        return self._address

    def add_bls_key(self, key) -> bool:
        """
        Add BLS public key to validator BLS keys if not already in list

        Returns
        -------
        bool
            If adding BLS key succeeded
        """
        key = self._sanitize_input(key)
        if key not in self._bls_keys:
            self._bls_keys.append(key)
            return True
        return False

    def remove_bls_key(self, key) -> bool:
        """
        Remove BLS public key from validator BLS keys if exists

        Returns
        -------
        bool
            If removing BLS key succeeded
        """
        key = self._sanitize_input(key)
        if key in self._bls_keys:
            self._bls_keys.remove(key)
            return True
        return False

    def get_bls_keys(self) -> list:
        """
        Get list of validator BLS keys

        Returns
        -------
        list
            List of validator BLS keys (strings)
        """
        return self._bls_keys

    def set_name(self, name):
        """
        Set validator name

        Parameters
        ----------
        name: str
            Name of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        name = self._sanitize_input(name)
        if len(name) > self.name_char_limit:
            raise InvalidValidatorError(3, f'Name must be less than {self.name_char_limit} characters')
        self._name = name

    def get_name(self) -> str:
        """
        Get validator name

        Returns
        -------
        str
            Validator name
        """
        return self._name

    def set_identity(self, identity):
        """
        Set validator identity

        Parameters
        ----------
        identity: str
            Identity of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        identity = self._sanitize_input(identity)
        if len(identity) > self.identity_char_limit:
            raise InvalidValidatorError(3, f'Identity must be less than {self.identity_char_limit} characters')
        self._identity = identity

    def get_identity(self) -> str:
        """
        Get validator identity

        Returns
        -------
        str
            Validator identity
        """
        return self._identity

    def set_website(self, website):
        """
        Set validator website

        Parameters
        ----------
        website: str
            Website of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        website = self._sanitize_input(website)
        if len(website) > self.website_char_limit:
            raise InvalidValidatorError(3, f'Website must be less than {self.website_char_limit} characters')
        self._website = website

    def get_website(self) -> str:
        """
        Get validator website

        Returns
        -------
        str
            Validator website
        """
        return self._website

    def set_security_contact(self, contact):
        """
        Set validator security contact

        Parameters
        ----------
        contact: str
            Security contact of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        contact = self._sanitize_input(contact)
        if len(contact) > self.security_contact_char_limit:
            raise InvalidValidatorError(3, f'Security contact must be less than {self.security_contact_char_limit} characters')
        self._security_contact = contact

    def get_security_contact(self) -> str:
        """
        Get validator security contact

        Returns
        -------
        str
            Validator security contact
        """
        return self._security_contact

    def set_details(self, details):
        """
        Set validator details

        Parameters
        ----------
        details: str
            Details of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        details = self._sanitize_input(details)
        if len(details) > self.details_char_limit:
            raise InvalidValidatorError(3, f'Details must be less than {self.details_char_limit} characters')
        self._details = details

    def get_details(self) -> str:
        """
        Get validator details

        Returns
        -------
        str
            Validator details
        """
        return self._details

    def set_min_self_delegation(self, delegation):
        """
        Set validator min self delegation

        Parameters
        ----------
        delegation: int
            Minimum self delegation of validator in ATTO

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        delegation = self._sanitize_input(delegation)
        try:
            delegation = Decimal(delegation)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Min self delegation must be a number') from e
        if delegation < self.min_required_delegation:
            raise InvalidValidatorError(3, f'Min self delegation must be greater than {self.min_required_delegation} ATTO')
        self._min_self_delegation = delegation

    def get_min_self_delegation(self) -> Decimal:
        """
        Get validator min self delegation

        Returns
        -------
        Decimal
            Validator min self delegation in ATTO
        """
        return self._min_self_delegation

    def set_max_total_delegation(self, max_delegation):
        """
        Set validator max total delegation

        Parameters
        ----------
        max_delegation: int
            Maximum total delegation of validator in ATTO

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        max_delegation = self._sanitize_input(max_delegation)
        try:
            max_delegation = Decimal(max_delegation)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Max total delegation must be a number') from e
        if self._min_self_delegation:
            if max_delegation < self._min_self_delegation:
                raise InvalidValidatorError(3, f'Max total delegation must be greater than min self delegation: '
                                               '{self._min_self_delegation}')
        else:
            raise InvalidValidatorError(4, 'Min self delegation must be set before max total delegation')
        self._max_total_delegation = max_delegation

    def get_max_total_delegation(self) -> Decimal:
        """
        Get validator max total delegation

        Returns
        -------
        Decimal
            Validator max total delegation in ATTO
        """
        return self._max_total_delegation

    def set_amount(self, amount):
        """
        Set validator initial delegation amount

        Parameters
        ----------
        amount: str
            Initial delegation amount of validator in ATTO

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        amount = self._sanitize_input(amount)
        try:
            amount = Decimal(amount)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Amount must be a number') from e
        if self._min_self_delegation:
            if amount < self._min_self_delegation:
                raise InvalidValidatorError(3, 'Amount must be greater than min self delegation: '
                                               f'{self._min_self_delegation}')
        else:
            raise InvalidValidatorError(4, 'Min self delegation must be set before amount')
        if self._max_total_delegation:
            if amount > self._max_total_delegation:
                raise InvalidValidatorError(3, 'Amount must be less than max total delegation: '
                                               f'{self._max_total_delegation}')
        else:
            raise InvalidValidatorError(4, 'Max total delegation must be set before amount')
        self._inital_delegation = amount

    def get_amount(self) -> Decimal:
        """
        Get validator initial delegation amount

        Returns
        -------
        Decimal
            Intended initial delegation amount in ATTO
        """
        return self._inital_delegation

    def set_max_rate(self, rate):
        """
        Set validator max commission rate

        Parameters
        ----------
        rate: str (to avoid precision troubles)
            Max commission rate of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        rate = self._sanitize_input(rate, True)
        try:
            rate = Decimal(rate)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Max rate must be a number') from e
        if rate < 0 or rate > 1:
            raise InvalidValidatorError(3, 'Max rate must be between 0 and 1')
        self._max_rate = rate

    def get_max_rate(self) -> Decimal:
        """
        Get validator max commission rate

        Returns
        -------
        Decimal
            Validator max rate
        """
        return self._max_rate

    def set_max_change_rate(self, rate):
        """
        Set validator max commission change rate

        Parameters
        ----------
        rate: str (to avoid precision troubles)
            Max commission change rate of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        rate = self._sanitize_input(rate, True)
        try:
            rate = Decimal(rate)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Max change rate must be a number') from e
        if rate < 0:
            raise InvalidValidatorError(3, 'Max change rate must be greater than or equal to 0')
        if self._max_rate:
            if rate > self._max_rate:
                raise InvalidValidatorError(3, f'Max change rate must be less than or equal to max rate: {self._max_rate}')
        else:
            raise InvalidValidatorError(4, 'Max rate must be set before max change rate')
        self._max_change_rate = rate

    def get_max_change_rate(self) -> Decimal:
        """
        Get validator max commission change rate

        Returns
        -------
        Decimal (to avoid precision troubles)
            Validator max change rate
        """
        return self._max_change_rate

    def set_rate(self, rate):
        """
        Set validator commission rate

        Parameters
        ----------
        rate: str (to avoid precision troubles)
            Commission rate of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        rate = self._sanitize_input(rate, True)
        try:
            rate = Decimal(rate)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Rate must be a number') from e
        if rate < 0:
            raise InvalidValidatorError(3, 'Rate must be greater than or equal to 0')
        if self._max_rate:
            if rate > self._max_rate:
                raise InvalidValidatorError(3, f'Rate must be less than or equal to max rate: {self._max_rate}')
        else:
            raise InvalidValidatorError(4, 'Max rate must be set before rate')
        self._rate = rate

    def get_rate(self) -> Decimal:
        """
        Get validator commission rate

        Returns
        -------
        Decimal
            Validator rate
        """
        return self._rate

    def does_validator_exist(self, endpoint=_default_endpoint, timeout=_default_timeout) -> bool:
        """
        Check if validator exists on blockchain

        Parameters
        ----------
        endpoint: :obj:`str`, optional
            Endpoint to send request to
        timeout: :obj:`int`, optional
            Timeout in seconds

        Returns
        -------
        bool
            Does validator exist on chain

        Raises
        ------
        RPCError, RequestsError, RequestsTimeoutError
            If unable to get list of validators on chain
        """
        all_validators = get_all_validator_addresses(endpoint, timeout)
        if self._address in all_validators:
            return True
        return False

    def load(self, info):
        """
        Import validator information

        Parameters
        ----------
        info: dict
            Validator information with dictionary
            Will ignore any extra fields in the input dictionary
            Example input:
            {
                "name": "",
                "website": "",
                "security-contact": "",
                "identity": "",
                "details": "",
                "amount": 0,
                "min-self-delegation": 0,
                "max-total-delegation": 0,
                "rate": '0',
                "max-rate": '0',
                "max-change-rate": '0',
                "bls-public-keys": [ "" ]
            }

        Raises
        ------
        InvalidValidatorError
            If input value is invalid
        """
        try:
            self.set_name(info['name'])
            self.set_identity(info['identity'])
            self.set_website(info['website'])
            self.set_details(info['details'])
            self.set_security_contact(info['security-contact'])

            self.set_min_self_delegation(info['min-self-delegation'])
            self.set_max_total_delegation(info['max-total-delegation'])
            self.set_amount(info['amount'])

            self.set_max_rate(info['max-rate'])
            self.set_max_change_rate(info['max-change-rate'])
            self.set_rate(info['rate'])

            self._bls_keys = []
            for key in info['bls-public-keys']:
                self.add_bls_key(key)
        except KeyError as e:
            raise InvalidValidatorError(3, 'Info has missing key') from e

    def load_from_blockchain(self, endpoint=_default_endpoint, timeout=_default_timeout):
        """
        Import validator information from blockchain with given address

        Parameters
        ----------
        endpoint: :obj:`str`, optional
            Endpoint to send request to
        timeout: :obj:`int`, optional
            Timeout in seconds

        Raises
        ------
        InvalidValidatorError
            If any error occur getting & importing validator information from the blockchain
        """
        try:
            if not self.does_validator_exist(endpoint, timeout):
                raise InvalidValidatorError(5, f'Validator does not exist on chain according to {endpoint}')
        except (RPCError, RequestsError, RequestsTimeoutError) as e:
            raise InvalidValidatorError(5, 'Error requesting validator information') from e
        try:
            validator_info = get_validator_information(self._address, endpoint, timeout)
        except (RPCError, RequestsError, RequestsTimeoutError) as e:
            raise InvalidValidatorError(5, 'Error requesting validator information') from e

        # Skip additional sanity checks when importing from chain
        try:
            info = validator_info['validator']
            self._name = info['name']
            self._identity = info['identity']
            self._website = info['website']
            self._details = info['details']
            self._security_contact = info['security-contact']

            self._min_self_delegation = info['min-self-delegation']
            self._max_total_delegation = info['max-total-delegation']
            self._inital_delegation = self._min_self_delegation  # Since validator exists, set initial delegation to 0

            self._max_rate = Decimal(info['max-rate'])
            self._max_change_rate = Decimal(info['max-change-rate'])
            self._rate = Decimal(info['rate'])
            self._bls_keys = info[ 'bls-public-keys' ]
        except KeyError as e:
            raise InvalidValidatorError(5, 'Error importing validator information from RPC result') from e

    def export(self) -> dict:
        """
        Export validator information as dict

        Returns
        -------
        dict
            Dictionary representation of validator
        """
        info = {
            "validator-addr": self._address,
            "name": self._name,
            "website": self._website,
            "security-contact": self._security_contact,
            "identity": self._identity,
            "details": self._details,
            "amount": self._inital_delegation,
            "min-self-delegation": self._min_self_delegation,
            "max-total-delegation": self._max_total_delegation,
            "rate": self._rate,
            "max-rate": self._max_rate,
            "max-change-rate": self._max_change_rate,
            "bls-public-keys": self._bls_keys
        }
        return info

    def sign_create_validator_transaction(self, nonce, gas_price, gas_limit, private_key, chain_id=None) -> SignedTransaction:
        """
        Create but not post a transaction to Create the Validator using private_key

        Returns
        -------
        SignedTransaction object, the hash of which can be used to send the transaction
            using transaction.send_raw_transaction

        Raises
        ------
        rlp.exceptions.ObjectSerializationError for malformed inputs

        API Reference
        -------------
        https://github.com/harmony-one/sdk/blob/99a827782fabcd5f91f025af0d8de228956d42b4/packages/harmony-staking/src/stakingTransaction.ts#L413
        """
        info = self.export().copy()
        info['directive'] = Directive.CreateValidator
        info['validatorAddress'] = info.pop('validator-addr')   # change the key
        info['nonce'] = nonce
        info['gasPrice'] = gas_price
        info['gasLimit'] = gas_limit
        if chain_id:
            info['chainId'] = chain_id
        return sign_staking_transaction(info, private_key)

    def sign_edit_validator_transaction(self, nonce, gas_price, gas_limit, rate, bls_key_to_add, bls_key_to_remove, private_key, chain_id=None) -> SignedTransaction:
        """
        Create but not post a transaction to Edit the Validator using private_key

        Returns
        -------
        SignedTransaction object, the hash of which can be used to send the transaction
            using transaction.send_raw_transaction

        Raises
        ------
        rlp.exceptions.ObjectSerializationError for malformed inputs

        API Reference
        -------------
        https://github.com/harmony-one/sdk/blob/99a827782fabcd5f91f025af0d8de228956d42b4/packages/harmony-staking/src/stakingTransaction.ts#L460
        """
        self.set_rate(rate)
        self.add_bls_key(bls_key_to_add)
        self.remove_bls_key(bls_key_to_remove)
        info = self.export().copy()
        info['directive'] = Directive.EditValidator
        info['validatorAddress'] = info.pop('validator-addr')   # change the key
        info['nonce'] = nonce
        info['gasPrice'] = gas_price
        info['gasLimit'] = gas_limit
        _ = info.pop('max-rate')            # not needed
        _ = info.pop('max-change-rate')     # not needed
        _ = info.pop('bls-public-keys')     # remove this list
        _ = info.pop('amount')              # also unused
        info['bls-key-to-remove'] = bls_key_to_remove
        info['bls-key-to-add'] = bls_key_to_add
        if chain_id:
            info['chainId'] = chain_id
        return sign_staking_transaction(info, private_key)