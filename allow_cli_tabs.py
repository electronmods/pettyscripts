#!/usr/bin/env python3

# Allows keyboard/paste tabs into strings without Python either auto-completing
# or removing them.

import readline  
readline.parse_and_bind("set disable-completion on")  
readline.parse_and_bind("tab: self-insert")
