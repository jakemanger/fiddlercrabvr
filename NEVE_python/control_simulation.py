from neve.env import Nenv
import argparse
from gooey import Gooey, GooeyParser
import os
import sys


# for nuitka exe
target = None
if "__compiled__" in globals():
    target = sys.argv[0]


def start(config_path):
    """ Main function for looping through all experimental conditions

    Experimental conditions are specified by the `config_path` argument
    """
    nenv = Nenv(params=config_path)

    print('Running for', len(nenv.execution_order), 'experimental conditions')
    for i in nenv.execution_order:
        nenv.set_params(i)
        nenv.reset()

    nenv.close()


@Gooey(target=target, program_name='NEVE stimulus controller', use_cmd_args=True)
def main():
    parser = GooeyParser(
        description='''
        Start Unity and loop through all stimuli specified by a
        configuration file at `config_path`.
        '''
    )

    # find possible config files in the configs/ directory
    configs_dir = os.path.join(os.path.dirname(__file__), 'configs')

    if not os.path.isdir(configs_dir):
        configs_dir = os.path.join(os.path.dirname(__file__), '..', 'configs')

        if not os.path.isdir(configs_dir):
            # running as a mac app and need to go up 4 or 5 levels
            configs_dir = os.path.join(
                os.path.dirname(__file__),
                '..', '..', '..', 'configs'
            )
            if not os.path.isdir(configs_dir):
                configs_dir = os.path.join(os.path.dirname(__file__),
                  '..', '..', '..', '..', 'configs')
                raise FileNotFoundError(
                    f'Could not find configs directory at {configs_dir}'
                )

    if os.path.exists(configs_dir):
        config_files = [f for f in os.listdir(configs_dir)]
    else:
        raise Exception(
            f'Could not find the configs directory in {configs_dir}.'
            f'The current working directory is {os.getcwd()}.'
            ' Store your config files in the configs/ directory'
        )

    parser.add_argument(
        'config_path',
        type=str,
        help='''
        Select your stimulus configuration file.
        ''',
        choices=config_files
    )
    args = parser.parse_args()

    start(os.path.join(configs_dir, args.config_path))

if __name__ == '__main__':
    main()
