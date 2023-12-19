from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.environment_parameters_channel import (
    EnvironmentParametersChannel
)
from mlagents_envs.side_channel.engine_configuration_channel import (
    EngineConfigurationChannel
)
import yaml
from yaml.loader import SafeLoader
import os
from sys import platform


class Nenv:
    """A NEVE environment to control a unity environment.

    A user-friendly wrapper around the UnityEnvironment class.
    """

    def __init__(self, params):
        """Initialize the NEVE environment.

        Args:
            params (str): The path to the configuration file with parameters of the Unity
            stimulus/environment.
        """

        if not os.path.exists(params):
            raise Exception('Could not find the configuration file')

        with open(params, 'r') as f:
            self.params = yaml.load(f, Loader=SafeLoader)

        # Create the side channels to communicate with unity
        self.env_parameters = EnvironmentParametersChannel()
        self.eng_config = EngineConfigurationChannel()

        print('Waiting for connection to Unity environment...')
        print('When Unity launches, python will gain control.')
	
        file_name = self._get_built_file_path()
        self.env = UnityEnvironment(
            file_name=file_name,
            side_channels=[self.env_parameters, self.eng_config],
            timeout_wait=999999,
            worker_id=0 if file_name is None else self._get_worker_id()
        )
        self.execution_order = self.params['execution_order']
        self.params.pop('execution_order')

    def set_params(self, i):
        """Sets the parameters for the experimental trial

        Any change using set_params requires a reset (self.reset()).

        Args:
            i (int): The index of the trial.
        """

        # Any change to a Unity SideChannel (self.env_parameters) will
        # only be effective after a step or reset
        # so self.reset() will need to be called to apply the changes.
        print('Setting new environmental parameters...')
        for key, value in self.params.items():
            print('Setting', key, '...')

            if type(value) != list:
                self.env_parameters.set_float_parameter(key, value)
            elif len(value) == 1:
                self.env_parameters.set_float_parameter(key, value[0])
            else:
                self.env_parameters.set_float_parameter(key, value[i])
                assert len(value) == len(self.execution_order), (
                    f'the length of {key} must be one or the same as the'
                    'length of execution_order'
                )
    
    def reset(self):
        """Resets the environment

        Should be called after self.set_params().
        """
        print('Resetting environment/Starting experiment...')
        print(
            'Press EXIT to end the Unity experiment prematurely.'
            ' Press ALT-TAB to access python.'
        )
        self.env.reset()

    def close(self):
        """Ends and closes the environment"""
        print('All experiments completed. Closing unity and exiting...')
        self.env.close()

    def _get_built_file_path(self):
        """Returns the path to the built Unity executable"""
        file_name = None
        if str(self.params['buildDir']).lower() not in (
                '', 'none', 'null', 'na', 'nan'
        ):
            build_dir = self.params['buildDir']

            if not os.path.exists(build_dir):
                build_dir = os.path.join(os.path.dirname(__file__), '..',
                        self.params['buildDir'])
                if not os.path.exists(build_dir):
                    build_dir = os.path.join(os.path.dirname(__file__), '..',
                            '..', self.params['buildDir'])

                    if not os.path.isdir(build_dir):
                        # running as a mac app and need to go up 5 or 6 levels
                        build_dir = os.path.join(
                            os.path.dirname(__file__),
                            '..', '..', '..', '..', self.params['buildDir']
                        )
                        if not os.path.isdir(build_dir):
                            build_dir = os.path.join(os.path.dirname(__file__),
                              '..', '..', '..', '..', '..', self.params['buildDir'])
                            raise FileNotFoundError(
                                f'Could not find build file at {build_dir}'
                                'Please check the buildDir parameter in the config file.'
                            )

            if platform in ['win32', 'cygwin']:
                file_name = os.path.join(
                    build_dir,
                    'Windows/NEVE_unity_urp.exe'
                )
            elif platform in ['darwin']:
                file_name = os.path.join(build_dir, 'Mac.app')
            elif platform in ['linux', 'linux2']:
                file_name = os.path.join(build_dir, 'Linux/Linux.x86_64')
            else:
                raise Exception(
                    f'Build file for platform {platform} has not been made.'
                )
        else:
            print(
                'No buildDir provided. Assuming you are'
                ' running your experiment in Unity for development.'
                ' Press play in the Unity Editor to start.'
            )

        # now remove buildDir from params, as we should not send it to unity
        self.params.pop('buildDir')

        return file_name

    def _get_worker_id(self, filename=".worker_id.dat"):
        """ Workaround for ml-agents socket connection communicator problem

        This changes the worker id if there is one left over from a old unity environment
        that didn't close its socket connection correctly.

        See https://github.com/Unity-Technologies/ml-agents/issues/1505
        """
        
        with open(filename, 'a+') as f:
            f.seek(0)
            val = int(f.read() or 0) + 1
            f.seek(0)
            f.truncate()
            f.write(str(val))
            return val

