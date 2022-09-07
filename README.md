# vgmpico
[Raspberry PICO](https://www.switch-science.com/catalog/6900/)向けの[VGMファイル](https://www.jpedia.wiki/blog/en/VGM_(file_format))簡易プレイヤーです。<br>
## 1.PSG(AY-3-8910やYMZ294)1個向けに作られたVGMファイルをPWMで鳴らすことが出来ます。<br>
### 使うもの
 - Raspbery pico(以降Pico) 1個
 - ブレッドボード
 - 小型スピーカまたはイヤホン
 - ジャンパ線適宜
 
### 設定
firmware.uf2をPicoにアップロードします<br>
main.pyの以下の行を変更します<br>
16行目: Pwm_enabled (Trueにすると有効)<br>
17行目: Pwm_pin = 26 (スピーカー(+)を接続するピン)<br>

### つなぎ方
1.以下の様に物理結線を行います。<br> 
 - Picoの3.3V OUT (物理36ピン)をLPC810の6ピンに接続
 - PicoのGND (物理38ピンなど)をLPC810の7ピンに接続
 - イヤホンやアンプのGND端子にPicoのGND (物理38ピンなど)を接続
 - イヤホンやアンプのAudio端子に26ピンを接続

## 2.PSG(AY-3-8910やYMZ294)２個か、PSG１個とSSC(K051649)１個向けに作られたVGMファイルを鳴らすことができます。<br>
音源チップとして[とよしまさん](https://twitter.com/toyoshim)が作られた[SoundCortexLPC](https://github.com/toyoshim/SoundCortexLPC)を使います。<br>
### 使うもの
 - Raspbery pico(以降Pico) 1個
 - LPC810 2個
 - プルアップ用抵抗(2～10KΩ) 4本
 - ブレッドボード
 - 小型スピーカまたはイヤホン
 - ジャンパ線適宜

### 設定
main.pyの以下の行を変更します
10行目: Scc_enabled (Trueにすると有効)

### つなぎ方
1.[I2Cで制御できる80円のPSG互換チップで遊ぼう](https://qiita.com/toyoshim/items/22a173d267f3c90fe36f)を基に、LPC810にSoundCoretexLPCを焼きます。<br>
2.Pico１個とLPC810２個をブレッドボードに刺します。<br>
3.以下の様に物理結線を行います。<br> 
 - Picoの3.3V OUT (物理36ピン)をLPC810の6ピンに接続
 - PicoのGND (物理38ピンなど)をLPC810の7ピンに接続
 - PicoのGP0 (物理1ピン)を1個目のLPC810の8ピンに接続、併せて2～10KΩの抵抗経由で3.3Vにも接続
 - PicoのGP1 (物理2ピン)を1個目のLPC810の1ピンに接続、併せて2～10KΩの抵抗経由で3.3Vにも接続
 - PicoのGP2 (物理4ピン)を2個目のLPC810の8ピンに接続、併せて2～10KΩの抵抗経由で3.3Vにも接続
 - PicoのGP3 (物理5ピン)を2個目のLPC810の1ピンに接続、併せて2～10KΩの抵抗経由で3.3Vにも接続
 - イヤホンやアンプのGND端子にPicoのGND (物理38ピンなど)を接続
 - イヤホンやアンプのAudio端子に1個目と2個目のLPC810の2ピンを接続、100Ω以下の抵抗を経由すると良い説有
![接続図](https://user-images.githubusercontent.com/111331376/186407765-80e2dc41-8b9d-4329-b2ba-1962ad221c98.png)


## 使い方
 - VGMファイルがvgz形式の場合、7zipやgzipなどで展開しvgm形式にする
 - [Thonny](https://thonny.org/)などを使い、main.pyと上記vgmファイルを同じディレクトリに転送する
 - Thonnyの実行を押すか、再起動するとmain.pyと同じディレクトリのvgmファイルが読み込まれ、再生が始まる

## 制限
 - VGMコマンド全てには対応していません。
 - ループ回数はソース内の定数部分に有ります。
 - 読み込めるVGMファイルサイズは160Kbyte位までです。
 - 音が小さいのでアンプを繋ぐと良いです。耳が若い人向けにはローパスフィルタもおすすめです。
 - Picoのタイマ分解能の関係で1サンプルが0.33マイクロ秒くらい遅いです（*´∀｀*）
 - 本記事内容及びプログラムを使用したことにより発生する、いかなる損害も補償しません。

## ライセンス
 [Apache License v2.0](http://www.apache.org/licenses/LICENSE-2.0)に基づいてご利用ください。ご連絡は[layer8](https://twitter.com/layer812)までお願いします。
