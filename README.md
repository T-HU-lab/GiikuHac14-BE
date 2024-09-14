# GiikuHac14-BE　環境構築方法

## コンテナ作成
以下のコマンドを実行
```
$ docker-compose build

$ docker-compose run --entrypoint "poetry install --no-root" demo-app

$ docker-compose up
``` 

## データベース作成
apiコンテナにアタッチし、ターミナルで以下を実行
```
$ poetry run alembic upgrade head
```
データベースのバージョンが更新されるたびにこのコマンドを実行する必要があり