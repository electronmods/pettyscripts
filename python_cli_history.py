#!/usr/bin/env python3

# One-liner with a limit on most recent entries
import readline; mostrecent=20; histsize=readline.get_current_history_length(); print('\n'.join([str(readline.get_history_item(i + 1)) for i in range(histsize-mostrecent, histsize)]))

# Everything, and not one line
import readline
for i in range(readline.get_current_history_length()):
    print (readline.get_history_item(i + 1))
