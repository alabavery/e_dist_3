import re

import utils
import secret


class NewEmail:

    def __init__(self, email_id, raw_email_datum, seen_email_data):
        self.email_id = email_id
        self.raw = raw_email_datum
        self.sender = self.extract_sender()
        self.should_ignore = self.should_we_ignore()

        if not self.should_ignore: # just skip these if we're ignoring it anyway
            self.attach = self.extract_attach()
            self.text = self.extract_part_of_snippet()
            self.surrender = self.find_key_phrase(secret.SURRENDER_KEY_PHRASE)
            self.asks_for_more = self.find_key_phrase(secret.ASK_FOR_MORE_KEY_PHRASE)
            self.from_seen = self.determine_if_seen(seen_email_data)
            self.from_active = self.is_from_active(seen_email_data)


    def find_email_substring(self, email_string):
        substrings = email_string.split(' ')
        email_substring = [ss for ss in substrings if '@' in ss]
        if len(email_substring) == 1:
            return email_substring[0]
        return False


    def should_we_ignore(self):
        return (self.sender == secret.THE_EMAIL) or ('google' in self.sender)


    def extract_sender(self):
        headers = self.raw['payload']['headers']
        return_path = [header for header in headers if header['name'].lower() == 'return-path']
        if return_path:
            sender = return_path[0]['value']
        else:
            sender = [header for header in headers if header['name'].lower() == 'from'][0]['value']

        sender = self.find_email_substring(sender)
        if sender:
            return utils.reformat_email_address(sender)
        else:
            raise RuntimeError("Couldn't find sender!")


    def extract_attach(self):
        pass


    def extract_part_of_snippet(self):
        """
        We are going to use snippet as a proxy for message text.  However, in replies, the
        snippet can (always does?) contain some of the previous messages' text.  But, these
        previous messages will be proceeded by a date header (e.g. 'On Tue, Jan 19 at 12:30).
        May God grant us the grace of making that heading always be there.
        :return: the part of the raw message snippet before the first date/time heading
        """
        snippet = self.raw['snippet']
        pattern = re.compile("On \D\D\D, \D\D\D \d+, \d\d\d\d at \d+:\d\d")
        found_date_heading_at = pattern.search(snippet)

        if found_date_heading_at != None:
            return snippet[:found_date_heading_at.start()]
        else:
            return snippet

    # def extract_text(self):
    #     """
    #     Let's make assumption that the most recent message will always be in one of the following two positions:
    #     - message_data.get('payload').get('body').get('data')
    #     - message_data.get('payload').get('parts')[0].get('body').get('data')
    #     - if multiple messages seem to be included here, then all text preceding the first 'On Tue, Nov 28, 2017 at 7:48 PM'
    #
    #     """
    #     payload = self.raw.get('payload')
    #
    #     if payload.get('body').get('data'):
    #         encoded_return = payload.get('body').get('data')
    #     else:
    #         # REALLY NEED TO MAKE SURE THIS IS ACTUALLY GETTING WHAT YOU WANT
    #         encoded_return = self.recurse_message_data_for_text(payload)
    #
    #     if encoded_return == None:
    #         print("No text area found for this email...")
    #         encoded_return = ""
    #
    #     bytes_version = encoded_return.encode('ASCII')
    #     different_bytes = base64.urlsafe_b64decode(bytes_version)
    #     return different_bytes.decode()
    #
    #
    # def recurse_message_data_for_text(self, raw_data):
    #     if raw_data.get('body'):
    #         if raw_data.get('body').get('data') != None:
    #             return raw_data.get('body').get('data')
    #         else:
    #             parts = raw_data.get('parts')
    #             if parts == None:
    #                 return parts
    #             for part in parts:
    #                 found_text = self.recurse_message_data_for_text(part)
    #
    #                 if found_text != None:
    #                     return found_text
    #     return None


    def find_key_phrase(self, key_phrase):
        lower_text = self.text.lower()
        lower_kp = key_phrase.lower()
        found = False
        if lower_kp in lower_text:
            print("Found 1st:{0} in text: {1}".format(lower_kp, lower_text))
            found = True
        if lower_kp.replace(' ', '-') in lower_text:
            print("Found 2nd:{0} in text: {1}".format(lower_kp.replace(' ', '-'), lower_text))
            found = True
        if lower_kp.replace(' ', '') in lower_text:
            print("Found 3rd:{0} in text: {1}".format(lower_kp.replace(' ', ''), lower_text))
            found = True
        return found


    def determine_if_seen(self, seen_email_data):
        return self.sender in seen_email_data.keys()


    def is_from_active(self, seen_email_data):
        if seen_email_data.get(self.sender):
            return seen_email_data[self.sender]['active']
        else:
            return False