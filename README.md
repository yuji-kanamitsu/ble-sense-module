# BLE Sense Module
ラズパイ用BLEセンシングモジュール。ラズパイ起動時に自動実行する仕様。


## Function
以下３つのファイルを起動時に同時に実行する。

#### ❏ sense.py
周辺のBLEデバイスを受信。ローカルデータベースに保存。

#### ❏ send.py
ローカルデータベースから未ポストのデータをサーバーへ送信。

#### ❏ delete.py
７日より前のデータをローカルデータベースから削除。


## Set up
#### 1. ダウンロード
```
git clone https://github.com/yuji-kanamitsu/ble-sense-module.git
```

#### 2. BLEドングルの設定
❏ ポート解放<br>
GUIで操作する場合: `menu` -> `setting` -> `interface` -> `serial port` -> `"on"`

❏ アドレス設定<br>
ターミナルで
```
$ hciconfig
------------
Bus: USB # ドングルが認識されている
BD Address: [bd_address] # BDアドレス
```

myconfig/config.iniを編集
```
...

[BDAddress]
dongle = [bd_address] # 先ほどチェックしたアドレスに変更

...

[Meta]
sensorID = [sensor_id] # ついでにセンサーIDも適宜変更
```

#### 3. ワーキングディレクトリの設定
myconfig/configmaker.py
```
...

def read_config():
  cwd = "[../ble-sense-module]" # プロジェクトをダウンロードした場所に変更
```

#### 4. 自動実行の設定
/etc/rc.local
```
...

# 追加
sudo python3 /home/pi/[path]/sense.py & python3 /home/pi/[path]/send.py & python3 /home/pi/[path]/delete.py $ # 絶対パスで指定する必要あり

exit 0
```

#### 5. データベースの権限変更 (不要にしたいけどまだできてない)
一度`sense.py`を実行してみる。
```
sudo python3 sense.py
```

すると`db/test__db3.sqlite3`というファイルが作成される。<br>
はじめ、このデータベースを編集する権限がない（データの編集や削除ができない）ので権限を変更する。
```
sudo chmod 777 db/test_db3.sqlite3
```

初めから権限を緩めたデータベースを作成する、もしくは強い権限をもって操作できるように改善の余地あり。

#### 6. テスト
再起動
```
sudo reboot
```

実行されているか確認
```
ps aux | grep python
```

無事に自動実行されていれば指定ファイルが表示される。
