#!/bin/bash

rm app.zip &> /dev/null
rm solution &> /dev/null
cd app
zip -r ../app.zip * &> /dev/null
cd .. 

echo '#!/usr/bin/env python3' | cat - app.zip > solution
chmod u+x solution

rm app.zip &> /dev/null