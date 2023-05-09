# 環境

- docker
- Debian
- python3.8

# 実行手順

```bash
# Dockerfileがあるディレクトリで以下のコマンドを実行し、Dockerイメージを作成
$ docker build -t profiling-linux .
# Dockerイメージが作られたら、それを使ってコンテナを起動
$ docker run -v "$(pwd)":/app profiling-linux
```
