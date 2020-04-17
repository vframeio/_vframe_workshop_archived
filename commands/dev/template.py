############################################################################# 
#
# VFRAME
# MIT License
# Copyright (c) 2020 Adam Harvey and VFRAME
# https://vframe.io 
#
#############################################################################

import click

@click.command('template')
@click.pass_context
def cli(ctx):
  """_template_"""

  # ------------------------------------------------
  # imports

  from os.path import join

  from vframe.settings import app_cfg

  # ------------------------------------------------
  # start

  log = app_cfg.LOG

  log.debug('This is a template file')