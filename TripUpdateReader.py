import PySimpleGUI as sg
import os
import re


def get_routes_data():
    try:
        with open(os.path.dirname(__file__) + '/ryobi/routes.txt', 'r', encoding='utf-8') as f:
            # データの読み出し
            data = []
            for line in f:
                data.append(line.split(','))

    except (FileExistsError, FileNotFoundError):
        sg.popup_error('routesファイルが見つかりませんでした。')
    except:
        sg.popup_error('routesファイルの読み込み中にエラーが発生しました。')

    replace_data_list = []
    # 改行文字の除去
    for i in range(1, len(data)):
        replace_data = []
        for j in range(len(data[i])):
            replace_data.append(data[i][j].replace('\n', ''))
        replace_data_list.append(replace_data)

    return replace_data_list


def get_routes_long_name(route_id, routes_data):
    return search(route_id, routes_data, 3)


def get_routes_short_name(route_id, routes_data):
    return search(route_id, routes_data, 2)


def search(param, target, return_column_id):
    for i in range(0, len(target)):
        if target[i][0] in param:
            return target[i][return_column_id]
    return '無効路線'


# オプションの設定と標準レイアウト
sg.theme('LightGrey')

layout = [
    [sg.Text('このプログラムはhttps://loc.bus-vision.jp/ryobi/view/opendata.htmlで公開されている\n両備バス（https://www.ryobi-holdings.jp/bus/）のオープンデータを解析します。')],
    [sg.Text('"./ryobi" 配下に両備バスの標準的なバス情報フォーマット形式のデータを配置してください。')],
    [sg.Text('ryobi_trip_update.binファイルパス'),
     sg.InputText(), sg.FileBrowse(key="file")],
    [sg.Submit(button_text='解析実行')]
]

# ウィンドウの生成
window = sg.Window('RyobiTripUpdateReader', layout)

# イベントループ
while True:
    event, values = window.read()

    if event is None:
        print('exit')
        break

    if event == '解析実行':
        try:
            with open(os.path.basename(os.path.normpath(values[0].replace('"', ''))), 'rb') as f:
                # バイナリデータの読み出し
                data = str(f.read())

                # 文字情報以外を除去
                data = re.sub(
                    r'\\x([01][0123456789abcdef]|[890abcdef][0123456789abcdef])', '', data)

                # 各ダイヤごとに分離（1次元リスト化）
                contents_list = re.split(r'!tripUpdate_', str(data))

                # 各ダイヤの情報ごとに分離（2次元リスト化）
                bus_data_list = []
                for i in range(1, len(contents_list)):

                    # バス運行路線、始発時刻、バス号車番号を取得
                    try:
                        bus_data = []
                        bus_data.append(
                            re.search(r'\d{5,5}+_\d{3,7}+_\d+', contents_list[i]).group())
                        bus_data.append(
                            re.search(r'\d{2,2}:\d{2,2}:\d{2,2}', contents_list[i]).group())
                        bus_data.append(
                            re.search(r'F\d{4,4}', contents_list[i]).group())
                        bus_data_list.append(bus_data)
                    except:
                        print("バス情報が正常に抽出できませんでした。")

                if len(bus_data_list) == 0:
                    sg.popup('解析結果', '表示する情報はありません。')
                    continue

                bus_data_list = sorted(
                    bus_data_list, reverse=False, key=lambda x: x[1])
                bus_data_list = sorted(
                    bus_data_list, reverse=False, key=lambda x: x[0])
                print(bus_data_list)
                # sg.popup('解析結果', str(bus_data_list))

        except (FileExistsError, FileNotFoundError):
            sg.popup_error_with_traceback('binファイルが見つかりませんでした。')
        except:
            sg.popup_error_with_traceback('binファイルの読み込み中にエラーが発生しました。')

        routes_data = get_routes_data()
        # print(routes_jp_data)

        for i in range(0, len(bus_data_list)):
            bus_data_list[i][0] = get_routes_short_name(
                bus_data_list[i][0], routes_data)

        print(bus_data_list)
        # sg.popup('解析結果', str(bus_data_list))

        header = ['運行ルート', '始発時刻', '号車番号']
        widths = [60, 10, 8]

        # テーブルオブジェクト作成
        L = [[sg.Table(bus_data_list, headings=header,
                       col_widths=widths, justification='left', expand_x=True, expand_y=True, auto_size_columns=False)]]

        # ウィンドウ作成
        window = sg.Window('解析結果', L,  resizable=True)

# ウィンドウの破棄と終了
window.close()
