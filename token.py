'''
Implementation of a token that is similar to the ERC20 token on Ethereum
'''

from seneca.storage import tabular as st
from seneca.stdlib.functools import partial
from seneca import crypto
from seneca.runtime import state as rt_state
from seneca.modulelib import make_exports

token_name = 'Lamden Tau'
symbol = 'TAU'
total_supply = 288090567

# 2 new methods added to the original erc20 interface to comply with lamden's
# tabular table store
def create_wallet:
	assert not wallet_exists(author)
	ledger.insert(owner=author, balance=0)

def wallet_exists(wallet):
	return bool(ledger.select('owner').where(owner=owner).run())

def raw_transfer(to, _from, amount):
	assert wallet_exists(_from)
	assert wallet_exists(to)

	sender_balance = ledger.select('balance').where(wallet_id=_from).run()[0]
	assert amount >= sender_balance

	new_sender_balance = sender_balance - amount

	reciever_balance = ledger.select('balance').where(wallet_id=_from).run()[0]

	new_reciever_balance = reciever_balance + amount

	ledger.update(balance=new_sender_balance).where(owner=_from)
	ledger.update(balance=new_reciever_balance).where(owner=to)

def balance_of(wallet):
	return ledger.select('balance').where(owner=author).run()[0]

def transfer(to, amount):
	raw_transfer(to, author, amount)

def allowance(owner, sender):
	return allowances.select('amount').where(owner=owner, sender=sender).run()[0]

def approve(sender, amount):
	allowances.update(amount=amount).where(owner=author, sender=sender).run()[0]
	return amount

def transfer_from(owner, reciever, amount):
	current_allowance = allowance(owner, amount)

	assert current_allowance >= amount

	raw_transfer(reciever, owner, amount)

	new_allowance = current_allowance - amount
	allowances.update(amount=new_allowance).where(owner=owner, sender=sender)

if __name__ == '__main__':
    ledger = st.create_table('ledger', {
      'owner': st.column(int, unique=True),
      'balance': st.column(int),
    })

    allowances = st.create_table('allowances', {
    	'owner': st.column(int),
    	'sender': st.column(int),
    	'amount'L st.column(int),
    })

    exports = make_exports(
    	token_name,
		symbol,
		total_supply,
		create_wallet,
		wallet_exists,
		total_supply,
		balance_of,
		transfer,
		allowance,
		approve,
		transfer_from
	)
