import utils


def get_entry_for_sender(sender, seen_email_data):
	return sender in seen_email_data.keys()


def update_for_sent_voters(sender, voters_to_add, seen_email_data):
	sender = utils.reformat_email_address(sender) # note that it was probably already reformatted by NewEmail
	
	if get_entry_for_sender(sender, seen_email_data):
		seen_email_data[sender] = add_voters_to_entry(voters_to_add, seen_email_data[sender])
	else:
		seen_email_data = add_entry(sender, voters_to_add, seen_email_data)
	return seen_email_data


def mark_existing_entry_active(sender, seen_email_data):
	seen_email_data[sender]['active'] = 'y'


def mark_existing_entry_inactive(sender, seen_email_data):
	seen_email_data[sender]['active'] = 'n'


def add_voters_to_entry(voters_to_add, entry):
	for voter in voters_to_add:
		if voter in entry['voters']:
			msg = "Already tried to add voter '{0}' to entry for {1}".format(voter, entry['sender'])
			raise RuntimeError(msg)
		entry['voters'].append(voter)
	return entry


def add_entry(new_sender, voters_to_add, seen_email_data):
	new_entry = {'sender':new_sender, 'voters':voters_to_add}
	seen_email_data[new_sender] = new_entry
	return seen_email_data
