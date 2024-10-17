#!/bin/sh
CODE_DIR="../"

echo 
echo "Добро пожаловать!"
echo
echo "Короче, выбери вариант и погнали:"
echo
echo "1. (Local): Django"
echo "2. (Local): Django + PostgreSQL"
echo "3. (Dev):   Django + Nginx"
echo "4. (Prod):  Django + Nginx"
echo

read -n1 -p "Что выберешь? [1,2,3,4]: " doit
echo
case $doit in
  1) echo "Запускаю Django"
     read -n1 -p "Билдить? [y/n]: " build_choice
     echo
     if [ "$build_choice" = "y" ]; then
         cd ../docker && \
             docker-compose -f local/docker-compose.local.yaml up --build
     else
         cd ../docker && \
             docker-compose -f local/docker-compose.local.yaml up
     fi
     ;;
  2) echo "Запускаю Django + PostgreSQL"
     read -n1 -p "Билдить? [y/n]: " build_choice
     echo
     if [ "$build_choice" = "y" ]; then
         cd ../docker && \
             docker-compose -f local/docker-compose.local.yaml -f docker-compose.postgres.yaml up --build
     else
         cd ../docker && \
             docker-compose -f local/docker-compose.local.yaml -f docker-compose.postgres.yaml up
     fi
     ;;
  3) echo "Запускаю (Dev): Django + Nginx"
     read -n1 -p "Билдить? [y/n]: " build_choice
     echo
     if [ "$build_choice" = "y" ]; then
         cd ../docker && \
             docker-compose -f dev/docker-compose.dev.yaml up --build
     else
         cd ../docker && \
             docker-compose -f dev/docker-compose.dev.yaml up
     fi
     ;;
  4) echo "Запускаю (Prod): Django + Nginx"
     read -n1 -p "Билдить? [y/n]: " build_choice
     echo
     if [ "$build_choice" = "y" ]; then
         cd ./docker && \
             docker-compose -f production/docker-compose.prod.yaml up --build
     else
         cd ./docker && \
             docker-compose -f production/docker-compose.prod.yaml up
     fi
     ;;
  *) echo "${Red} Такого варианта нет! ${NC}" ;; 
esac
