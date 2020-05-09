#!/usr/bin/env python3
"""
A Python script for automatically adjusting the font scaling in Gnome based on the number
of monitors.
"""
__docformat__ = 'reStructuredText'
# ***************************************************************************************
#  File Name: montextscale.py
#
# ---------------------------------------------------------------------------------------
#                           C O P Y R I G H T
# ---------------------------------------------------------------------------------------
#             Copyright (c) 2020 by Frank Voorburg   All rights reserved
#
#   This software has been carefully tested, but is not guaranteed for any particular
# purpose. The author does not offer any warranties and does not guarantee the accuracy,
#    adequacy, or completeness of the software and is not responsible for any errors or
#              omissions or the results obtained from use of the software.
# ---------------------------------------------------------------------------------------
#                             L I C E N S E
# ---------------------------------------------------------------------------------------
# This file is part of montextscale. Montextscale is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Montextscale is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program. If not, see <http://www.gnu.org/licenses/>.
#
# ***************************************************************************************

# ***************************************************************************************
#  Imports
# ***************************************************************************************
import logging
import argparse
import subprocess
import time


# ***************************************************************************************
#  Global constant declarations
# ***************************************************************************************
# Program return codes.
RESULT_OK = 0
# Font scaling factor in case multiple screen are connected.
FONT_SCALING_MULTI_SCREEN = 1.00
# Font scaling factor in case only a single screen is connected.
FONT_SCALING_SINGLE_SCREEN = 1.25


# ***************************************************************************************
#  Implementation
# ***************************************************************************************
def main():
    """
    Entry point into the program.
    """
    # Initialize the program exit code.
    result = RESULT_OK

    # Handle command line parameters.
    parser = argparse.ArgumentParser(description="A Python script for automatically " +
                                     "adjusting the font scaling in Gnome based on " + 
                                     "the number of monitors.\r\n")
    # Add optional command line parameters.
    parser.add_argument('-d', '--debug', action='store_true', dest='debug_enabled', default=False,
                        help="enable debug messages on the standard output.")
    # Perform actual command line parameter parsing.
    args = parser.parse_args()

    # Enable debug logging level if requested.
    if args.debug_enabled:
        logging.basicConfig(level=logging.DEBUG)

    # Set the lat screen count to an invalid value
    last_screen_count = -1

    # Enter the program loop.
    while True:
        # Obtain the current number of connected screens.
        current_screen_count = get_connected_screen_count()

        # Only continue if the last screen count is initialized and the number of
        # connected screens is valid
        if last_screen_count != -1 and current_screen_count > 0:
            # Detect change in screen count
            if (current_screen_count != last_screen_count):
                # Do we have multiple screens?
                if current_screen_count > 1:
                    # Set the font scaling for multiple screens
                    set_gnome_font_scaling(FONT_SCALING_MULTI_SCREEN)
                else:
                    set_gnome_font_scaling(FONT_SCALING_SINGLE_SCREEN)

        # Store screen count for the next loop iteration
        last_screen_count = current_screen_count
        # Sleep in between to not hog up the CPU.
        time.sleep(5)
    # Give the exit code back to the caller
    return result


def get_connected_screen_count():
    """
    Determines the number of screens that are currently connected.

    :returns: Number of connected screens.
    :rtype: int
    """
    result = 0

    # Assemble and execute the commands that counts the number of connected screens. The command to run is:
    # cmd = "xrandr -d :0 -q | grep ' connected' | wc - l"
    proc_xrandr = subprocess.Popen(['xrandr', '-d', ':0', '-q'], stdout=subprocess.PIPE)
    proc_grep   = subprocess.Popen(['grep', ' connected'], stdin=proc_xrandr.stdout, stdout=subprocess.PIPE)
    proc_wc     = subprocess.Popen(['wc', '-l'], stdin=proc_grep.stdout, stdout=subprocess.PIPE)
    # Wait for the last subprocess to exit and get the output.
    cmd_output = proc_wc.communicate()[0]

    # Output information for debugging purposes.
    logging.debug('xrandr pipe command returned {} with output {}'.format(proc_wc.returncode, cmd_output))
    # Process the output if the last subprocess was successful.
    if proc_wc.returncode == 0:
        try:
            result = int(cmd_output.decode('utf-8').strip())
        except:
            result = 0

    # Give the result back to the caller
    return result


def set_gnome_font_scaling(font_scaling):
    """
    Changes the font scaling configuration of the Gnome desktop environment.
    """

    # Assemble and execute the command for changing the font scaling.
    subprocess.Popen(['gsettings', 'set', 'org.gnome.desktop.interface', 'text-scaling-factor', '{}'.format(font_scaling)])


if __name__ == '__main__':
    exit(main())


# ********************************* end of montextscale.py ******************************
