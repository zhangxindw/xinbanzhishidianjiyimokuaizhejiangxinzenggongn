#!/bin/bash
cat > /etc/nginx/conf.d/quiz-system.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        root /var/www/quiz-system/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:5000/;
    }
}
EOF

rm -f /etc/nginx/sites-enabled/default
nginx -t && service nginx restart && echo "Nginx配置完成"