# 第一阶段：构建前端应用
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json ./
COPY package-lock.json* ./
RUN npm install --only=production

COPY . .
RUN npm run build

# 第二阶段：使用 Nginx 提供静态文件服务
FROM nginx:alpine

# 安装环境变量替换工具
RUN apk add --no-cache gettext

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 80

CMD ["/entrypoint.sh"]
