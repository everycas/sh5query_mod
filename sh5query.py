import requests

# Connection
HOST = '127.0.0.1'
PORT = '9797'

# Operations

EXEC = 'sh5exec'  # выполнить процедуру

USER_NAME = 'Admin'
USER_PASS = ''

# STOREHOUSE 5 REPLICATION PROCEDURES -------------------------------------------------------------- #


# send sh5 api request
def api_request(host, port, operation, proc):
    request = requests.post(url=f'http://{host}:{port}/api/{operation}', json=proc)
    request.raise_for_status()
    data = request.json()
    print(data)
    return data


# convert num string to guid
def num_to_guid(num: str):
    """ Convert any number to guid """
    zero_add = ''
    guid_mask = '{00000000-0000-0000-0000-'
    postfix = '}'
    if len(num) < 12:
        diff = 12 - len(num)  # 6
        for _ in range(diff):
            zero_add += '0'
            code = zero_add + num
    elif len(num) > 12:
        diff = len(num) - 12
        code = num[diff:]
    else:
        code = num

    guid = guid_mask + code + postfix
    return guid  # make

# Fields ---------------------------------------------------------------------------------------------------- #

# ggroup
ggroup_parent_guid = ['{00000000-0000-0000-0000-000000000300}']  # mask: '{00000000-0000-0000-0000-000000000000}'
ggroup_guid = ['']  # mask: '{00000000-0000-0000-0000-000000000000}'
ggroup_name = ['Root Test group']  # [str]
# good
good_parent_guid = []  # mask: '{00000000-0000-0000-0000-000000000000}'
good_guid = []  # mask: '{00000000-0000-0000-0000-000000000000}'
good_name = []  # [str]
good_price = []  # [float] : sale price + taxes
good_rkcode = []  # [int]
# corr
corr_guid = []  # mask: '{00000000-0000-0000-0000-000000000000}'
corr_name = []  # [str]
corr_type = [2]  # [int] / 2 - спец.корр
# sunit
sunit_guid = []  # mask: '{00000000-0000-0000-0000-000000000000}'
sunit_name = []  # [str]
# odoc
odoc_date = ['2022-04-05']  # [date] / 221\\31
odoc_sunit_guid = ['{00000000-0000-0000-0000-000005000000}']  # mask: '{00000000-0000-0000-0000-000000000000}' / место реализации / 221\\226\\4
odoc_corr_guid = ['{00000000-0000-0000-0000-100000000000}']  # mask: '{00000000-0000-0000-0000-000000000000}' / спец.корр / 221\\107\\4
odoc_good_guid = ['{00000000-0000-0000-0000-000000010014}']  # mask: '{00000000-0000-0000-0000-000000000000}' / товар / 210\\4
odoc_good_qnt = [3.0]  # [float] / кол-во товара / 9
odoc_good_total = [450.00]  # [float] / сумма товара б.н. / 55
odoc_spec = [0]  # [int] / спецификация заявки / стандарт / 42

# Репликация групп товаров --------------------------------------------------------------------------- #

repl_groups = {
    "UserName": USER_NAME,
    "Password": USER_PASS,
    "ProcName": 'ReplGGroups',
    "Input": [
        {
            "Head": "209#2",
            "Original": ['209#3\\4', '4', '3'],
            "Values": [[ggroup_parent_guid], [ggroup_guid], [ggroup_name]]
        }
    ]
}

# Репликация товаров ------------------------------------------------------------- #

repl_goods = {
    "UserName": USER_NAME,
    "Password": USER_PASS,
    "ProcName": 'ReplGoods',
    "Input": [
        {
            "Head": "210",
            "Original": ['209\\4', '4',  '3', '56', '241'],
            "Values": [ggroup_guid, good_guid, good_name, good_price, good_rkcode]
        }
    ]
}

# Репликация спец.корр-ов --------------------------------------- #

repl_corrs = {
    "UserName": USER_NAME,
    "Password": USER_PASS,
    "ProcName": 'ReplCorrs',
    "Input": [
        {
            "Head": "107",
            "Original": ['4', '3', '32'],
            "Values": [corr_guid, corr_name, corr_type]
        }
    ]
}

# Репликация мест реализации

repl_sunits = {
    "UserName": USER_NAME,
    "Password": USER_PASS,
    "ProcName": 'ReplSUnits',
    "Input": [
        {
            "Head": "226",
            "Original": ['4', '3'],
            "Values": [sunit_guid, sunit_name]
        }
    ]
}

# Репликация расхода / заявок ------------------------- #

repl_odoc = {
    "UserName": USER_NAME,
    "Password": USER_PASS,
    "ProcName": 'ReplODocs',
    "Input": [
        {
            "Head": "222",
            "Original": ['221\\31', '221\\226\\4', '221\\107\\4', '210\\4', '9', '55', '42'],
            "Values": [odoc_date, odoc_sunit_guid, odoc_corr_guid, odoc_good_guid, odoc_good_qnt, odoc_good_total, odoc_spec]
        }
    ]
}

# Action
api_request(host=HOST, port=PORT, operation=EXEC, proc=repl_groups)
