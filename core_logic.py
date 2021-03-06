import gmail_handling
import data_handling
import config
import secret
import utils


def decide_what_to_do_with_email(newemail):

	if newemail.should_ignore:
		handler = None
		is_expected = True
		return handler, is_expected

	else:
		# FIRST TAKE CARE OF ALL THE SCENARIOS WITH CONDITIONS THAT WILL REQUIRE MANUAL REVIEW TO
		# DETERMINE COURSE OF ACTION
		# Note that there are other unexpected scenarios that will be logged as abnormal but which
		# we will have an autmoated response to... those are further down
		unexpected_scenarios = [
			# shouldn't get a surrender and an attach in one
			(newemail.from_active, newemail.surrender, newemail.attach),
			# shouldn't get an attach from someone who is inactive
			(not newemail.from_active, newemail.attach),
			# shouldn't get a surrender from an inactive/unseen
			(not newemail.from_active, newemail.surrender),
			# shouldn't get any of those special things on an unseen
			(not newemail.from_seen, newemail.attach or newemail.surrender or newemail.asks_for_more)
		]

		for scenario_conditions in unexpected_scenarios:
			if all(scenario_conditions):
				handler = None
				is_expected = False
				return handler, is_expected

		if newemail.from_seen:
			return decide_what_to_do_with_seen_emailer_email(newemail)
		else:
			# already eliminated all the other scenarios...
			return send_voters_handler, True


def decide_what_to_do_with_seen_emailer_email(newemail):

	if newemail.from_active:

		if newemail.attach:
			is_expected = True
			if newemail.asks_for_more:
				handler = send_voters_handler
			else:
				handler = inquire_about_more_handler
		else:
			if newemail.surrender:
				is_expected = True
				handler = surrender_handler
			else:
				is_expected = False
				handler = reminder_of_options_handler

	# EMAILERS WE HAVE PREVIOUSLY SEEN but WHO ARE 'INACTIVE'
	# already covered most of these scenarios in 'unexpected_scenarios'
	else:
		if newemail.asks_for_more:
			is_expected = True
			handler = send_voters_handler
		else:
			is_expected = False
			handler = reminder_of_options_handler

	return handler, is_expected


# EACH OF THESE FUNCTIONS REPLIES APPROPRIATELY (if applicable) AND ADJUSTS SEEN_EMAIL_DATA 
# AND UNUSED_VOTERS APPROPRIATELY (if applicable)
def send_voters_handler(newemail, seen_email_data, unused_voters, gmail_client):
	# get message from secret (apart from the voters)
	# get voters
	# combine
	# send to newemail.sender using gmail_handling
	# add voters to newemail.sender's entry (and create entry if necessary)
	# change/leave entry['active'] to 'y'
	# delete voters
	intro_message = config.BOT_MESSAGES['MESSAGE_WHEN_SENDING_VOTERS']
	voters_to_add = data_handling.get_voters(unused_voters, config.NUMBER_OF_VOTERS_TO_SEND)
	pretty_voters = utils.pretty_format_voters(voters_to_add)
	message = intro_message + "\n\n" + pretty_voters
	gmail_handling.send_email(gmail_client, newemail.sender, message)
	seen_email_data = data_handling.update_for_sent_voters(newemail.sender, voters_to_add, seen_email_data)
	seen_email_data = data_handling.mark_existing_entry_active(newemail.sender, seen_email_data)
	data_handling.delete_voters(unused_voters, voters_to_add)
	print("replied to {0} with voters".format(newemail.sender))
	return seen_email_data, unused_voters


def inquire_about_more_handler(newemail, seen_email_data, unused_voters, gmail_client):
	# get message from secret
	# send to newemail.sender using gmail_handling
	# change entry['active'] to 'n'
	message = config.BOT_MESSAGES['MESSAGE_FOR_ASKING_IF_PEOPLE_WANT_MORE']
	gmail_handling.send_email(gmail_client, newemail.sender, message)
	seen_email_data = data_handling.mark_existing_entry_inactive(newemail.sender, seen_email_data)
	print("replied to {0} with inquiry about more".format(newemail.sender))
	return seen_email_data, unused_voters


def reminder_of_options_handler(newemail, seen_email_data, unused_voters, gmail_client):
	# get message from secret
	# send to newemail.sender using gmail_handling
	message = config.BOT_MESSAGES['MESSAGE_WHEN_BOT_DOESNT_UNDERSTAND']
	gmail_handling.send_email(gmail_client, newemail.sender, message)
	print("replied to {0} with did not understand/reminder of options".format(newemail.sender))
	return seen_email_data, unused_voters


def surrender_handler(newemail, seen_email_data, unused_voters, gmail_client):
	# get message from secret
	# send to newemail.sender using gmail_handling
	# change entry['active'] to 'n'
	message = config.BOT_MESSAGES['MESSAGE_WHEN_SOMEONE_CANT_MAIL_THEIR_VOTERS']
	gmail_handling.send_email(gmail_client, newemail.sender, message)
	seen_email_data = data_handling.mark_existing_entry_inactive(newemail.sender, seen_email_data)
	print("replied to {0} with thanks for surrender".format(newemail.sender))
	return seen_email_data, unused_voters




