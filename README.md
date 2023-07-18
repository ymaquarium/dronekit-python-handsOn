# dronekit-python-handsOn
「ドローンエンジニア養成塾」2023年春学期のDay4課題の実施コード。

# 動作環境
- Windows 10 version 22H2
- Ubuntu 20.04.6LTS
- VSCode 1.80.1
- Python 3.8.10
- Mission Planner 1.3.80

# 接続機体（シミュレータを利用しない場合）
- ArduPilot 4.1.1以降（Wi-Fi接続）

# 環境構築手順
## ArduPilotソースコードのクローン
ホームディレクトリに、GitHubのArduPilotリポジトリよりソースコードをクローン。  
`cd `    
`git clone https://github.com/ArduPilot/ardupilot.git`    
  
Ubuntuにてビルド環境をセットアップ    
`cd ardupilot`    
`./Tools/environment_install/install-prereqs-ubuntu.sh -y`

## Dronekit Pythonのインストール
ホームディレクトリにて以下のコマンドを順次実行。  
`git clone https://github.com/dronekit/dronekit-python`  
`cd dronekit-python`  
`pip3 install . --user`  

## このリポジトリのソースコードをクローン
`cd `  
`git clone https://github.com/ymaquarium/dronekit-python-handsOn`  

# 動作確認手順
機体とPCをWi-Fi接続させ、Wi-Fiプロパティから機体のIPアドレスを取得。    
ホームディレクトリにて、以下のコマンドを実行。  
`mavproxy.py --master=udp:DRONE-IP-ADDRESS:14550 --out=127.0.0.1:14551`  
<br>
別のターミナルタブを開き、以下のコマンドを実行。  ！！ドローンが飛行開始するため注意！！  
`python3 /dronekit-python-handsOn/flightExperience.py`  
