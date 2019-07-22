#!/usr/bin/env python3
#
# Copyright 2019 RADAR, Inc. - All Rights Reserved
# Proprietary and confidential

import argparse
import sys
import re

def filter_terraform_output(tf_output, keys):
    renewal_string = "------------------------------------------------------------------------"

    output = tf_output

    r_index = output.find(renewal_string)
    # remove everything above and including the renewal string
    # this also removes the newline
    output = output[r_index + len(renewal_string) + 2:]

    r_index = output.rfind(renewal_string)
    # remove everything after and including the final renewal string
    # this also removes the newline
    output = output[:r_index - 2]
    
    for key in keys:
        reg = r"%s.*" % key
        matches = re.finditer(reg, output, re.IGNORECASE)
        for match in matches:
            start, end = match.span()            
            equals_index = output.find("= ", start, end)
            if equals_index > 0:
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
    
