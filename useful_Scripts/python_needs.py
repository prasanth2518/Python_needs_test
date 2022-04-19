"""import modules"""
import base64
import csv
import email
import filecmp
import functools
import hashlib
import hmac
import imaplib
import io
import itertools
import json
import multiprocessing
import os
import re
import sys
import time
import webbrowser
import zipfile
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from email.header import decode_header
from operator import itemgetter
from urllib.parse import urlencode

import aiohttp
import pandas as pd
import pyAesCrypt
import pyexcel
import requests
import xlrd
from PIL import Image
from cryptography.fernet import Fernet
from dateutil.parser import parse
from imapclient import IMAPClient

'''
hashing
'''


def hash(self, key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def generate_api_info(self, diag_code, edition, PRODUCTS, SEARCH_TYPE, API_VERSION, CONTENT_OWNER, CLIENT_ID, METHOD,
                      HASH_KEY, MCG_BASE_URL):
    # _params = {"searchType": SEARCH_TYPE, "value": diag_code}
    _params = {"products": PRODUCTS, "searchType": SEARCH_TYPE, "value": diag_code}
    # end_point = f"/api/{API_VERSION}/{CONTENT_OWNER}/{EDITION}/{PRODUCT}/search"
    end_point = f"/api/{API_VERSION}/{CONTENT_OWNER}/{edition}/search"
    query_end_point = f"{end_point}?"
    param_query_str = f"{query_end_point}{urlencode(_params, doseq=True)}"
    signature_str = f"{param_query_str}{CLIENT_ID}{METHOD}{HASH_KEY}"
    signature = ((base64.b64encode(hashlib.sha256(signature_str.encode("UTF-8")).digest())).decode())
    url = f"{MCG_BASE_URL}{param_query_str}"
    return url, signature


'''
Decorators with Time
'''


def timer(func):
    """Print the runtime of decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        run_time = end - start
        print(f"Finished processing function {func.__name__!r} in {run_time:.4f} sec")
        return value

    return wrapper_timer


'''
aes encryption with file and password
'''

aes_key = ""


@timer
def aes_encryption(password, file):
    buffer_size = 64 * 1024
    infile = open(file, 'r')
    file_content = json.load(infile)
    base64_content = file_content['result']['image_output'][0]['base64']
    base64_content = base64_content.encode("utf-8")
    fin = io.BytesIO(base64_content)
    fCiph = io.BytesIO()
    pyAesCrypt.encryptStream(fin, fCiph, password, buffer_size)
    return fCiph.getvalue()


@timer
def aes_decryption(password, content):
    buffer_size = 64 * 1024
    ctlen = len(content)
    fcipher = io.BytesIO(content)
    fcipher.seek(0)
    fDec = io.BytesIO()
    pyAesCrypt.decryptStream(fcipher, fDec, password, buffer_size, ctlen)
    return str(fDec.getvalue())


content = aes_encryption(aes_key, 'IF20210616006215845_page_1.json')
if __name__ == "__main__":
    payload = 'IF20210616006215845_page_1.json'
    # requests = [payload]
    requests = [content] * 100
    try:
        multiprocessing.set_start_method('spawn')
    except RuntimeError:
        pass
    pool = multiprocessing.Pool(processes=11)
    try:
        start = time.perf_counter()
        func = pool.map(functools.partial(aes_decryption, aes_key), requests)
        # func=pool.map(process_request,requests)
        pool.close()
        pool.join()
        end = time.perf_counter()
        print("Time elapsed", end - start)
    except Exception as e:
        print(e)
        pool.close()

'''
Fernet Encryption
'''


def fernet_encrypt(key, file):
    fernet = Fernet(key)
    infile = open(file, 'r')
    file_content = json.load(infile)
    base64_content = file_content['result']['image_output'][0]['base64']
    base64_content = base64_content.encode("utf-8")
    encrypted = fernet.encrypt(base64_content)
    return encrypted
    # with open('encrypted_insights.json', 'wb') as fout:
    #     fout.write(encrypted)


def fernet_decrypt(key, encrypted_data):
    fernet = Fernet(key)
    # with open(file, 'rb') as fin:
    #      encrypted_data=fin.read()
    decrypted_Data = fernet.decrypt(encrypted_data)
    return decrypted_Data
    # with open('decrypted_insights.json', 'wb') as fout:
    #        fout.write(decrypted_Data)


'''
Protegrity encryption
'''


def get_content(file_name, base_path=None):
    if base_path is None:
        base_path = os.path.abspath(__file__)
        base_path = base_path.rsplit("/", 1)[0]
    file_path = os.path.join(base_path, file_name)
    with open(file_path, encoding="utf-8") as data_file:
        return json.loads(data_file.read())


encryption_url = os.getenv("protegrity_encryption_url")
decryption_url = os.getenv("protegrity_decryption_url")
solution_id = os.getenv("solution_id")

user = os.getenv("username")
password = os.getenv("password")
session = requests.Session()
session.auth = (user, password)


# SSL=os.getenv("SSL")

@timer
def protegrity_encryption(session, file):
    infile = open(file, 'r')
    file_content = json.load(infile)
    base64_content = file_content['result']['image_output'][0]['base64']
    base64_content = base64_content.encode("utf-8")

    with session.post(encryption_url, data=base64_content, verify=False) as response:
        content = response.content
        res = {"status": response.status_code}
        return content


# start=time.perf_counter()
# file='getInsight_response.json'
# print(protegrity_encryption(session,file))
# end=time.perf_counter()
#
# print("Time elapsed",end-start)


@timer
def protegrity_decryption(session, content):
    with session.post(decryption_url, data=content, verify=False) as response:
        content_decrypted = response.content
        res = {"status": response.status_code}
        print(res)
        return content_decrypted


async def protegrity_encrypt(session, file):
    file_name = file.split("/")[-1]
    file_content = get_content(file_name, './')
    # file_content=read_file(solution_id,file)
    base64_content = file_content['result']['image_output'][0]['base64']
    base64_content = base64_content.encode("utf-8")
    try:
        async with session.post(encryption_url, data=base64_content, verify_ssl=False,
                                auth=aiohttp.BasicAuth(user, password)) as response:
            resp = await response.read()
            res = {"status": response.status}
            return resp
    except Exception as e:
        print(e)


async def protegrity_decrypt(session, content):
    async with session.post(decryption_url, data=content, verify_ssl=False,
                            auth=aiohttp.BasicAuth(user, password)) as response:
        resp = await response.read()
        res = {"status": response.status}
        print(res)
        return resp


'''
Excel csv operation
'''


def csv_from_excel(file):  # file = "C:\\\\Users\\\\AG82323\\\\Downloads\\\\08252020_16_policies_prod_v1.1.xlsx"
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('v2_policy.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def csv_from_excel_1(file):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name('Proc Code Mapping')
    with open('v13_policies_map.csv', 'w', encoding='utf-8') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))


'''
Csv to execl
'''


def csv_to_execl():
    s = pyexcel.get_sheet(file_name="exec_repor.csv")
    s.save_as("exec_re.xlsx")


'''
Json File reading & Writing
'''


def json_read_write(data):
    with open("v2_policy_config.json", encoding='utf-8-sig') as r:
        d = json.load(r)

    with open('v2_policy_config.json', 'w') as outfile:
        json.dump(data, outfile)


'''
dividing list to equal chunks
'''


def dividing_list_equal_chunks(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


'''
prepareing zip from api response
'''


def prepare_Zip_with_api_Response(response_data):
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
        with z.open("data.json", "w") as data_file:
            data_file.write(json.dumps(response_data).encode("utf-8"))
    data.seek(0)


'''
Read ZIP Files
'''


def read_zip(path_file, file_name, local_path_lst):
    json_response = {}
    with zipfile.ZipFile(path_file + file_name) as zip_ref:
        zip_ref.extractall(path_file)
        for info in zip_ref.infolist():
            with open(path_file + info.filename) as json_file:
                json_response = json.load(json_file)
                local_path_lst.append(path_file + info.filename)
    return json_response


'''
Partial _func
'''


def func(u, v, w, x):
    return u * 4 + v * 3 + w * 2 + x


# Enter your code here to create and print with your partial function
print(func(2, 3, 5, 6))
fg = functools.partial(func, 2, 3)
print(fg)
print(fg(5, 6))


def partial_func_iter(RECORD_SIZE):
    with open("example_text.txt", 'rt') as f:
        # partial takes function fileobject.read and RECORD_SIZE and this is converted
        # into an iterator
        chunk_records = iter(functools.partial(f.read, RECORD_SIZE), "")
        for records in chunk_records:
            print(records)


'''
Generators
'''
'''generator is a function that returns an object (iterator) which we can iterate over (one value at a time).'''


# A simple generator function
def my_gen():
    n = 1
    print('This is printed first')
    # Generator function contains yield statements
    yield n

    n += 1
    print('This is printed second')
    yield n

    n += 1
    print('This is printed at last')
    yield n


a = my_gen()
print(a)  # iterator object
for i in a:
    print(i)

'''
Diff b/w is and ==
'''


def diff_is_and_equal():
    list1 = []
    list2 = []
    list3 = list1

    if (list1 == list2):
        print("True")
    else:
        print("False")

    if (list1 is list2):
        print("True")
    else:
        print("False")

    if (list1 is list3):
        print("True")
    else:
        print("False")

    list3 = list3 + list2

    if (list1 is list3):
        print("True")
    else:
        print("False")


'''
Max Product pairs from list
'''


def max_product(items):
    items = list(set(items))
    # get max pairs from list
    m = [(items[i], items[j]) for i in range(len(items)) for j in range(i + 1, len(items))]
    m = list(set([i for i in m]))
    # getting product pairs dict
    p = {}
    for j in m:
        if j[0] * j[1] in p:
            p[j[0] * j[1]].append(j)
        else:
            p[j[0] * j[1]] = [j]
    print(p[max(p.keys())])


k = [1, 2, 3, 4, 0, 8, 4]
l = [0, -1, -2, -4, 5, 0, -6]

max_product(k)
max_product(l)

'''
get DCN page Data 
'''


def get_dcn_page_data(l):
    df = pd.DataFrame(l)
    df_list = df[(df["dcn"] == 'NXTCOMUA736472011') & (df["page"] == 19)].to_dict(orient="records")[
        0] if df.to_dict() else []
    print(df_list)


'''
Convert base64 to tiff 
'''


def base_to_tiff(_base64, tiff_file_name):
    _base64 += "=" * ((4 - len(_base64) % 4) % 4)
    bytes_base64 = _base64.encode()
    data = base64.b64decode(bytes_base64)
    f = open(tiff_file_name, 'wb')
    f.write(data)
    f.close()


'''
get jpeg base64 from Tiff files
'''


def get_jpeg_base64_from_tiff(tiff_filepath, jpeg_filepath):
    im = Image.open(tiff_filepath)
    try:
        im.save(jpeg_filepath)
    except:
        im = im.convert("RGB")
        im.save(jpeg_filepath)

    with open(jpeg_filepath, "rb") as img_file:
        string = base64.b64encode(img_file.read())
        st = string.decode("utf-8")
    size = len(st.encode('utf-8'))
    size = size / 1000
    return size, st


'''
Sort dictionary key or value
'''


def sort_dictionary():
    dictionary_of_names = {'beth': 37, 'jane': 32, 'john': 41, 'mike': 59}

    # with keys
    print(dict(sorted(dictionary_of_names.items())))
    print(dict(sorted(dictionary_of_names.items(), key=lambda kv: kv[0])))

    # with value:
    sorted_age = dict(sorted(dictionary_of_names.items(), key=lambda kv: kv[1]))
    print(sorted_age)

    '''
    Examples
    nums = [1,1,7,3,5,3,2,9,5,1,3,2,2,2,2,2,9]
    def count(num_list):
        return dict(sorted({num:num_list.count(num) for num in num_list}.items(), key=lambda x:x[1]))
    '''


'''
Sorting list of dictionries
'''


def sort_list_of_dictionaries():
    # Initializing list of dictionaries
    lis = [{"name": "Nandini", "age": 20},
           {"name": "Manjeet", "age": 20},
           {"name": "Nikhil", "age": 19}]

    # using sorted and itemgetter to print list sorted by age
    print("The list printed sorting by age: ")
    print(sorted(lis, key=itemgetter('age')))
    print(sorted(lis, key=lambda x: x['age']))

    # using sorted and itemgetter to print list sorted by both age and name
    # notice that "Manjeet" now comes before "Nandini"

    print("The list printed sorting by age and name: ")
    print(sorted(lis, key=itemgetter('age', 'name')))
    print(sorted(lis, key=lambda x: (x['age'], x["name"])))

    # using sorted and itemgetter to print list sorted by age in descending order
    print("The list printed sorting by age in descending order: ")
    print(sorted(lis, key=itemgetter('age'), reverse=True))
    print(sorted(lis, key=lambda x: x['age'], reverse=True))


'''
MAP function
'''


def map_fun():
    numbers1 = [1, 2, 3]
    numbers2 = [4, 5, 6]

    result = map(lambda x, y: x + y, numbers1, numbers2)
    print(list(result))


'''
groupby itertools
'''


def group_by():
    # Python code to demonstrate
    # itertools.groupby() method

    L = [("a", 1), ("a", 2), ("b", 3), ("b", 4)]

    # Key function
    key_func = lambda x: x[0]
    key_func = itemgetter("a")

    for key, group in itertools.groupby(L, key_func):
        print(key + " :", list(group))


'''
default_dict_func
'''


def default_dict_func():
    # Defining the dict and passing
    # lambda as default_factory argument
    d = defaultdict(lambda: "Not Present")
    d["a"] = 1
    d["b"] = 2

    print(d["a"])
    print(d["b"])
    print(d["c"])

    h = defaultdict(list)
    for i in range(10):
        h[i].append("added")
    print(h)


"""
minimum platforms
"""


def findPlatform(arr, dep, n):
    # Sort arrival and
    # departure arrays
    arr.sort()
    dep.sort()

    # plat_needed indicates
    # number of platforms
    # needed at a time
    plat_needed = 1
    result = 1
    i = 1
    j = 0

    # Similar to merge in
    # merge sort to process
    # all events in sorted order
    while (i < n and j < n):

        # If next event in sorted
        # order is arrival,
        # increment count of
        # platforms needed
        if (arr[i] <= dep[j]):

            plat_needed += 1
            i += 1

        # Else decrement count
        # of platforms needed
        elif (arr[i] > dep[j]):

            plat_needed -= 1
            j += 1

        # Update result if needed
        if (plat_needed > result):
            result = plat_needed

    return result


# Driver code


arr = [900, 940, 950, 1100, 1500, 1800]
dep = [910, 1200, 1120, 1130, 1900, 2000]
n = len(arr)

print("Minimum Number of Platforms Required = ",
      findPlatform(arr, dep, n))
'''
reverse of number
'''


def reverse_number(num):
    """

    Args:
            num (int): number

    Returns:
            revesre_int(int): reversed number
    """

    if not isinstance(num, int):
        return "this is not an integer"
    return int(f"-{str(num)[:0:-1]}") if "-" in str(num) else int(str(num)[::-1])


print(reverse_number(2412))

'''
Delete Unread mails

'''


def delete_unread_mails():
    mail = IMAPClient('imap.gmail.com', ssl=True, port=993)
    mail.login("example@gmail.com", "password")
    totalMail = mail.select_folder('Inbox')
    # Shows how many messages are there - both read and unread
    print('You have total %d messages in your folder' % totalMail[b'EXISTS'])
    delMsg = mail.search(('UNSEEN'))
    mail.delete_messages(delMsg)
    # Shows number of unread messages that have been deleted now
    print('%d unread messages in your folder have been deleted' % len(delMsg))
    mail.logout()


'''Read Mails'''


def read_mails():
    # account credentials
    username = "youremailaddress@provider.com"
    password = "yourpassword"

    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 3
    # total number of emails
    messages = int(messages[0])
    for i in range(messages, messages - N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        body = "Error"
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            try:
                                body = str(part)
                            except:
                                pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    folder_name = clean(subject)
                    if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                        os.mkdir(folder_name)
                    filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    # write the file
                    open(filepath, "w").write(body)
                    # open in the default browser
                    webbrowser.open(filepath)
                print("=" * 100)
    # close the connection and logout
    imap.close()
    imap.logout()


'''read_unread emails'''


# no need to import smtplib for this code
# no need to import time for this code

def read_email_from_gmail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('my_mail', 'my_pwd')
    mail.select('inbox')

    result, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in range(latest_email_id, first_email_id, -1):
        # need str(i)
        result, data = mail.fetch(str(i), '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                # from_bytes, not from_string
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                try:
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                except Exception as e:
                    print(str(e))


# nothing to print here
read_email_from_gmail()

'''Compare two files'''


def compare_two_files():
    file1 = "python_needs.py"
    file2 = "../test_run_1.py"
    # method 1
    # shallow mode, compare metadata
    result = filecmp.cmp(file1, file2)
    print(result)
    # deep mode, Compare content
    result = filecmp.cmp(file1, file2, shallow=False)
    print(result)

    # method2
    file1_data = open(file1, 'r').readlines()
    file2_data = open(file2, 'r').readlines()
    diff = [line for idx, line in enumerate(file1_data) if
            (len(file2_data) > idx and line != file2_data[idx]) or len(file2_data) < idx]
    return True if len(file1_data) == len(file2_data) and not diff else False


'''Hashing files '''


# method_1:
# Python rogram to find the SHA-1 message digest of a file

def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


message = hash_file("track1.mp3")
print(message)


# methos_2
def hash_file():
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(sys.argv[1], 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)

    print("MD5: {0}".format(md5.hexdigest()))
    print("SHA1: {0}".format(sha1.hexdigest()))


'''
date match regex(mdy)
'''


def date_convert_match():
    date = str(parse("02/23/4567", fuzzy=True).date())
    _date = datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")
    match_group = re.match('^(0[1-9]|1[012])*[a-zA-Z]*[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$', _date)
    return _date


'''
env vars export
'''


def env_Vars_export():
    for k, v in json.load(open('env.json')).items():
        os.environ[k] = v
    print(os.getenv('DB_PASSWORD_MONGO'))


'''
add numbers recursivly
'''


# method1
def add_num(num_list, total=None):
    total = total if total else 0
    if isinstance(num_list, list):
        for num in num_list:
            total = add_num(num, total)
            total += num
    else:
        total + num_list
    return total


def _main_add(num_list):
    res = add_num(num_list)
    print(res)


_main_add(l)


##method2:

def getSum(piece):
    if len(piece) == 0:
        return 0
    else:
        return piece[0] + getSum(piece[1:])


print(getSum([1, 3, 4, 2, 5]))

'''
read list env var
'''

env_list = json.loads(os.getenv('ENV_LIST1', '[]'))
print(env_list)
print(type(env_list))

'''
change str recursivly
'''


def modifiy_individual_rule(payload, updated_rules=None):
    if "conditions" not in payload:
        print(payload)
        raise Exception("conditions not found in input payload")
    if len(payload["conditions"]) == 1:
        return payload["conditions"][0]
    modified_rule = deepcopy(payload["conditions"])
    updated_rules = updated_rules if updated_rules else []
    if "log" in payload:
        for each_rule in payload["conditions"]:
            if each_rule != payload["conditions"][-1]:
                modified_rule.insert(modified_rule.index(each_rule) + 1, {"log": payload["log"]})
        for _each_mod_rule in modified_rule:
            if "conditions" not in _each_mod_rule:
                updated_rules.append(_each_mod_rule)
                continue
            _mod_rule = modifiy_individual_rule(_each_mod_rule)
            updated_rules.append(_mod_rule)
        return updated_rules


def get_modified_rules(_rule_json):
    conditions = _rule_json["conditions"][0]
    updated_rules = modifiy_individual_rule(conditions)
    if not isinstance(updated_rules, list):
        updated_rules = [updated_rules]
    _rule_json["conditions"] = updated_rules
    return _rule_json


'''
Quey executions 
'''


def create_condition_string(match_Rkey, match_Lkey, operator, lvalue, rvalue):
    # query_str = '(name == "patient_first_name" and value == "Linda") or (name == "sex" and value == "Female")'
    if operator in ["==", ">", "<", "!=", ">=", "<="]:
        if not match_Rkey and not match_Lkey:
            if isinstance(rvalue, str):
                base_q = '{lvalue} {op} "{rvalue}"'
            else:
                base_q = '{lvalue} {op} {rvalue}'
        else:
            if isinstance(rvalue, str):
                base_q = '{match_Lkey} == "{lvalue}" and {match_Rkey} {op} "{rvalue}"'
            else:
                base_q = '{match_Lkey} == "{lvalue}" and {match_Rkey} {op} {rvalue}'

        if lvalue == "":
            if isinstance(rvalue, str):
                base_q = '{match_Rkey} {op} "{rvalue}"'
            else:
                base_q = '{match_Rkey} {op} {rvalue}'
            cond_string = base_q.format(
                match_Rkey=match_Rkey,
                op=operator,
                rvalue=rvalue)
        elif rvalue == "":
            if isinstance(lvalue, str):
                base_q = '{match_Lkey} {op} "{lvalue}"'
            else:
                base_q = '{match_Lkey} {op} {lvalue}'
            cond_string = base_q.format(
                match_Lkey=match_Lkey,
                op=operator,
                lvalue=lvalue)
        else:
            cond_string = base_q.format(
                match_Lkey=match_Lkey,
                lvalue=lvalue,
                match_Rkey=match_Rkey,
                op=operator,
                rvalue=rvalue)

    elif operator.lower() == "contains":
        if not match_Rkey and not match_Lkey:
            cond_string = '{lvalue}.str.contains(@rvalue, na=False)'.format(
                lvalue=lvalue,
                op=operator)
        else:
            if lvalue == "":
                cond_string = '{match_Rkey}.str.contains(@rvalue, na=False)'.format(match_Rkey=match_Rkey)
            elif rvalue == "":
                cond_string = '{match_Lkey}.str.contains(@lvalue, na=False)'.format(match_Lkey=match_Lkey)
            else:
                cond_string = '{match_Lkey} == "{lvalue}" and {match_Rkey}.str.contains(@rvalue, na=False)'.format(
                    match_Lkey=match_Lkey,
                    lvalue=lvalue,
                    match_Rkey=match_Rkey,
                    op=operator)
    elif operator.lower() == "regex":
        if not match_Rkey and not match_Lkey:
            cond_string = '{lvalue}.str.contains(@rvalue, na=False, regex=True)'.format(
                lvalue=lvalue,
                op=operator)
        else:
            if lvalue == "":
                cond_string = '{match_Rkey}.str.contains(@rvalue, na=False, regex=True)'.format(match_Rkey=match_Rkey)
            elif rvalue == "":
                cond_string = '{match_Lkey}.str.contains(@lvalue, na=False, regex=True)'.format(match_Lkey=match_Lkey)
            else:
                cond_string = '{match_Lkey} == "{lvalue}" and {match_Rkey}.str.contains(@rvalue, na=False, regex=True)'.format(
                    match_Lkey=match_Lkey,
                    lvalue=lvalue,
                    match_Rkey=match_Rkey,
                    op=operator)
    elif operator.lower() == "in":
        cond_string = '{lvalue}.isin({rvalue})'.format(lvalue=lvalue, rvalue=rvalue)
    elif operator.lower() == "notin":
        cond_string = '~{lvalue}.isin({rvalue})'.format(lvalue=lvalue, rvalue=rvalue)
    else:
        cond_string = ""
    return cond_string


def exec_list_conditions(_lval, _rval, inp_df, operator):
    out_df = pd.DataFrame()
    lis = inp_df[_lval].to_list()
    if operator.lower() in ["any_startswith", "not_any_startswith"]:
        index = list(set([lis.index(j) for j in lis for l in j for m in _rval if l.startswith(m)]))
    else:
        index = [lis.index(j) for j in lis if set(j).intersection(set(_rval))]
    if operator.lower() in ["any", "any_startswith"]:
        out_df = inp_df[inp_df.index.isin(index)] if index else out_df
    elif operator.lower() in ["not_any", "not_any_startswith"]:
        out_df = inp_df[~inp_df.index.isin(index)] if index else inp_df
    return out_df
