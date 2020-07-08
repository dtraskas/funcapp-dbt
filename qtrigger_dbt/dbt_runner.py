import os
import re
import logging
from subprocess import PIPE, Popen

class DBTRunner():

    def __init__(self):
        # set up the current directory so that the DBT models can be accessed
        curr_dir = os.path.basename(os.path.normpath(os.getcwd()))
        self.logger = logging.getLogger(__name__)
        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        if curr_dir != "jaffle_shop":
            self.logger.info("Changing to dbt project directory")
            os.chdir("jaffle_shop")

    def go(self, model=None, tag=None, vars=None):
        
        if self.is_valid(tag):
            self.exec_dbt(['--warn-error', 'run', '--model', 'tag:' + tag])
            return

        if self.is_valid(model):
            self.exec_dbt(['--warn-error', 'run', '--model', model])
            return

        raise IOError('No valid tag or model was provided.')

    def exec_dbt(self, args=None):
        if args is None:
            args = ["run"]

        final_args = ['dbt']
        final_args.append('--single-threaded')
        final_args.extend(args)
        final_args.extend(['--profiles-dir', "../."])

        with Popen(final_args, stdout=PIPE) as proc:
            for line in proc.stdout:
                line = line.decode('utf-8').replace('\n', '').strip()
                line = self.ansi_escape.sub('', line)        
                self.logger.info(line)
                
    def is_valid(self, text):
        return text is not None and len(text) > 0