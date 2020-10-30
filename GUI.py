import PySimpleGUI as sg
import RSA
import DiffieHellman
import sys

layout = [
    [sg.Text('Asymmetric Cryptography', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Frame(layout=[
    [sg.Checkbox('Encrypt/Decrypt From File', default=False, key="EncryptFromFile")],
    [sg.Checkbox('Key From File', default=False, key="KeyFromFile")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=[
        [sg.Radio('Encrypt', default=False, key="Encrypt", group_id='Encrypt')],
        [sg.Radio('Decrypt', default=False, key="Decrypt", group_id='Encrypt')],
    ], title='Encrypt/Decrypt',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=[
        [sg.Radio('RSA', default=False, key="RSA", group_id='Method')],
        [sg.Radio('ElGamal', default=False, key="ElGamal", group_id='Method')],
    ], title='Cryptography Method',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Key format=(<e or d>,<public or private key>) e.g. (79,3337)', size=(45, 1), auto_size_text=False, justification='right',key="key_format",border_width=1)],
    [sg.Text('Key', size=(15, 1), auto_size_text=False, justification='right',key="key_text"),sg.InputText(key="input_key",disabled_readonly_background_color="grey")],
    [sg.Text('Key File', size=(15, 1), auto_size_text=False, justification='right',key="key_file"),sg.InputText(key="input_key_file",disabled_readonly_background_color="grey"), sg.FileBrowse(key='input_file_browse')],
    [sg.Text('Message', size=(15, 1), auto_size_text=False, justification='right',key="input_file_text"),sg.InputText(key="input_message",disabled_readonly_background_color="grey")],
    [sg.Text('Message File', size=(15, 1), auto_size_text=False, justification='right',key="input_file_text"),sg.InputText(key="input_file",disabled_readonly_background_color="grey"), sg.FileBrowse(key='input_file_browse')],
    [sg.Text('Output File Name', size=(15, 1), auto_size_text=False, justification='right'),sg.InputText(key="output_file",disabled_readonly_background_color="grey")],
]


window = sg.Window('Asymmetric Cryptography',layout, default_element_size=(50, 1), grab_anywhere=False)
while True:
    event, values = window.read(1)
    print(values)
    if values['EncryptFromFile']:
        window["input_message"].update(disabled=True)
        window["input_file"].update(disabled=False)
        window["output_file"].update(disabled=False)
    else:
        window["input_message"].update(disabled=False)
        window["input_file"].update(disabled=True)
        window["output_file"].update(disabled=True)
    if values['KeyFromFile']:
        window["input_key_file"].update(disabled=False)
        window["input_key"].update(disabled=True)
    else:
        window["input_key_file"].update(disabled=True)
        window["input_key"].update(disabled=False)
    if values["RSA"]:
        if values["Encrypt"]:
            text=""
            if values["EncryptFromFile"]:
                pass
            else:
                text = values["input_message"]
            public_key = ""
            if values["KeyFromFile"]:
                public_key = DiffieHellman.read_key(values["input_key_file"])
            else:
                public_key = values["input_key"]
            RSA.encrypt_text(text, public_key)
        if values["Decrypt"]:
            pass
    elif values["ElGamal"]:
        #TODO ElGamal
        pass
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()