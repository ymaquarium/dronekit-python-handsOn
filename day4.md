# build
フラコンのUSB3にブザーを追加していつもの音が出るようになる
電源は分電盤、モーターは各ESCから制御となる
分電盤およびESCとFCUを接続して、各モーターの制御ができるようになる
FCUのUSB-microBにPCと接続することでも、FCUへの電源供給ができる（mission plannerへの接続も可能に）

# first test
mission plannerから各種設定→各種モーターのテストで実施（スロットル量は適時調整、day4では16-18）
回転方向が逆の場合は、3本のケーブルのうちの2つを入れ替える
mission plannerのモーター認識A-Dと、マルチコプターとしての回転番号（左・右回り）の1-4の相違に注意

# tuning
パラメータリストのうち、フルパラメータツリーだとグルーピングされていてわかりやすい
普段使うやつはスタンダードパラメータでよさそう

# lua script
飛行制御に影響を及ぼさず、ArduPilotへの機能追加をするときに使える
パラメータのSCR_ENABLEを1にして使うようにする
STABLIZE> param show SCR_ENABLEなど、例の画面で変更できるようになる
パラメータを変更した場合、再起動が必要
sim_vehicle.pyを動かすディレクトリの下に/scriptsフォルダを作成し、そこにlua scriptを作成する
mission plannerなら、設定→mavftpで設定する
.(dot)はluaのライブラリ、:(colon)はardupilotのライブラリ呼び出しを行っている
