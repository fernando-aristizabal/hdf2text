# HDF2TEXT
Command line python function to convert HDF5 file to ASCII format on terminal.

Tested with Python==3.10.6, Pandas==1.5.1, and PyTables==3.7.0 on Linux Bash.

Run:

Basic example: `./hdf2text.py -r <your_hdf_file> -k <your_hdf_key>`

Complete example: `./hdf2text.py -r <your_hdf_file> -k <your_hdf_key> --start <start_row_index> --stop <stop_row_index> --read-columns <col1_to_read> <col2_to_read>`

For help: `./hdf2text.py --help`

