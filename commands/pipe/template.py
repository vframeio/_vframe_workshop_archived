############################################################################# 
#
# VFRAME
# MIT License
# Copyright (c) 2020 Adam Harvey and VFRAME
# https://vframe.io 
#
#############################################################################


import click

from vframe.utils.click_utils import processor

@click.command('')
@processor
@click.pass_context
def cli(ctx, pipe):
  """\033[97mTemplate\033[00m"""
  
  from vframe.settings import app_cfg

  
  # ---------------------------------------------------------------------------
  # initialize

  log = app_cfg.LOG
  log.debug('This is a template file')


  # ---------------------------------------------------------------------------
  # Example: process images as they move through pipe

  while True:

    pipe_item = yield
    pipe.send(pipe_item)


  # ---------------------------------------------------------------------------
  # Example: accumulate all pipe items
  
  # while True:
  #   try:
  #     pipe_items.append( (yield) )
  #   except GeneratorExit as e:
  #     log.debug('Done accumulating pipe items')
  #     break
  
  # rebuild the generator
  # for pipe_item in pipe_items:
  #   pipe.send(pipe_item)


  # def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
  # def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
  # def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
  # def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
  # def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
  # def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
  # def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
  # def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))
  