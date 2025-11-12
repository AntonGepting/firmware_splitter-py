# Firmware Splitter

## Description

Simple python script for splitting firmware binary according to given map into the multiple separate files


## Usage

```
firmware_splitter.py -h

usage: firmware_splitter [-h] [-i INPUT] [-o OUTPUT] [-m MAPFILE] [-p] [--dry-run] [-v] [-V]

extract, split and save firmware blocks

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        binary firmware file (default: firmware.bin)
  -o OUTPUT, --output OUTPUT
                        output directory (default: output)
  -m MAPFILE, --mapfile MAPFILE
                        map file (default: firmware.map)
  -p, --print-blocks    print blocks parsed from file
  --dry-run             create no files, parse and print info only
  -v, --verbose
  -V, --version         show program's version number and exit

map file syntax:
<block_name1> <begin> <size> <output_filename1>\n
<block_name2> <begin> <size> <output_filename2>\n
...

block_name      - not used in script, just for better readability of the map
begin           - block begin
size            - size of block
output_filename - file name for block

example:
u-boot 0x00000000 0x00020000 uboot.bin \n
u-boot-env 0x00020000 0x00020000 ubootenv.bin
```


## Licenses

`firmware_splitter.py` is licensed under the MIT license. Please read the
[license file](LICENSE.md) in the repository for more information.
