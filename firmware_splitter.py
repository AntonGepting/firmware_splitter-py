#!/usr/bin/env python3
import sys, os, argparse

# blocks = [
#         {
#             'name': 'uboot',
#             'begin': 0x00000000,
#             'size':  0x00020000,
#             'output': 'uboot.bin',
#         },
#         {
#             'name': 'ubootconfig',
#             'begin': 0x00020000,
#             'size':  0x00020000,
#             'output': 'ubootconfig.bin',
#         },
#         {
#             'name': 'backup_sysconfig',
#             'begin': 0x00040000,
#             'size':  0x00020000,
#             'output': 'backup_sysconfig.bin',
#         },
#         {
#             'name': 'second_firmware',
#             'begin': 0x00060000,
#             'size':  0x00040000,
#             'output': 'second_firmware.bin',
#         },
#         {
#             'name': 'second_rootfs,kernel',
#             'begin': 0x000a0000,
#             'size':  0x00760000,
#             'output': 'second_rootfs_kernel.bin',
#         },
#         {
#             'name': 'backup_uboot',
#             'begin': 0x00800000,
#             'size':  0x00020000,
#             'output': 'backup_uboot.bin',
#         },
#         {
#             'name': 'backup_ubootconfig',
#             'begin': 0x00820000,
#             'size':  0x00020000,
#             'output': 'backup_ubootconfig.bin',
#         },
#         {
#             'name': 'sysconfig',
#             'begin': 0x00840000,
#             'size':  0x00020000,
#             'output': 'sysconfig.bin',
#         },
#         {
#             'name': 'active_firmware',
#             'begin': 0x00860000,
#             'size':  0x00040000,
#             'output': 'active_firmware.bin',
#         },
#         {
#             'name': 'active_rootfs,kernel',
#             'begin': 0x008a0000,
#             'size':  0x00760000,
#             'output': 'active_rootfs_kernel.bin',
#         },
# ]

# input file with map of blocks in firmware
MAPFILE_DEFAULT = 'firmware.map'
# input file with binary firmware
FIRMWARE_DEFAULT = 'firmware.bin'
# output subdirectory
OUTPUT_PATH_DEFAULT = 'output'

# format for printing hex values for block offset and size
HEX_FORMAT = '0x{:08x}'

# field names for structure holding block title, offset, size, output file
FIELD_NAME = 'name'
FIELD_BEGIN = 'begin'
FIELD_SIZE = 'size'
FIELD_OUTPUT = 'output'


# extract each firmware block and save in output dir
def extract(filename, blocks, output_path=OUTPUT_PATH_DEFAULT):
    # open flash dump
    with open(filename, 'rb') as infile:
        # create subdirectory for an output
        os.makedirs(output_path, exist_ok = True)

        # processing blocks with offset and size
        for block in blocks:
            # create part file
            output_filename = os.path.join(output_path, block[FIELD_OUTPUT])
            with open(output_filename, 'wb') as outfile:
                infile.seek(block[FIELD_BEGIN])
                data = infile.read(block[FIELD_SIZE])
                outfile.write(data)


# show given blocks table
def print_blocks(blocks):
    # print each parsed block as a line
    for block in blocks:
        print(block[FIELD_NAME], end=' ')
        print(HEX_FORMAT.format(block[FIELD_BEGIN]), end=' ')
        print(HEX_FORMAT.format(block[FIELD_SIZE]), end=' ')
        print(block[FIELD_OUTPUT], end='\n')


# parse blocks structure from text file map
def read_blocks(filename):
    blocks = []
    #with open('layout.cfg', 'w') as configfile:
    with open(filename, 'r') as f:
        for line in f:
            cols = line.strip().split(maxsplit=4)
            block = { FIELD_NAME: cols[0], FIELD_BEGIN: int(cols[1], 16), FIELD_SIZE: int(cols[2], 16), FIELD_OUTPUT: cols[3] }
            blocks.append(block)

    return blocks


# example of map file
MAPFILE_FORMAT_HELP = '''
    map file syntax:
        <block_name1> <begin>    <size>     <output_filename1>\\n
        <block_name2> <begin>    <size>     <output_filename2>\\n
        ...
    example:
        u-boot        0x00000000 0x00020000 uboot.bin \\n
        u-boot-env    0x00020000 0x00020000 ubootenv.bin
    '''


# create CLI arguments
def create_args():
    parser = argparse.ArgumentParser(
                        prog='firmware_splitter',
                        description='extract and split firmware blocks',
                        epilog=MAPFILE_FORMAT_HELP)
    parser.add_argument('-i', '--input',
                        help='binary firmware file (default: firmware.bin)',
                        default=FIRMWARE_DEFAULT)
    parser.add_argument('-o',
                        '--output',
                        help='output directory (default: output)',
                        default=OUTPUT_PATH_DEFAULT)
    parser.add_argument('-m',
                        '--mapfile',
                        help='map file (default: firmware.map)',
                        default=MAPFILE_DEFAULT)
    parser.add_argument('-p',
                        '--print-blocks',
                        help='print blocks parsed from file',
                        default=False,
                        action='store_true'
                        )
    parser.add_argument('--dry-run',
                        help='create no files, parse and print info only',
                        default=False,
                        action='store_true'
                        )
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true')
    return parser


# use CLI arguments
def use_args(args):
    # blocks
    if args.verbose:
        print(f'reading map file {args.mapfile} ...')

    blocks = read_blocks(args.mapfile)

    # print blocks
    if args.print_blocks:

        if args.verbose:
            print('printing blocks...')

        print_blocks(blocks)

    # firmware input -> output
    if args.verbose:
        print(f'reading firmware file {args.input} ...')
        print(f'saving to output directory {args.output} ...')

    if not args.dry_run:
        extract(args.input, blocks, output_path=args.output)


# main
if (__name__ == "__main__"):
    parser = create_args()
    args = parser.parse_args()
    use_args(args)
