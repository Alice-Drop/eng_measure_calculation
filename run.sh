#!/bin/bash

APP_PATH="./dist/main.app/Contents/MacOS/main"

if [ -f "$APP_PATH" ]; then
  echo "运行主程序..."
  "$APP_PATH"
else
  echo "错误：找不到 $APP_PATH"
  exit 1
fi
