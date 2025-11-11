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


class Block:
    def __init__(self):
        self.name = ""
        self.begin = 0
        self.size = 0
        self.output = ""


    def from_str(self, line: str):
        cols = line.strip().split(maxsplit=4)
        self.name = cols[0]
        self.begin = int(cols[1], 16)
        self.size = int(cols[2], 16)
        self.output = cols[3]


    def __repr__(self):
        begin = HEX_FORMAT.format(self.begin) 
        size = HEX_FORMAT.format(self.size) 
        return f"Block {{ name: {self.name}, begin: {begin}, size: {size}, output: {self.output} }}"


    def __str__(self):
        """

        Returns
        -------


        """
        begin = HEX_FORMAT.format(self.begin) 
        size = HEX_FORMAT.format(self.size) 
        return f"{self.name} {begin} {size} {self.output}"


    def extract(self, infile, output_path=OUTPUT_PATH_DEFAULT):
        # create part file
        output_filename = os.path.join(output_path, self.output)
        with open(output_filename, 'wb') as outfile:
            infile.seek(self.begin)
            data = infile.read(self.size)
            outfile.write(data)


class BlockList:
    def __init__(self):
        self.blocks = []


    def __repr__(self):
        v = []
        for block in self.blocks:
            v.append(repr(block))
        s = ', '.join(v)
        return f"Blocks [{s}]"


    def __str__(self):
        v = []
        # print each parsed block as a line
        for block in self.blocks:
            v.append(str(block))
        s = '\n'.join(v)
        return s


    def from_str(self, s: str):
        for line in s:
            block = Block()
            block.from_str(line)
            self.blocks.append(block)


    # parse blocks structure from text file map
    def from_file(self, filename):
        #with open('layout.cfg', 'w') as configfile:
        with open(filename, 'r') as f:
            self.from_str(f)


    def extract(self, filename, output_path=OUTPUT_PATH_DEFAULT):

        # open flash dump
        with open(filename, 'rb') as infile:
            # create subdirectory for an output
            os.makedirs(output_path, exist_ok = True)

            # processing blocks with offset and size
            for block in self.blocks:
                block.extract(infile, output_path)



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
                        description='extract, split and save firmware blocks',
                        epilog=MAPFILE_FORMAT_HELP)

    # specify input file
    parser.add_argument('-i', '--input',
                        help='binary firmware file (default: firmware.bin)',
                        default=FIRMWARE_DEFAULT)

    # specify output file
    parser.add_argument('-o',
                        '--output',
                        help='output directory (default: output)',
                        default=OUTPUT_PATH_DEFAULT)

    # specify map file
    parser.add_argument('-m',
                        '--mapfile',
                        help='map file (default: firmware.map)',
                        default=MAPFILE_DEFAULT)

    # print
    parser.add_argument('-p',
                        '--print-blocks',
                        help='print blocks parsed from file',
                        default=False,
                        action='store_true'
                        )

    # dry-run
    parser.add_argument('--dry-run',
                        help='create no files, parse and print info only',
                        default=False,
                        action='store_true'
                        )

    # verbose
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true')

    # version
    parser.add_argument("-V",
                        "--version",
                        action='version',
                        version="%(prog)s 0.2")

    return parser


# use CLI arguments
def use_args(args):
    # blocks
    if args.verbose:
        print(f'reading map file {args.mapfile} ...')

    blocks = BlockList()
    blocks.from_file(args.mapfile)

    # print blocks
    if args.print_blocks:

        if args.verbose:
            print('printing blocks...')

        print(blocks)

    else:
        # firmware input -> output
        if args.verbose:
            print(f'reading firmware file {args.input} ...')
            print(f'saving to output directory {args.output} ...')

        if not args.dry_run:
            blocks.extract(args.input)


# main
if (__name__ == "__main__"):
    parser = create_args()
    args = parser.parse_args()
    use_args(args)
