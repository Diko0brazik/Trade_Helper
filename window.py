import PySimpleGUI as sg
from  threading     import Thread





def get_main_window():
    layout = [
        [sg.Text("trading"), sg.Text('automated trading = '), sg.Text('', key='automated trading')], 
        [sg.Button("up"), sg.Button('down'), 
            sg.Button("start automated trading"), sg.Button('stop automated trading'),],
        [sg.Text("tiker", key='tiker'), 
            sg.Input(default_text='EURUSD', key='inp_tiket'),
            sg.Button('change ticker') 
            ],
        [sg.Text('Last price = '), sg.Text('0', key='last_price')],
        [sg.Text('Strategy data = '), sg.Text('', key='strategy_data')],
        # [sg.Listbox(values=[], 
        #             enable_events=True, 
        #             size=(40, 20), 
        #             key="trades")
        #             ],
        [sg.Button("save cookies")], 
        ]
    window = sg.Window("trade", layout, finalize=True)
    return(window)
