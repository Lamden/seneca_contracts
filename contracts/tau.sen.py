from seneca.libs.datatypes import hmap

# Declare Data Types
xrate = hmap('xrate', str, float)
balances = hmap('balances', str, int)
custodials = hmap('custodials', str, hmap(key_type=str, value_type=int))



@seed
def initialize_contract():

    # Initialization
    xrate['TAU_STP'] = 1.0
    balances['LamdenReserves'] = 0

    # Deposit to all network founders
    ALL_WALLETS = [
        '324ee2e3544a8853a3c5a0ef0946b929aa488cbe7e7ee31a0fef9585ce398502',
        'a103715914a7aae8dd8fddba945ab63a169dfe6e37f79b4a58bcf85bfd681694',
        '20da05fdba92449732b3871cc542a058075446fedb41430ee882e99f9091cc4d',
        'ed19061921c593a9d16875ca660b57aa5e45c811c8cf7af0cfcbd23faa52cbcd',
        'cb9bfd4b57b243248796e9eb90bc4f0053d78f06ce68573e0fdca422f54bb0d2',
        'c1f845ad8967b93092d59e4ef56aef3eba49c33079119b9c856a5354e9ccdf84'
    ]
    SEED_AMOUNT = 1000000

    for w in ALL_WALLETS:
        balances[w] = SEED_AMOUNT

@export
def submit_stamps(stamps):
    assert stamps > 0, "Stamps supplied must be non-negative"
    if xrate['TAU_STP'] == 0:
        xrate['TAU_STP'] = 1.0
    amount = stamps * xrate['TAU_STP']
    balances[rt['origin']] -= amount
    balances['LamdenReserves'] += amount
    sender_balance = balances[rt['origin']]
    assert sender_balance >= 0, "Not enough funds to submit stamps"

@export
def transfer(to, amount):
    assert stamps > 0, "Transfer amount must be non-negative."
    assert balances[rt['sender']] >= amount, "Not enough funds to transfer"
    balances[to] += amount
    balances[rt['sender']] -= amount

@export
def add_to_custodial(to, amount):
    assert balances[rt['sender']] >= amount, "Not enough funds to add to custodial"
    custodials[rt['sender']][to] += amount
    balances[rt['sender']] -= amount

@export
def remove_from_custodial(to, amount):
    assert custodials[rt['sender']][to] >= amount, "Not enough allowance in custodial"
    balances[rt['sender']] += amount
    custodials[rt['sender']][to] -= amount

@export
def spend_custodial(_from, amount, to):
    assert custodials[_from][rt['sender']] >= amount, 'Not enough allowance to spend in custodial'
    balances[to] += amount
    custodials[_from][rt['sender']] -= amount

@export
def get_balance(account):
    return balances[account]

@export
def get_custodial(owner, spender):
    return custodials[owner][spender]
