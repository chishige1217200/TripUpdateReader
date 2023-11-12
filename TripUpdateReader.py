import PySimpleGUI as sg
import os
import re

# オプションの設定と標準レイアウト
# sg.theme('Dark Blue 3')

main_directory = os.path.dirname(__file__)

layout = [
    [sg.Text('このプログラムはhttps://loc.bus-vision.jp/ryobi/view/opendata.htmlで公開されている\n両備バス（https://www.ryobi-holdings.jp/bus/）のオープンデータを解析します。')],
    [sg.Text('"./ryobi" 配下に両備バスの標準的なバス情報フォーマット形式のデータを配置してください。')],
    [sg.Text('ryobi_trip_update.binファイルパス'), sg.InputText(), sg.FileBrowse(key="file")],
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

                print()
                bus_data_list = sorted(
                    bus_data_list, reverse=False, key=lambda x: x[1])
                bus_data_list = sorted(
                    bus_data_list, reverse=False, key=lambda x: x[0])
                print(bus_data_list)
                sg.popup('解析結果', str(bus_data_list))

        except (FileExistsError, FileNotFoundError):
            sg.popup_error('ファイルが見つかりませんでした。')
        except:
            sg.popup_error('ファイルの読み込み中にエラーが発生しました。')




            

# ウィンドウの破棄と終了
window.close()

def get_routes_jp_data():
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

        print()
        bus_data_list = sorted(
            bus_data_list, reverse=False, key=lambda x: x[1])
        bus_data_list = sorted(
            bus_data_list, reverse=False, key=lambda x: x[0])
        print(bus_data_list)
        sg.popup('解析結果', str(bus_data_list))

    except (FileExistsError, FileNotFoundError):
        sg.popup_error('ファイルが見つかりませんでした。')
    except:
        sg.popup_error('ファイルの読み込み中にエラーが発生しました。')
    return