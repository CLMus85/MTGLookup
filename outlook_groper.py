import imaplib
import config
import re
import requests
from bs4 import BeautifulSoup

imap = imaplib.IMAP4_SSL(config.imap_server)


# Login to outlook imap-mail.outlook.com with imap_server/smtp_server NAME and PASSWORD set correctly in config
def main():
    imap.login(config.NAME, config.PASSWORD)
    result, mailboxes = imap.list()
    print([result, mailboxes])
    # They're my emails and i need them NOW!
    pick_mailbox()


def pick_mailbox():
    print("Choose a number:\n\t 1. INBOX 2. OUTBOX 3. TRASH\n\t "
          "4. JUNK 5. DRAFTS 6. ARCHIVE\n\t 7. NOTES 8. SENT 9. DELETED")
    choice = input()
    if len(choice) > 1 or (not 57 >= ord(choice) >= 49):
        print("Pick a single digit number only")
        print("1. Try again? 2. Logout?")
        new_choice = int(input())
        if new_choice == 1:
            pick_mailbox()
        else:
            print("Logged out. Type main() to log back in")
            imap.logout()
    elif int(choice) == 1:
        print("Inbox Selected")
        imap.select("INBOX")
    elif int(choice) == 2:
        print("Outbox selected")
        imap.select("OUTBOX")
    elif int(choice) == 3:
        print("Trash selected")
        imap.select("TRASH")
    elif int(choice) == 4:
        print("Junk selected")
        imap.select("JUNK")
    elif int(choice) == 5:
        print("Drafts selected")
        imap.select("DRAFTS")
    elif int(choice) == 6:
        print("Archive selected")
        imap.select("ARCHIVE")
    elif int(choice) == 7:
        print("Notes selected")
        imap.select("NOTES")
    elif int(choice) == 8:
        print("Sent selected")
        imap.select("SENT")
    elif int(choice) == 9:
        print("Deleted selected")
        imap.select("DELETED")


"""
CREATE command  
(typ, [data]) = <instance>.create(mailbox)

COPY command 
(typ, [data]) = <instance>.copy(message_set, new_mailbox)
        
STATUS Command 
rc, test = imap.status('Junk', '(UNSEEN)') 
'OK', [b'Junk (UNSEEN 307) '])

DELETE command (deletes entire mailbox)
(typ, [data]) = <instance>.delete(mailbox)

DELETEACL command 
deletes mailbox permissions for who
(typ, [data]) = <instance>.deleteacl(mailbox, who)

EXPUNGE command
(typ, [data]) = <instance>.expunge()
'data' is list of 'EXPUNGE'd message numbers in order received.

FETCH command
fetch parts of message
'message_parts' should be a string of selected parts
enclosed in parentheses, eg: "(UID BODY[TEXT])".
'data' are tuples of message part envelope and data.
(typ, [data, ...]) = <instance>.fetch(message_set, message_parts)

GETACL command
gets acls for a mailbox
(typ, [data]) = <instance>.getacl(mailbox)

GETANNOTATION command
(typ, [data]) = <instance>.getannotation(mailbox, entry, attribute)
        Retrieve ANNOTATIONs.
        
GETQUOTA command
Get the quota root's resource usage and limits.
Part of the IMAP4 QUOTA extension defined in rfc2087.
(typ, [data]) = <instance>.getquota(root)

GETQUOTAROOT command
Get the list of quota roots for the named mailbox.
(typ, [[QUOTAROOT responses...], [QUOTA responses]]) = <instance>.getquotaroot(mailbox)

LIST command
List mailbox names in directory matching pattern.
(typ, [data]) = <instance>.list(directory='""', pattern='*')
'data' is list of LIST responses.

LOGIN commmand
Identify client using plaintext password.
(typ, [data]) = <instance>.login(user, password)
NB: 'password' will be quoted.

LOGIN_CRAM_MD5 command
Force use of CRAM-MD5 authentication.
(typ, [data]) = <instance>.login_cram_md5(user, password)

_CRAM_MD5_AUTH command
Authobject to use with CRAM-MD5 authentication.

LOGOUT command
Shutdown connection to server.
(typ, [data]) = <instance>.logout()
Returns server 'BYE' response.

LSUB command 
List 'subscribed' mailbox names in directory matching pattern.
(typ, [data, ...]) = <instance>.lsub(directory='""', pattern='*')
'data' are tuples of message part envelope and data.

MYRIGHTS command
show my ACLs for a mailbox (i.e. the rights that I have on mailbox).
(typ, [data]) = <instance>.myrights(mailbox)

NAMESPACE command
Returns IMAP namespaces ala rfc2342
(typ, [data, ...]) = <instance>.namespace()

NOOP command
Send NOOP command.
(typ, [data]) = <instance>.noop()

FETCH command
fetch truncated part of a message.
(typ, [data, ...]) = <instance>.partial(message_num, message_part, start, length)
'data' is tuple of message part envelope and data.

PROXYAUTH command
Assume authentication as "user".
Allows an authorised administrator to proxy into any user's
mailbox.
(typ, [data]) = <instance>.proxyauth(user)


"""

