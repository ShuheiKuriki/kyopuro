# Usage

## Requirements
Please install a compiler for Rust language (see https://www.rust-lang.org).

## Input Generation
Prepare `seeds.txt` which contains a list of random seeds (unsigned 64bit integers) and execute the following command.
```
cargo run --release --bin gen seeds.txt
```

This will output input files into `in` directory.

## Testing
Let `in.txt` be an input file, `out.txt` be a file to which output of your program will be written, and `cmd` be a command to run your program.
You can test your program by executing the following command.
```
cargo run --release --bin tester cmd < in.txt > out.txt
```
The above command outputs the score to standard error.
You can specify arguments to your program by 
```
cargo run --release --bin tester cmd arg1 arg2 ... < in.txt > out.txt
```

## Visualization
Let `in.txt` be an input file and `out.txt` be an output file.
You can visualize the output by executing the following command.
```
cargo run --release --bin vis in.txt out.txt
```
The above command writes a visualization result to `vis.html`.
You can also use a [web visualizer](https://img.atcoder.jp/ahc008/fa9d69020e638e81975a2c631d1b.html?lang=en) which is more rich in features.

## Acknowledgements
We used images from [DOTOWN](https://dotown.maeda-design-room.net/).

# 使い方

## 実行環境
Rust言語のコンパイル環境が必要です。
https://www.rust-lang.org/ja を参考に各自インストールして下さい。

## 入力生成
`seeds.txt` に欲しい入力ファイルの数だけ乱数seed値(符号なし64bit整数値)を記入し、以下のコマンドを実行します。
```
cargo run --release --bin gen seeds.txt
```

生成された入力ファイルは `in` ディレクトリに出力されます。

## テスト実行
入力ファイル名を`in.txt`、出力結果を書き出す先のファイル名を`out.txt`、あなたのプログラムの実行コマンドを`cmd`としたとき、以下のコマンドを実行します。
```
cargo run --release --bin tester cmd < in.txt > out.txt
```
実行が終わると、スコアが標準エラーに出力されます。
引数が必要な場合には
```
cargo run --release --bin tester cmd arg1 arg2 ... < in.txt > out.txt
```
のようにします。

## ビジュアライザ
入力ファイル名を`in.txt`、出力ファイル名を`out.txt`としたとき、以下のコマンドを実行します。
```
cargo run --release --bin vis in.txt out.txt
```
出力のビジュアライズ結果は `vis.html` というファイルに書き出されます。
より機能が豊富な[ウェブ版のビジュアライザ](https://img.atcoder.jp/ahc008/fa9d69020e638e81975a2c631d1b.html)も利用可能です。

## 謝辞
画像は [DOTOWN](https://dotown.maeda-design-room.net/) のものを利用させていただきました。
