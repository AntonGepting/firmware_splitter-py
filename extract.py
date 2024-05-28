#!/bin/python3

input_file = 'factory_firmware.bin'

blocks = [
        {
            'name': 'uboot',
            'begin': 0x00000000,
            'size':  0x00020000,
            'output': 'uboot.bin',
        },
        {
            'name': 'ubootconfig',
            'begin': 0x00020000,
            'size':  0x00020000,
            'output': 'ubootconfig.bin',
        },
        {
            'name': 'backup_sysconfig',
            'begin': 0x00040000,
            'size':  0x00020000,
            'output': 'backup_sysconfig.bin',
        },
        {
            'name': 'second_firmware',
            'begin': 0x00060000,
            'size':  0x00040000,
            'output': 'second_firmware.bin',
        },
        {
            'name': 'second_rootfs,kernel',
            'begin': 0x000a0000,
            'size':  0x00760000,
            'output': 'second_rootfs_kernel.bin',
        },
        {
            'name': 'backup_uboot',
            'begin': 0x00800000,
            'size':  0x00020000,
            'output': 'backup_uboot.bin',
        },
        {
            'name': 'backup_ubootconfig',
            'begin': 0x00820000,
            'size':  0x00020000,
            'output': 'backup_ubootconfig.bin',
        },
        {
            'name': 'sysconfig',
            'begin': 0x00840000,
            'size':  0x00020000,
            'output': 'sysconfig.bin',
        },
        {
            'name': 'active_firmware',
            'begin': 0x00860000,
            'size':  0x00040000,
            'output': 'active_firmware.bin',
        },
        {
            'name': 'active_rootfs,kernel',
            'begin': 0x008a0000,
            'size':  0x00760000,
            'output': 'active_rootfs_kernel.bin',
        },
]

# show given blocks table
def display_blocks():
    for block in blocks:
        print(block['name'], end=' ')
        print('0x{:08x}'.format(block['begin']), end=' ')
        print('0x{:08x}'.format(block['size']), end=' ')
        print(block['output'], end='\n')

def extract():
    # open flash dump
    with open(input_file, 'rb') as infile:
        # woriking with defined blocks
        for block in blocks:
            # create part file
            with open(block['output'], 'wb') as outfile:
                infile.seek(block['begin'])
                data = infile.read(block['size'])
                outfile.write(data)

display_blocks()

extract()