# print("Commands available \nall_seen(), all_unseen(), all_st(), ")
# front end stuff


def HAL():
    print("There are a number of tools I want to be accessible from here, that HAL"
          "should inform the user of the tools and the method in which to select them\n"
          "HAL will issue a NOOP command.  It does nothing and always succeeds. "
          "Can be used as a periodic poll for new messages - updates FolderStatus returned by last Select(String), "
          "Select(FolderInfo) command. Can also be used to reset any inactivity auto-logout timer on the server.\n"
          "After issuing the NOOP command, HAL will check specific boxes again for updates from specific targets"
          "and handle them accordingly.")
    return user_search()


""" uids in single uid[0] b'array' must be split to be selected as an index
re.match(pattern, string, flags=0)
this returns <re.Match object; span=(9012, 9019), match='http://'>
https://gist.github.com/martinrusev/6121028 """


def all_unseen():
    result, numbers = imap.search(None, None, 'UNSEEN')
    unread_uids = numbers[0].split()
    return unread_uids


def all_seen():
    typ, data = imap.search(None, None, 'SEEN')
    return data[0].split()


# Come back later and write a function for EVERY contractor
def all_st():
    # signingTRAC only requires an acceptance reply message
    typ, st_uids = imap.search(None, 'FROM', '"important person"')
    return st_uids[0].split()


def me():
    typ, data = imap.search(None, '(FROM "my name" BODY "important string")')
    return data[0].split()


def user_search():
    print("What would you like to search for?")
    my_search = input()
    response, li_st = imap.search(None, None, 'BODY "{}"'.format(my_search))
    length_of_search = len(li_st[0].split())
    li_st = li_st[0].split()
    if length_of_search > 1:
        print("I found {} entries.\nWhich email would you like?\n"
              "between 1 = oldest and {} = newest".format(length_of_search, length_of_search))
        new_search = input()
        if not ((type(int(new_search) == int)) or (1 <= int(new_search) <= length_of_search)):
            return "I need a number here in the correct range."
        else:
            return imap.fetch(li_st[int(new_search) - 1], '(RFC822)')
    if length_of_search == 1:
        return imap.fetch(li_st[0], '(RFC822)')


#   typ, uids = imap.search(None, 'FROM', '"Whoever you want"'
#   return uids[0].split()
def newest_email(uids):
    typ, data = imap.fetch(uids()[-1], '(RFC822)')
    return data


def fetch_latest():
    result, data = imap.uid('search', None, "ALL")
    latest = data[0].split()[-1]
    result, data = imap.uid('fetch', latest, '(RFC822)')
    return data


"""
Parses a contractors new email for a link then
Parses the html contents of the link for a specific link
Visits Link :)
"""


def parse_contractor_email():
    default_url = "Contractors url here sans tailing /"
    parsed_text = re.search(default_url, str(newest_email(me)))
    # The format my contractor returns urls ends in a random 6 char alphanumeric sequence
    # remove the logic or modify it to suit your purposes
    x_index = 6
    begin, end = parsed_text.span()[0], parsed_text.span()[1] + x_index
    soup = BeautifulSoup(requests.get(str(newest_email(me))[begin:end]).text, 'html.parser')
    my_str = ""
    """
    re.match(pattern, string, flags=0) 
    This contractor accepts orders in the form of a specific <a href='url'> nested in the html doc of the reference
    url in email
    The contractors html response is identical in structure to all previous
    The str_end is always in the same position
    """
    for i in soup.find_all('a'):
        my_str += i.get('href')
    my_str_begin, my_str_end = my_str.find('your_desired_string_is_here')
    my_str_end = my_str.find('observe_structure_put_tail_end_here')
    my_acceptance_link = "default_url{}".format(my_str[my_str_begin:my_str_end])
    return my_acceptance_link, requests.get('default_url{}').format(my_acceptance_link)


""" IMAP4.fetch(message_set, message_parts)
Fetch (parts of) messages. message_parts should 
be a string of message part names enclosed within parentheses, eg: "(UID BODY[TEXT])". 
Returned data are tuples of message part envelope and data. """


# mark all emails in selected box as seen
def all_seen():
    for i in all_unseen():
        imap.uid('store', i, '+FLAGS', '\SEEN')

# def mark_seen(email)
#     imap.uid()


if __name__ == "__main__":
    main()

# imap.search(None, 'UNSEEN', 'ALL')
# imap.search(None, 'SEEN', 'ALL')



