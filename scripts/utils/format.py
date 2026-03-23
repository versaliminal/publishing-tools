from termcolor import colored


def print_header(text):
    print(colored("\n{0}\n{1}".format(text, '-' * len(text)), 'magenta'))


def print_subheader(text, indent=0):
    print(colored("{0}# ".format("  " * indent * 2), 'magenta') + text)


def print_item_success(text, indent=0):
    print(colored("{0}* ".format("  " * indent * 2), 'green') + text)


def print_item_failure(text, indent=0):
    print(colored("{0}! ".format("  " * indent * 2), 'red') + text)


def print_item_notice(text, indent=0):
    print(colored("{0}? ".format("  " * indent * 2), 'yellow') + text)
