from seneca.storage import tabular as st
from seneca.stdlib.functools import partial
from seneca import crypto
from seneca.runtime import state as rt_state
from seneca.modulelib import make_exports

prefix = 'dapp'
minimum_length = 8

def claim_name(domain, contract):
	assert len(domain) >= minimum_length
	assert not does_resolve(domain)
	domains.insert(owner=author, name=domain, contract=contract)

def does_resolve(domain):
	return bool(domains.select().where(name=domain).run())

def resolve(domain):
	assert does_resolve(domain)
	return domains.select('contract').where(name=domain).run()

if __name__ == '__main__':
    domains = st.create_table('domain', {
      'owner': st.column(int, unique=True),
      'name': st.column(str),
      'contract': st.column(int)
    })