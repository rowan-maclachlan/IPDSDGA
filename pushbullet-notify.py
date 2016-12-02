#!/usr/bin/env python3

"""
Pushbullet Notify
"""

from urllib import request
import json

def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-a', '--token', type=str, required=True)

    targets = parser.add_mutually_exclusive_group(required=True)
    targets.add_argument('-e', '--email', type=str)
    targets.add_argument('-d', '--device', type=str)
    targets.add_argument('-c', '--channel', type=str)

    parser.add_argument('-t', '--title', type=str)

    parser.add_argument('string', nargs='+')

    return parser.parse_args()


if __name__ == '__main__':
    from os import path
    import sys

    args = get_arguments()

    note = {
        'type': 'note',
        'body': ' '.join(args.string)
    }

    if args.title:
        note['title'] = args.title

    if args.email:
        note['email'] = args.email

    if args.device:
        note['device_iden'] = args.device

    if args.channel:
        note['channel_tag'] = args.channel

    request.urlopen(request.Request(
        'https://api.pushbullet.com/v2/pushes',
        json.dumps(note).encode('utf-8'),
        {   'Access-Token': args.token,
            'Content-Type': 'application/json'
        })
    )
