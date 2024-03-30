# pip install requests parsel json random PySimpleGUI

import PySimpleGUI as sg
from parser import ScrapeParse
import utils

tabgrp = [
          [
          sg.Text("Request input: ", size=(15, 1)),
          sg.Text("Page input: ", size=(14, 1), key='PAGE_INPUT'),
          sg.Text("Request now: ", size=(15, 1)),
          sg.Text("Page now: ", size=(12, 1), key='PAGE_NOW')
          ],
          [
           sg.InputText(size=(15, 1)),
           sg.InputText(size=(15, 1)),
           sg.Text("", size=(15, 1), key='REQUEST', background_color='White', text_color='Black'),
           sg.Text("", size=(15, 1), key='PAGE_N', background_color='White', text_color='Black')
          ],
          [
           sg.Button('Ok'),
           sg.Button('Clear'),
           sg.Checkbox("Redaction", key='redact')
          ],
          [
           sg.TabGroup([
              [
               sg.Tab('All', [[sg.Output(size=(88, 20), key='ALL')]], background_color='Blue'),
               sg.Tab('News', [[sg.Output(size=(88, 20), key='NEWS')]], background_color='Green'),
               sg.Tab('Videos', [[sg.Output(size=(88, 20), key='VIDEOS')]], background_color='Purple'),
               sg.Tab('Books', [[sg.Output(size=(88, 20), key='BOOKS')]], background_color='Red')
              ]
           ],
           tab_location='topleft', title_color='White', tab_background_color='Gray',
           selected_title_color='Yellow', selected_background_color='Gray',
           border_width=5, enable_events=True, key="tab_group")
          ],
          [
           sg.Button('Back'),
           sg.Button('Next'),
           sg.Button('Exit')
          ]
        ]

page_n = -1
dict_tab = {'ALL': '', 'VIDEOS': '&tbm=vid', 'NEWS': '&tbm=nws', 'BOOKS': '&tbm=bks', }
request = ''

window = sg.Window("Parser", tabgrp, finalize=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Ok':
        request = values[0]
        if values[1] == '':
            if page_n == -1:
                page_n = 0
        else:
            try:
                page_n = int(values[1])
                window['PAGE_NOW'].update('Page now: ')
            except:
                window['PAGE_NOW'].update('ERROR')
                continue
    elif event == 'Next':
        page_n += 1
    elif event == 'Back' and page_n > 0:
        page_n -= 1
    else:
        page_n = 0

    if event in ['Ok', 'Next', 'Back']:
        window['PAGE_NOW'].update('Page now: ')
        window['PAGE_N'].update(page_n)

    if event in ['Ok', 'Next', 'Back'] and request != '':
        parse = ScrapeParse(url=request)
        window['REQUEST'].update(request)
        dict_parse = parse.parse(tab_dict_parse=dict_tab[values['tab_group'].upper()], page=page_n * 10)
        if dict_parse == []:
            window[values['tab_group'].upper()].update(value='No result found!')
        else:
            if values['redact']:
                window[values['tab_group'].upper()].update('\n'.join(utils.redact_parse(dict_parse)))
            else:
                window[values['tab_group'].upper()].update(value=parse.print(dict_parse))
    elif event == 'Clear':
        window[values['tab_group'].upper()].update(value=' ')

window.close()
