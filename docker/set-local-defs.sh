#!/bin/bash

LOCAL_KERNEL_NAME=$(uname -s)

if [ ${LOCAL_KERNEL_NAME}='Mac' ]; then
	export SHARE_DATA_PATH='/Users/kari.antila/Projects/NLP_demo/share'
fi
