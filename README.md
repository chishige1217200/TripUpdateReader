# TripUpdateReader

## How to use
1. Python 3及びpipをインストールする。
2. PySimpleGUIをインストールする。  
`pip install PySimpleGUI`
3. Bus-Visionから[両備バスのバス情報フォーマット形式のデータ](https://loc.bus-vision.jp/gtfs/ryobi/gtfsFeed)をダウンロードし、解凍したryobiフォルダをpyファイルと同じディレクトリに置く。
4. TripUpdateReader.pyを実行し、[ryobi_trip_update.bin](https://loc.bus-vision.jp/realtime/ryobi_trip_update.bin)を読み込ませると、バイナリに含まれる運行ルート、始発時刻、号車番号を表示する。