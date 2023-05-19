FROM python:3.11.3-alpine

RUN addgroup -S mercari && adduser -S trainee -G mercari

WORKDIR /app

#FastAPIとかインストールする
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pillow

#pythonディレクトリを/appにコピー
COPY . .
#dbディレクトリを/dbにコピー
COPY db /db

#Dockerでの権限を設定する
RUN chown -R trainee:mercari db && chown -R trainee:mercari images 
USER trainee

#サーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

# CMD ["python", "-V"]
