import PySimpleGUI as sg
import os
import re


def get_routes_jp_data():
    print(os.path.dirname(__file__) + '/ryobi/routes_jp.txt')
    try:
        with open(os.path.dirname(__file__) + '/ryobi/routes_jp.txt', 'r', encoding='utf-8') as f:
            # データの読み出し
            data = f.readlines()

    except (FileExistsError, FileNotFoundError):
        sg.popup_error('routes_jpファイルが見つかりませんでした。')
    except:
        sg.popup_error('routes_jpファイルの読み込み中にエラーが発生しました。')

    # 改行文字の除去
    replace_data = list(map(lambda n: n.replace('\n', ''), data))

    return replace_data


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
                sg.popup('解析結果', str(bus_data_list))
                routes_jp_data = get_routes_jp_data()
                print(routes_jp_data)

        except (FileExistsError, FileNotFoundError):
            sg.popup_error_with_traceback('binファイルが見つかりませんでした。');
        except:
            sg.popup_error_with_traceback('binファイルの読み込み中にエラーが発生しました。');

# ウィンドウの破棄と終了
window.close()
