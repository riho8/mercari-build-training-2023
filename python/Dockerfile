FROM alpine

RUN addgroup -S mercari && adduser -S trainee -G mercari
#alpineからpython3とpip3をインストールして、バージョンを確認する
RUN apk update && apk add --no-cache python3 py3-pip && python3 --version && pip3 --version
# RUN chown -R trainee:mercari /path/to/db

WORKDIR /app

#FastAPIとかインストールする
COPY python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#pythonディレクトリを/appにコピー
COPY python .
#dbディレクトリを/dbにコピー
COPY ../db /db

#サーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

# CMD ["python", "-V"]
