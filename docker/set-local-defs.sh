#!/bin/bash

LOCAL_KERNEL_NAME=$(uname -s)

if [ ${LOCAL_KERNEL_NAME}='Mac' ]; then
	export SHARE_DATA_PATH='/Users/'$USER'/Projects/NLP_demo/share'
	export GIT_REPO_PATH='/Users/'$USER'/GitHub/NLP_demo'
fi
