#!/usr/bin/env python3

import readline; print('\n'.join([str(readline.get_history_item(i + 1)) for i in range(readline.get_current_history_length())]))

import readline
for i in range(readline.get_current_history_length()):
    print (readline.get_history_item(i + 1))
