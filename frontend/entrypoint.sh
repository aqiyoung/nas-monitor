#!/bin/sh

# 替换nginx配置中的环境变量
envsubst '${API_BASE_URL}' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp && mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf

# 启动nginx
nginx -g "daemon off;"