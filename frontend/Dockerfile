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

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
