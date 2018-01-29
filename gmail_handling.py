
def get_unread_email_ids(gmail_client):
    """
    return list of id of unread emails
    """
    #response = gmail_client.users().messages().list(userId='me',q='is:unread').execute()
    response = gmail_client.users().messages().list(userId='me').execute()

    if 'messages' in response: # messages key only exists if there are unread messages
        ids = [message['id'] for message in response['messages']]
        ids.reverse() # ids comes most to least recent; we want vice versa
        return ids
    else:
        print("No unread messages...")
        return [] # still return a list since that's what caller expects


def get_emails(client, email_ids):
    return [(this_id, client.users().messages().get(userId='me', id=this_id).execute()) for this_id in email_ids]


def mark_as_read(client, email_ids):
    print("Marking the following ids as read: {0}".format(email_ids))
    pass