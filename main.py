#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import stat

from subprocess import call


PATH = os.path.dirname(os.path.realpath(__file__))
PASS_HOME = '/home/kevin/Develop/ProtocolEx/cmake-build-debug'

PASS = {
    'sys-call-counter': PASS_HOME + '/lib/SysLibCounter/libSysLibCounterPass.so',
    'global-identify-struct': PASS_HOME + '/lib/Global-Structure/libGlobalSTPass.so'
}

PARAMS = {
    'sys-call-counter': '-Count-System-Call',
    'global-identify-struct': '-global-identify-struct'
}


def count():
    all_bc_full_path = []
    paths = []
    file_dirnames = []
    new_file_names = []
    for dirname, dirnames, filenames in os.walk('.'):
        # print path to all filenames.
        for filename in filenames:
            if filename.endswith('.bc'):
                file_dirnames.append(dirname[2:])

                all_bc_full_path.append(
                    os.path.join(PATH, os.path.join(dirname[2:], filename)))

                paths.append(os.path.join(os.path.join(PATH), dirname[2:]))

    for index, _path in enumerate(all_bc_full_path):
        for _pass in PASS:
            new_file_name = os.path.join(
                paths[index], file_dirnames[index] + '-' + _pass + '.txt')
            new_file_names.append(new_file_name)

            call_command = ''.join(['opt', ' -load ', PASS[_pass], ' ',
                                    PARAMS[_pass], ' -strFileName ',
                                    new_file_name, ' ', _path, ' > /dev/null'])

            with open('test.sh', 'w') as run_script:
                run_script.writelines(call_command)
                st = os.stat('test.sh')
                os.chmod('test.sh', st.st_mode | stat.S_IEXEC)

            call(['/bin/bash', 'test.sh'])

    # delete temp test.sh
    os.remove('test.sh')

    statistics(set(new_file_names))

    print('Done!')


def clean():
    for dirname, dirnames, filenames in os.walk('.'):
        # print path to all filenames.
        for filename in filenames:
            if filename.endswith('.txt'):
                os.remove(
                    os.path.join(PATH, os.path.join(dirname[2:], filename)))
    print('Clean all txt file!')


def statistics(file_names):
    for _f in file_names:
        with open(_f) as st:
            lines = st.readlines()
            print("file name {0}, the number is {1}".format(_f, len(set(lines))))


def main():
    clean()
    count()
    # clean()


if __name__ == '__main__':
    main()
