import imaplib, email
import sys

imap_url = 'imap.gmail.com'
email_to_search = 'antonio.fernandez@neonode.com'

f = open("./data/config.txt", "r")
user = f.readline().replace('\n', '')
password = f.readline().replace('\n', '')
f.close()

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value, con):
    # result, data = con.search(None, key, '"{}"'.format(value))
    result, data = con.search(None, '(UNSEEN)')
    return result, data

# Function to get the list of emails under this label
def get_emails(key, value, con):
    msgs = [] # all the email data are pushed inside an array

    retcode, result_bytes = search(key, value, con)

    if retcode == 'OK':
        for num in result_bytes[0].split():
            typ, data = conn.fetch(num, '(RFC822)')
            msgs.append(data)

            msg = email.message_from_string(str(data[0][1]))

            # Set msg as unread
            # typ, data = conn.store(num,'-FLAGS','\\Seen')

            if typ == 'OK':
                print(data,'\n',30*'-')
                print(msg)

    return msgs

# this is done to make SSL connnection with GMAIL
conn = imaplib.IMAP4_SSL(imap_url)

# logging the user in
try:
    (retcode, capabilities) = conn.login(user, password)
except:
    print(sys.exc_info()[1])
    sys.exit(1)

# calling function to check for email under this label
conn.select('Inbox') # ,readonly=1)

 # fetching emails from this user "tu**h*****1@gmail.com"
msgs = get_emails('FROM', email_to_search, conn)

# Finding the required content from our msgs
# User can make custom changes in this part to
# fetch the required content he / she needs
# printing them by the order they are displayed in your gmail
# for msg in msgs[::-1]:
#     for sent in msg:
#         if type(sent) is tuple:
#
#             # encoding set as utf-8
#             content = str(sent[1], 'utf-8')
#             data = str(content)
#
#             # Handling errors related to unicodenecode
#             try:
#                 indexstart = data.find("ltr")
#                 data2 = data[indexstart + 5: len(data)]
#                 indexend = data2.find("</div>")
#
#                 # printtng the required content which we need
#                 # to extract from our email i.e our body
#                 print(data2[0: indexend])
#
#             except UnicodeEncodeError as e:
#                 pass
