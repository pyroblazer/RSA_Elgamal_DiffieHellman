import PySimpleGUI as sg
import RSA
import DiffieHellman
import sys

def read_text_from_file(fname):
    with open(fname, 'r') as f:
        text= f.read()
    return text

def save_text_to_file(text, fname="output_file.txt"):
    f = open(fname, "w+")
    f.write(str(text))
    f.close()

layout = [
    [sg.Text('Asymmetric Cryptography / Key Generator', size=(50, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Frame(layout=[
        [sg.Radio('RSA', default=True, key="RSA", group_id='Method')],
        [sg.Radio('ElGamal', default=False, key="ElGamal", group_id='Method')],
        [sg.Radio('Diffie-Hellman', default=False, key="DH", group_id='Method')],
    ], title='Method',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=[
    [sg.Checkbox('Encrypt/Decrypt From File', default=False, key="EncryptDecryptFromFile")],
    [sg.Checkbox('Key From File', default=False, key="KeyFromFile")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=[
        [sg.Radio('Encrypt', default=True, key="Encrypt", group_id='Encrypt')],
        [sg.Radio('Decrypt', default=False, key="Decrypt", group_id='Encrypt')],
    ], title='Encrypt/Decrypt',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Key format=(<e or d>,<public or private key>) e.g. (79,3337)', size=(45, 1), auto_size_text=False, justification='right',key="key_format",border_width=1)],
    [sg.Text('Key', size=(15, 1), auto_size_text=False, justification='right',key="key_text"),sg.InputText(key="input_key",disabled_readonly_background_color="grey")],
    [sg.Text('Key File', size=(15, 1), auto_size_text=False, justification='right',key="key_file"),sg.InputText(key="input_key_file",disabled_readonly_background_color="grey"), sg.FileBrowse(key='input_file_browse')],
    [sg.Text('Message', size=(15, 1), auto_size_text=False, justification='right',key="input_file_text"),sg.InputText(key="input_message",disabled_readonly_background_color="grey")],
    [sg.Text('Message File', size=(15, 1), auto_size_text=False, justification='right',key="input_file_text"),sg.InputText(key="input_message_file",disabled_readonly_background_color="grey"), sg.FileBrowse(key='input_file_browse')],
    [sg.Text('Output File Name', size=(15, 1), auto_size_text=False, justification='right'),sg.InputText(key="output_file",disabled_readonly_background_color="grey")],
    [sg.Text('Output Message:'), sg.Text(size=(100,1), key='output_message')],
    [sg.Text('DiffieHellman')],
    [sg.Text('n', size=(15, 1), auto_size_text=False, justification='right'),sg.InputText(key="DH_n",disabled_readonly_background_color="grey")],
    [sg.Text('g', size=(15, 1), auto_size_text=False, justification='right'),sg.InputText(key="DH_g",disabled_readonly_background_color="grey")],
    [sg.Text('x', size=(15, 1), auto_size_text=False, justification='right'),sg.InputText(key="DH_x",disabled_readonly_background_color="grey")],
    [sg.Text('y', size=(15, 1), auto_size_text=False, justification='right'),sg.InputText(key="DH_y",disabled_readonly_background_color="grey")],
    [sg.Text('Secret:'), sg.Text(size=(30,1), key='DH_secret')],
    [sg.Submit(), sg.Cancel()]
]

# plaintext = "HELLO ALICE"
# public_key = RSA.read_key(text="(79, 3337)")
# encoded = RSA.encrypt_text(plaintext, public_key)
# save_text_to_file(encoded)
# print(encoded)
# private_key = RSA.read_key(text="(1019, 3337)")
# decoded = RSA.decrypt_text(encoded, private_key)

window = sg.Window('Asymmetric Cryptography',layout, default_element_size=(50, 1), grab_anywhere=False)
while True:
    event, values = window.read(0)
    print(values)
    if values["DH"]:
        window["DH_n"].update(disabled=False)
        window["DH_g"].update(disabled=False)
        window["DH_x"].update(disabled=False)
        window["DH_y"].update(disabled=False)
        window["input_message"].update(disabled=True)
        window["input_message_file"].update(disabled=True)
        window["output_file"].update(disabled=True)
        window["input_key_file"].update(disabled=True)
        window["input_key"].update(disabled=True)
    else:
        window["DH_n"].update(disabled=True)
        window["DH_g"].update(disabled=True)
        window["DH_x"].update(disabled=True)
        window["DH_y"].update(disabled=True)
        if values['EncryptDecryptFromFile']:
            window["input_message"].update(disabled=True)
            window["input_message_file"].update(disabled=False)
            window["output_file"].update(disabled=False)
        else:
            window["input_message"].update(disabled=False)
            window["input_message_file"].update(disabled=True)
            window["output_file"].update(disabled=True)
        if values['KeyFromFile']:
            window["input_key_file"].update(disabled=False)
            window["input_key"].update(disabled=True)
        else:
            window["input_key_file"].update(disabled=True)
            window["input_key"].update(disabled=False)
    if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel':
        break
    elif event == 'Submit':
        if values["RSA"]:
            if values["Encrypt"]:
                plaintext=""
                if values["EncryptDecryptFromFile"]:
                    plaintext = read_text_from_file(values["input_message_file"])
                else:
                    plaintext = values["input_message"]
                public_key = ""
                if values["KeyFromFile"]:
                    public_key = RSA.read_key(fname=values["input_key_file"],from_file=True)
                else:
                    public_key = RSA.read_key(text=values["input_key"])
                ciphertext = RSA.encrypt_text(plaintext, public_key)
                window["output_message"].update(ciphertext)
                print(ciphertext)
                if values["EncryptDecryptFromFile"]:
                    fname = values["output_file"]
                    save_text_to_file(ciphertext,fname)
            if values["Decrypt"]:
                ciphertext =""
                if values["EncryptDecryptFromFile"]:
                    ciphertext = read_text_from_file(values["input_message_file"])
                else:
                    ciphertext = values["input_message"]
                private_key = ""
                if values["KeyFromFile"]:
                    private_key = RSA.read_key(fname=values["input_key_file"],from_file=True)
                else:
                    private_key = RSA.read_key(text=values["input_key"])
                plaintext = RSA.decrypt_text(ciphertext, private_key)
                window["output_message"].update(plaintext)
                if values["EncryptDecryptFromFile"]:
                    fname = values["output_file"]
                    print(plaintext)
                    print(fname)
                    save_text_to_file(plaintext,fname)
        elif values["ElGamal"]:
            #TODO ElGamal
            pass
        elif values["DH"]:
            n = values["DH_n"]
            g = values["DH_g"]
            x = values["DH_x"]
            y = values["DH_y"]
            secret = DiffieHellman.generate_secret_both(n,g,x,y)
            window["DH_secret"].update(secret)

window.close()