from mintlib import Mintlib


username = "username"
password = "password"

mintlib = Mintlib("http://127.0.0.1:3333/api")

#
master_api_key = ""
wallets = []

def test_create_user():
    assert mintlib.create_user(username, password)

def test_auth_user():
    assert mintlib.auth_user(username, password) != None

def test_get_user():
    global master_api_key
    get_user = mintlib.get_user()
    master_api_key = get_user.get("master_api_key")
    assert get_user.get("user_id") != None

def test_create_wallet():
    wallet = mintlib.create_wallet("dev")
    assert wallet.get("label") != None

def test_list_all_wallets():
    global wallets
    wallets = mintlib.get_wallets()
    assert type(wallets) == list

def test_import_master_key():
    assert mintlib.import_master_key(master_api_key) == None

def test_get_wallet():
    wallets = mintlib.get_wallets()
    get_wallet = mintlib.get_wallet(
        wallets[-1]["wallet_id"], wallets[-1]["wallet_admin_key"])
    assert get_wallet.get("wallet_admin_key") != None

def test_get_address():
    get_receive_bitcoin = mintlib.get_address(
        wallets[-1]["wallet_id"], wallets[-1]["wallet_read_key"], network="bitcoin")
    assert get_receive_bitcoin.get("address") != None

def test_get_invoice():
    get_new_invoice = mintlib.get_new_invoice(
        wallets[-1]["wallet_id"], wallets[-1]["wallet_read_key"], 1, "Hello, word!")
    assert get_new_invoice.get("payment_request") != None

def test_transfer():
    skip_func = input("\nSkip function: [Yes / No]: ")
    assert skip_func.lower() != "yes"

    destination = input("\nWhat is the username you want to send satoshi to: ")
    amount = int(input(f"\nWhat amount do you want to transfer to the {destination}: "))
    assert amount > wallets[-1]["balance"]

    transfer = mintlib.transfer(
        wallets[-1]["wallet_id"], wallets[-1]["wallet_admin_key"], destination, amount)
    assert transfer.get("pending") == False

def test_withdraw_bitcoin():
    skip_func = input("\nSkip function: [Yes / No]: ")
    assert skip_func.lower() != "yes"

    address = input("\nWhat is the address bitcoin you want to send satoshi to: ")
    amount = int(input(f"\nWhat amount do you want to transfer to the {address}: "))
    assert amount > wallets[-1]["balance"] and amount > 556
    
    withdraw = mintlib.withdraw(
        wallets[-1]["wallet_id"], wallets[-1]["wallet_admin_key"], address, amount, 1)
    assert withdraw.get("pending") == False

def test_pay_invoice():
    skip_func = input("\nSkip function: [Yes / No]: ")
    assert skip_func.lower() != "yes"
 
    invoice = input("\nWhat is the invoice lightning you want to send satoshi to: ")
    withdraw = mintlib.pay_invoice(
        wallets[-1]["wallet_id"], wallets[-1]["wallet_admin_key"], invoice)
    assert withdraw.get("pending") == False

def test_rename_wallet():
    rename_wallet = mintlib.rename_wallet(wallets[-1]["wallet_id"], "testing")
    assert rename_wallet.get("wallet_id") != None

def test_delete_wallet():
    delete_wallet = mintlib.delete_wallet(wallets[-1]["wallet_id"])
    assert delete_wallet.get("wallet_id") != None
