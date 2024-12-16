@echo off

call openssl speed

call rhash --benchmark

call john --test

call 7z b

winsat cpu -encryption
