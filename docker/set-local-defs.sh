#!/bin/bash

LOCAL_KERNEL_NAME=$(uname -s)

if [ ${LOCAL_KERNEL_NAME}='Mac' ]; then
	export TESTING_DATA_PATH='/Users/kari.antila/Projects/NLP_demo/testing/' 
fi
