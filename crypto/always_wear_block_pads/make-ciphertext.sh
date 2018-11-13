#!/bin/sh

openssl aes-128-cbc -K 746869735f69736e745f615f666c6167 -iv 0 -in plaintext.txt -out ciphertext.bin
