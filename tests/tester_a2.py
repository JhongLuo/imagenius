import argparse
import requests
import os


def isgoodipv4(s):
    digs_only = s.replace('http://', '')
    pieces = digs_only.split('.')
    if len(pieces) != 4: return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False


parser = argparse.ArgumentParser()
parser.add_argument(
    "--ip_addr", help="the IP of your web app, e.g. http://34.228.7.61", type=str, required=True)
args = parser.parse_args()

print("--------------------------------------------------------------------")
print("ECE1779 auto-tester A2")
print("--------------------------------------------------------------------")
print("checking your web app IP...")
if not args.ip_addr.startswith('http://'):
    exit('error: your IP address should starts with "http://"')
elif not isgoodipv4(args.ip_addr):
    exit('please use a valid IPv4 address with the correct format, e.g. http://34.228.7.61')

# link set up 
url = args.ip_addr + ':5000/api'
print("tester will be run on: {}".format(url))
score = 0

# test 1: delete_all
print("--------------------------------------------------------------------")
print("test 1: delete all keys & values from the application")
test_1_flag = True
try:
    response = requests.post(url + "/delete_all")
except:
    print("error in test 1: could not post /delete_all to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_1_flag = False

if test_1_flag:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 1: your response cannot be represented in JSON format")
    try:
        if jsonResponse["success"] == "true":
            score += 1
        else:
            print('error in test 1: /delete_all operation should return {"success": "true"}')
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 1: access failure on ["success"] of the post response')
        print("")

# test 2: list_keys
print("--------------------------------------------------------------------")
print("test 2: list_keys without any upload")
test_2_flag = True
try:
    response = requests.post(url + "/list_keys")
except:
    print("error in test 2: could not post /list_keys to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_2_flag = False

if test_2_flag:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 2: your response cannot be represented in JSON format")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["keys"] == []:
            score += 1
        else:
            print("""error in test 2: /list_keys operation should return 
                {
                    "success": "true",
                    "keys": []
                }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 2: access failure on ["success"]/["key"] of the post response')
        print("")

# test 3: upload
print("--------------------------------------------------------------------")
print("test 3: upload 2 images")
filenames = ['1.jpeg', '2.png']
work_dir = os.path.abspath(os.path.dirname(__file__))

try:
    file_1 = {'file': open(work_dir + '/images/' + filenames[0], 'rb')}
except:
    print("script failure: unable to open the image file. Please contact TA at wenjun.qiu@mail.utoronto.ca")

test_3_flag_1 = True
try:
    response = requests.post(url + "/upload", files=file_1, data={'key': 'test_1'})
except:
    print("error in test 3-1: could not post /upload to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_3_flag_1 = False

if test_3_flag_1:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 3-1: your response cannot be represented in JSON format")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["key"] == "test_1":
            score += 1
        else:

            print("""error in test 3-1: /upload operation should return 
                    {
                        "success": "true",
                        "key": "test_1"
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 3-1: access failure on ["success"]/["key"] of the post response')
        print("")

try:
    file_2 = {'file': open(work_dir + '/images/' + filenames[1], 'rb')}
except:
    print("script failure: unable to open the image file. Please contact TA at wenjun.qiu@mail.utoronto.ca")

test_3_flag_2 = True
try:
    response = requests.post(url + "/upload", files=file_2,
                             data={'key': 'test_2'})
except:
    print("error in test 3-2: could not post /upload to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_3_flag_2 = False

if test_3_flag_2:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 3-2: your response cannot be represented in JSON format")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["key"] == "test_2":
            score += 1
        else:

            print("""error in test 3-2: /upload operation should return 
                    {
                        "success": "true",
                        "key": "test_2"
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 3-2: access failure on ["success"]/["key"] of the post response')
        print("")

# test 4: retrieval
print("--------------------------------------------------------------------")
print("test 4: retrieve 1 image")

test_4_flag = True
try:
    response = requests.post(url + "/key/test_1")
except:
    print("error in test 4: could not post /key/test_1 to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_4_flag = False

if test_4_flag:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 4: your response cannot be represented in JSON format")
    try:
        if jsonResponse["success"] == "true" and jsonResponse["key"] == "test_1" and jsonResponse["content"] != None:
            score += 1
        else:
            print("""error in test 4: /key/test_1 operation should return 
                    {
                        "success": "true", 
                        "key" : "test_1",
                        "content" : file contents
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 4: access failure on ["success"]/["key"]/["content"] of the post response')
        print("")

# test 5: configure cache settings
print("--------------------------------------------------------------------")
print("test 5: configure the cache (manual mode)")

test_5_flag_1 = True
try:
    response = requests.post(url + '/configure_cache',
                             params={'mode': 'manual', 'numNodes': 2, 'cacheSize': 3, 'policy': 'RR'})
except:
    print("error in test 5: could not post /configure_cache to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_5_flag_1 = False

if test_5_flag_1:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 5: your response cannot be represented in JSON format.")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["mode"] == "manual" \
                and jsonResponse["numNodes"] == 2 and jsonResponse["cacheSize"] == 3 \
                and jsonResponse["policy"] == "RR":
            score += 1
        else:

            print("""error in test 5: /configure_cache operation should return 
                    {
                        "success": "true",
                        "mode": "manual",
                        "numNodes": 2,
                        "cacheSize": 3,
                        "policy": "RR"
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print(
            "error in test 5: access failure on ['success']/['mode']/['numNodes']/['cacheSize']/['policy'] of the post response.")
        print("")

# test 6: get number of nodes
print("--------------------------------------------------------------------")
print("test 6: get number of nodes")

test_6_flag_1 = True
try:
    response = requests.post(url + '/getNumNodes')
except:
    print("error in test 6: could not post /getNumNodes to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_6_flag_1 = False

if test_6_flag_1:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 6: your response cannot be represented in JSON format.")
    try:
        if jsonResponse["success"] == "true" and jsonResponse["numNodes"] == 2:
            score += 1
        else:
            print("""error in test 6: /getNumNodes operation should return 
                {
                    "success": "true",
                    "numNodes": 2
                }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print("error in test 6: access failure on ['success']/['numNodes'] of the post response.")
        print("")


# test 7: get miss rate
print("--------------------------------------------------------------------")
print("test 7: get miss rate")

test_7_flag_1 = True
try:
    response = requests.post(url + "/getRate", params={'rate': 'miss'})
except:
    print("error in test 7: could not post /getRate to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_7_flag_1 = False

if test_7_flag_1:
    try:
        jsonResponse = response.json()
    except:
        print("error in test 7: your response cannot be represented in JSON format.")
    try:
        if jsonResponse["success"] == "true" and jsonResponse["rate"] == "miss":
            score += 1
            print("Endpoint passes, but you should also check that your 'value' field returns the miss rate for the "
                  "last 1 minute.")
        else:
            print("""error in test 7: /getRate operation should return 
                {
                   "success": "true",
                    "rate": "miss",
                    "value": miss rate for the last 1 minute (as float)
                }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print("error in test 7: access failure on ['success']/['getRate'] of the post response.")
        print("")

print("--------------------------------------------------------------------")
print("tester total: {}/8".format(score))
