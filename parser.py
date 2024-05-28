#!/bin/python3

import configparser


config = configparser.ConfigParser()


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

with open('layout.cfg', 'w') as configfile:
    for block in blocks:
        config[block['name']] = {'begin': '0x{:08x}'.format(block['begin']), 'size':
                                 '0x{:08x}'.format(block['size']), 'output': block['output']}
    config.write(configfile)


blocks = []

#with open('layout.cfg', 'w') as configfile:
config.read('layout.cfg')
for section in config.sections():
    begin = int(config[section]['begin'], 16)
    size = int(config[section]['size'], 16)
    output = config[section]['output']
    blocks.append({ 'name': section, 'begin': begin, 'size': size, 'output':
                   output })

# show given blocks table
for block in blocks:
    print(block['name'], end=' ')
    print('0x{:08x}'.format(block['begin']), end=' ')
    print('0x{:08x}'.format(block['size']), end=' ')
    print(block['output'], end='\n')

#b =  int('0x00800000', 16)
a = '0xadf'
try:
    b = int(a)
except ValueError:
    b = int(a, 16)
print(hex(b))

print('Hello, World!')


