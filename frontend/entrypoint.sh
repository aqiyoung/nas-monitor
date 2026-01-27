#!/bin/sh

# 如果设置了VITE_API_BASE_URL环境变量，替换nginx配置中的代理目标
if [ -n "$VITE_API_BASE_URL" ]; then
    echo "Using API base URL: $VITE_API_BASE_URL"
    # 使用sed替换代理目标
    sed -i "s|proxy_pass http://backend:8017/;|proxy_pass $VITE_API_BASE_URL;|g" /etc/nginx/conf.d/default.conf
else
    echo "Using default API base URL: http://backend:8017"
fi

# 启动nginx
nginx -g "daemon off;"