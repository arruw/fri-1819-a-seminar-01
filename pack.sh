#!/bin/bash

cd ./app
rm ../solution.zip &> /dev/null
zip -r ../solution.zip *
cd .. 