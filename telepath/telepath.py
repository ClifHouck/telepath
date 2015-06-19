# -*- coding: utf-8 -*-

# TODO(ClifHouck) Load options through a configuration file.
# - standup endpoint
# - irc nick
# - functional area?
# - file to store task/wot/impediments in?
# TODO(ClifHouck) Support command-line addition of a completed task.
# TODO(ClifHouck) Send completed task to standup endpoint.
# TODO(ClifHouck) be able to generate a crontab entry to send status, on a
# weekday, at a specified time

from six.moves import configparser

config_filename = "telepath.cfg"


class BadConfigurationError(Exception):
    pass


def validate_configuration(config):
    return (True, "Good configuration.")


def get_configuration(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    is_config_good, reason = validate_configuration(config)
    if not is_config_good:
        raise BadConfigurationError(reason)
    return config

if __name__ == "__main__":
    config = get_configuration(config_filename)
