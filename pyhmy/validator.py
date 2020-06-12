import json

from decimal import (
    Decimal,
    InvalidOperation
)

from .account import (
    get_balance,
    is_valid_address
)

from .exceptions import (
    InvalidValidatorError,
    RPCError,
    RequestsError,
    RequestsTimeoutError
)

from .numbers import (
    convert_atto_to_one,
    convert_one_to_atto
)

from .staking import (
    get_all_validator_addresses,
    get_validator_information
)


_default_endpoint = 'http://localhost:9500'
_default_timeout = 30


# TODO: Add validator transcation functions
# TODO: Add unit testing
class Validator:

    name_char_limit = 140
    identity_char_limit = 140
    website_char_limit = 140
    security_contact_char_limit = 140
    details_char_limit = 280
    min_required_delegation = 10000

    def __init__(self, address):
        if not isinstance(address, str):
            raise InvalidValidatorError(1, f'given ONE address was not a string.')
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
            List of validator BLS keys
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
        if not name:
            name = ''
        name = str(name)
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
        if not identity:
            identity = ''
        identity = str(identity)
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
        if not website:
            website = ''
        website = str(website)
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
        if not contact:
            contact = ''
        contact = str(contact)
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
        if not details:
            details = ''
        details = str(details)
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
        delegation: str
            Minimum self delegation of validator in ONE

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        try:
            delegation = Decimal(delegation)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, f'Min self delegation must be a number') from e
        if delegation < self.min_required_delegation:
            raise InvalidValidatorError(3, f'Min self delegation must be greater than {self.min_required_delegation} ONE')
        self._min_self_delegation = delegation.normalize()

    def get_min_self_delegation(self) -> Decimal:
        """
        Get validator min self delegation

        Returns
        -------
        Decimal
            Validator min self delegation in ONE
        """
        return self._min_self_delegation

    def set_max_total_delegation(self, max):
        """
        Set validator max total delegation

        Parameters
        ----------
        max: str
            Maximum total delegation of validator in ONE

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        try:
            max = Decimal(max)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, 'Max total delegation must be a number') from e
        if self._min_self_delegation:
            if max < self._min_self_delegation:
                raise InvalidValidatorError(3, f'Max total delegation must be greater than min self delegation: '
                                               f'{self._min_self_delegation}')
        else:
            raise InvalidValidatorError(4, 'Min self delegation must be set before max total delegation')
        self._max_total_delegation = max.normalize()

    def get_max_total_delegation(self) -> Decimal:
        """
        Get validator max total delegation

        Returns
        -------
        Decimal
            Validator max total delegation in ONE
        """
        return self._max_total_delegation

    def set_amount(self, amount):
        """
        Set validator initial delegation amount

        Parameters
        ----------
        amount: str
            Initial delegation amount of validator in ONE

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        try:
            amount = Decimal(amount)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, f'Amount must be a number') from e
        if self._min_self_delegation:
            if amount < self._min_self_delegation:
                raise InvalidValidatorError(3, f'Amount must be greater than min self delegation: '
                                               f'{self._min_self_delegation}')
        else:
            raise InvalidValidatorError(4, f'Min self delegation must be set before amount')
        if self._max_total_delegation:
            if amount > self._max_total_delegation:
                raise InvalidValidatorError(3, f'Amount must be less than max total delegation: '
                                               f'{self._max_total_delegation}')
        else:
            raise InvalidValidatorError(4, f'Max total delegation must be set before amount')
        self._inital_delegation = amount.normalize()

    def get_amount(self) -> Decimal:
        """
        Get validator initial delegation amount

        Returns
        -------
        Decimal
            Intended initial delegation amount in ONE
        """
        return self._inital_delegation

    def set_max_rate(self, rate):
        """
        Set validator max commission rate

        Parameters
        ----------
        rate: str
            Max commission rate of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        try:
            rate = Decimal(rate)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, f'Max rate must be a number') from e
        if rate < 0 or rate > 1:
            raise InvalidValidatorError(3, f'Max rate must be between 0 and 1')
        self._max_rate = rate.normalize()

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
        rate: str
            Max commission change rate of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        try:
            rate = Decimal(rate)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, f'Max change rate must be a number') from e
        if rate < 0:
            raise InvalidValidatorError(3, f'Max change rate must be greater than or equal to 0')
        if self._max_rate:
            if rate > self._max_rate:
                raise InvalidValidatorError(3, f'Max change rate must be less than or equal to max rate: {self._max_rate}')
        else:
            raise InvalidValidatorError(4, f'Max rate must be set before max change rate')
        self._max_change_rate = rate.normalize()

    def get_max_change_rate(self) -> Decimal:
        """
        Get validator max commission change rate

        Returns
        -------
        Decimal
            Validator max change rate
        """
        return self._max_change_rate

    def set_rate(self, rate):
        """
        Set validator commission rate

        Parameters
        ----------
        rate: str
            Commission rate of validator

        Raises
        ------
        InvalidValidatorError
            If input is invalid
        """
        try:
            rate = Decimal(rate)
        except (TypeError, InvalidOperation) as e:
            raise InvalidValidatorError(3, f'Rate must be a number') from e
        if rate < 0:
            raise InvalidValidatorError(3, f'Rate must be greater than or equal to 0')
        if self._max_rate:
            if rate > self._max_rate:
                raise InvalidValidatorError(3, f'Rate must be less than or equal to max rate: {self._max_rate}')
        else:
            raise InvalidValidatorError(4, f'Max rate must be set before rate')
        self._rate = rate.normalize()

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
                "rate": 0,
                "max-rate": 0,
                "max-change-rate": 0
            }

        Raises
        ------
        InvalidValidatorError
            If input value is invalid
        """
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
            raise InvalidValidatorError(5, f'Error requesting validator information') from e
        try:
            validator_info = get_validator_information(self._address, endpoint, timeout)
        except (RPCError, RequestsError, RequestsTimeoutError) as e:
            raise InvalidValidatorError(5, f'Error requesting validator information') from e

        # Skip additional sanity checks when importing from chain
        try:
            info = validator_info['validator']
            self._name = info['name']
            self._identity = info['identity']
            self._website = info['website']
            self._details = info['details']
            self._security_contact = info['security-contact']

            self._min_self_delegation = convert_atto_to_one(info['min-self-delegation']).normalize()
            self._max_total_delegation = convert_atto_to_one(info['max-total-delegation']).normalize()
            self._inital_delegation = Decimal(0)  # Since validator exists, set initial delegation to 0

            self._max_rate = Decimal(info['max-rate']).normalize()
            self._max_change_rate = Decimal(info['max-change-rate']).normalize()
            self._rate = Decimal(info['rate']).normalize()
        except KeyError as e:
            raise InvalidValidatorError(5, f'Error importing validator information from RPC result') from e

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
            "max-change-rate": self._max_change_rate
        }
        return info
