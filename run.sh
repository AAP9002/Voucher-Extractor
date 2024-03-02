#!/bin/bash

echo "Running setup.sh"
./setup.sh > /dev/null 2>&1
echo "Running main.py"
python3 main.py
echo "Running generatePdf.sh"
./generatePdf.sh
open bin/output.pdf