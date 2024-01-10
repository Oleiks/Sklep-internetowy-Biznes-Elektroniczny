FROM prestashop/prestashop:1.7.8

RUN apt-get update && \
    apt-get install -y \
        memcached \
        libmemcached-dev \
        libmemcached11 \
        libmemcachedutil2 \
		systemctl

RUN pecl install memcached && \
    docker-php-ext-enable memcached

CMD ["bash", "-c", "service memcached start && apache2-foreground"]

RUN rm -rf /var/www/html/*

COPY ./psdata /var/www/html

RUN chmod -R 777 /var/www/html

COPY ./prestashop.crt /etc/ssl/certs/prestashop.crt
COPY ./prestashop.key /etc/ssl/private/prestashop.key
COPY ./prestashop-ssl.conf /etc/apache2/sites-available/prestashop-ssl.conf

RUN a2enmod ssl && \
    a2ensite prestashop-ssl