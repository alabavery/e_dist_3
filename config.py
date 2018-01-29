
CLIENT_SECRET_FILE_PATH = "client_secret.json"
SEEN_EMAIL_DATA_FILE_PATH = "test_seen_email_data.json"
UNUSED_VOTERS_FILE_PATH = "test_unused_voters.json"

ERROR_LOG_FILE_PATH = "logs/error_log.txt"
ROUTINE_ACTION_LOG_FILE_PATH = "logs/routine_log.txt"
ABNORMAL_ACTION_LOG_FILE_PATH = "logs/abnormal_log.txt"
IGNORE_LOG_FILE_PATH = "logs/ignored_log.txt"

BOT_MESSAGES = dict()
for bot_message_name in ['MESSAGE_WHEN_SENDING_VOTERS',
                    'MESSAGE_FOR_ASKING_IF_PEOPLE_WANT_MORE',
                    'MESSAGE_WHEN_BOT_DOESNT_UNDERSTAND',
                    'MESSAGE_WHEN_SOMEONE_CANT_MAIL_THER_VOTERS']:
    with open('Bot_Messages/{0}.txt'.format(bot_message_name), 'r') as f:
        BOT_MESSAGES[bot_message_name] = f.read()



SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.modify']