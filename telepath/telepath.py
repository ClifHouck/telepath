# -*- coding: utf-8 -*-

import argparse
import io
import os

import requests
from six.moves import configparser

CONFIG_FILENAME = os.path.expanduser("~/.telepath.cfg")


class BadConfigurationError(Exception):
    pass


def validate_configuration(config):
    if not config.has_section('telepath'):
        return (False, "No telepath section. Are you sure the configuration "
                       "file exists?")

    REQUIRED_OPTIONS = ['endpoint', 'irc_nick', 'status_filename']
    present_options = config.options('telepath')
    missing = []
    for option in REQUIRED_OPTIONS:
        if option not in present_options:
            missing.append(option)

    if len(missing) > 0:
        return (False, "The configuration is missing the following required "
                       "options: %(missing_options)s" % {
                           'missing_options': missing})

    return (True, "Good configuration.")


def get_configuration(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    is_config_good, reason = validate_configuration(config)
    if not is_config_good:
        raise BadConfigurationError(reason)

    # Do expansion on the status_filename option.
    status_filename = os.path.expanduser(
        config.get('telepath', 'status_filename'))
    config.set('telepath', 'status_filename', status_filename)

    return config


def add_completed_task(status_filename, task_body):
    with open(status_filename, 'a') as outfile:
        outfile.seek(io.SEEK_END)
        outfile.write(task_body + "\n")


def task_complete(args):
    config = get_configuration(args.config_file)

    status_file = config.get('telepath', 'status_filename')

    add_completed_task(status_file, args.task_body)

    if args.verbose:
        print(("Added completed task to " +
              config.get('telepath', 'status_filename')))


def get_completed_tasks(status_filename):
    with open(status_filename, 'r') as infile:
        return infile.read()


def clear_tasks(status_filename):
    os.remove(status_filename)


def send_report(args):
    config = get_configuration(args.config_file)
    endpoint = config.get('telepath', 'endpoint')

    completed_tasks = get_completed_tasks(
        config.get('telepath', 'status_filename'))

    form_dict = {
        'irc_nick': config.get('telepath', 'irc_nick'),
        'area': '',
        'completed': completed_tasks,
        'inprogress': '',
        'impediments': '',
    }

    if args.verbose:
        print("Posting status to " + endpoint)

    response = post_data_to_endpoint(endpoint, form_dict)

    if response.status_code == 200:
        clear_tasks(config.get('telepath', 'status_filename'))
        if args.verbose:
            print(''.join(["Cleared tasks in ",
                           config.get('telepath', 'status_filename')]))

    if args.verbose:
        print(''.join(["Returned ", str(response.status_code),
                       " status code."]))


def post_data_to_endpoint(endpoint, payload):
    response = requests.post(endpoint + '/irc', data=payload, verify=False)
    return response


def main():
    parser = argparse.ArgumentParser(
        description="Automate standup reporting.")
    parser.add_argument('-c', '--config-file', default=CONFIG_FILENAME,
                        help="The configuration file to use with telepath.")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Show more detailed information on progress.")

    subparsers = parser.add_subparsers(help='sub-command help')

    # Completed task parser.
    complete_task_parser = subparsers.add_parser('task-complete',
                                                 help='Add a completed task.')
    complete_task_parser.add_argument('task_body')
    complete_task_parser.set_defaults(func=task_complete)

    # Send report parser.
    report_send_parser = subparsers.add_parser('report',
                                               help='Send the current report.')
    report_send_parser.set_defaults(func=send_report)

    args = parser.parse_args()

    if args.verbose:
        print(''.join(["Loading configuration from ", args.config_file]))

    args.func(args)


if __name__ == "__main__":
    main()
