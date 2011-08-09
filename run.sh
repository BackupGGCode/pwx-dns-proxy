#!/bin/sh
echo 在 Linux 下面侦听端口必须要有 root 权限。
echo 因此，这个脚本会向您询问 su 权限。

sudo python src/dnsproxy.py
