FROM node:16-alpine

WORKDIR /app

#simple-mercari-webディレクトリを/appにコピー
COPY . .

RUN addgroup -S mercari && adduser -S trainee -G mercari
RUN chown -R trainee:mercari node_modules
USER trainee

CMD ["npm", "start"]
