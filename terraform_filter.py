#!/usr/bin/env python3
#
# Copyright 2019 RADAR, Inc. - All Rights Reserved
# Proprietary and confidential

import argparse
import sys
import re

def filter_terraform_output(tf_output, keys):
    output = tf_output
    for key in keys:
        reg = r"%s.*" % key
        matches = re.finditer(reg, output, re.IGNORECASE)
        for match in matches:
            start, end = match.span()            
            equals_index = output.find("= ", start, end)
            secret = "*" * (end - equals_index - 2)
            output = output[:equals_index+2]  + secret  + output[end:]
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tf_output', nargs='?', type=argparse.FileType('r'),  default=sys.stdin)
    parser.add_argument('sensitive_keys_input', type=argparse.FileType('r'))
    args = parser.parse_args()    
    
    tf_output = args.tf_output.read()
    args.tf_output.close()
    
    keys = [k.strip() for k in args.sensitive_keys_input.readlines()]
    args.sensitive_keys_input.close()

    print(filter_terraform_output(tf_output, keys))
    
