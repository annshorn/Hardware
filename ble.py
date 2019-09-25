#!/usr/bin/env python

################################################################################
# COPYRIGHT(c) 2018 STMicroelectronics                                         #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#   1. Redistributions of source code must retain the above copyright notice,  #
#      this list of conditions and the following disclaimer.                   #
#   2. Redistributions in binary form must reproduce the above copyright       #
#      notice, this list of conditions and the following disclaimer in the     #
#      documentation and/or other materials provided with the distribution.    #
#   3. Neither the name of STMicroelectronics nor the names of its             #
#      contributors may be used to endorse or promote products derived from    #
#      this software without specific prior written permission.                #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE    #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                                  #
################################################################################

################################################################################
# Author:  Davide Aliprandi, STMicroelectronics                                #
################################################################################


# DESCRIPTION
#
# This application example shows how to perform a Bluetooth Low Energy (BLE)
# scan, connect to a number of devices handled though dedicated threads, and get
# push notifications from all their features.


# IMPORT

from __future__ import print_function
import sys
import os
import time
from time import gmtime, strftime
import datetime
import threading
from abc import abstractmethod
import csv
import pandas as pd

from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener
from blue_st_sdk.feature import FeatureListener
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm import FeatureAudioADPCM
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm_sync import FeatureAudioADPCMSync


# PRECONDITIONS
#
# In case you want to modify the SDK, clone the repository and add the location
# of the "BlueSTSDK_Python" folder to the "PYTHONPATH" environment variable.
#
# On Linux:
#   export PYTHONPATH=/home/<user>/BlueSTSDK_Python


# CONSTANTS

# Presentation message.
INTRO = """##################
# BlueST Example #
##################"""

# Bluetooth Scanning time in seconds (optional).
SCANNING_TIME_s = 5

name = input()
name2 = input()
newpath = ((r'/home/pi/Desktop/Folder/' + name))
if not os.path.exists(newpath): os.makedirs(newpath)

file_name = name + ".csv"
file_ = open(newpath +'/' + file_name, "w")
writer = csv.writer(file_, delimiter = ",")

file_name2 = name2 + ".csv"
file_2 = open(newpath +'/' + file_name2, "w")
writer2 = csv.writer(file_2, delimiter = ",")

#df = pd.DataFrame(columns = ['1', '2'])
#df.to_csv(newpath + file_name, header = True)


array1 = []
array2 = []



# FUNCTIONS

#
# Printing intro.
#
def print_intro():
    print('\n' + INTRO + '\n')


# INTERFACES

#
# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
#
class MyManagerListener(ManagerListener):

    #
    # This method is called whenever a discovery process starts or stops.
    #
    # @param manager Manager instance that starts/stops the process.
    # @param enabled True if a new discovery starts, False otherwise.
    #
    def on_discovery_change(self, manager, enabled):
        print('Discovery %s.' % ('started' if enabled else 'stopped'))
        if not enabled:
            print()

    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
        print('New device discovered: %s.' % (node.get_name()))


#
# Implementation of the interface used by the Node class to notify that a node
# has updated its status.
#
class MyNodeListener(NodeListener):

    #
    # To be called whenever a node connects to a host.
    #
    # @param node Node that has connected to a host.
    #
    def on_connect(self, node):
        print('Device %s connected.' % (node.get_name()))

    #
    # To be called whenever a node disconnects from a host.
    #
    # @param node       Node that has disconnected from a host.
    # @param unexpected True if the disconnection is unexpected, False otherwise
    #                   (called by the user).
    #
    def on_disconnect(self, node, unexpected=False):
        print('Device %s disconnected%s.' % \
            (node.get_name(), ' unexpectedly' if unexpected else ''))


#
# Implementation of the interface used by the Feature class to notify that a
# feature has updated its data.
#
class MyFeatureListener(FeatureListener):

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        #print('[%s %s]' % (feature.get_parent_node().get_name(), \
            #feature.get_parent_node().get_tag()))
        data_acc = [0,0,0]
        data_gyr = [0,0,0]
        data_mag = [0,0,0]
        if feature._name == 'Accelerometer':
            data_acc[0] = feature._last_sample._data[0]
            data_acc[1] = feature._last_sample._data[1]
            data_acc[2] = feature._last_sample._data[2]
        if feature._name == 'Gyroscope':
            data_gyr[0] = feature._last_sample._data[0]
            data_gyr[1] = feature._last_sample._data[1]
            data_gyr[2] = feature._last_sample._data[2]
        if feature._name == 'Magnetometer':
            data_mag[0] = feature._last_sample._data[0]
            data_mag[1] = feature._last_sample._data[1]
            data_mag[2] = feature._last_sample._data[2]
        #init_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        current = datetime.datetime.now()
        writer.writerow([str(current)[14:-3], data_acc,data_gyr,data_mag ])
        #array1.append(data_acc+data_gyr+data_mag )
        print( str(current)[14:-3], data_acc+data_gyr+data_mag )
        
        
class MyFeatureListener2(FeatureListener):

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        #print('[%s %s]' % (feature.get_parent_node().get_name(), \
            #feature.get_parent_node().get_tag()))
        data_acc = [0,0,0]
        data_gyr = [0,0,0]
        data_mag = [0,0,0]
        if feature._name == 'Accelerometer':
            data_acc[0] = feature._last_sample._data[0]
            data_acc[1] = feature._last_sample._data[1]
            data_acc[2] = feature._last_sample._data[2]
        if feature._name == 'Gyroscope':
            data_gyr[0] = feature._last_sample._data[0]
            data_gyr[1] = feature._last_sample._data[1]
            data_gyr[2] = feature._last_sample._data[2]
        if feature._name == 'Magnetometer':
            data_mag[0] = feature._last_sample._data[0]
            data_mag[1] = feature._last_sample._data[1]
            data_mag[2] = feature._last_sample._data[2]
        #writer.writerow([data_acc+data_gyr+data_mag ])
        #array2.append(data_acc+data_gyr+data_mag )
        #init_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        current = datetime.datetime.now()
        writer2.writerow([str(current)[14:-3],data_acc,data_gyr,data_mag ])
        print( '||||||||||||',str(current)[14:-3],'|||||||', data_acc+data_gyr+data_mag, '||||||||||||' )


class DeviceThread(threading.Thread):
    """Class to handle a device in a thread."""

    def __init__(self, device, *args, **kwargs):
        """Constructor.

        Args:
            device (:class:`blue_st_sdk.node.Node`): The device to handle.
        """
        super(DeviceThread, self).__init__(*args, **kwargs)
        self._device = device

    def run(self):
        """Run the thread."""

        # Connecting to the device.
        self._device.add_listener(MyNodeListener())
        print('Connecting to %s...' % (self._device.get_name()))
        if not self._device.connect():
            print('Connection failed.\n')
            return

        # Getting features.
        features = self._device.get_features()

        # Enabling notifications.
        for feature in features:
            # For simplicity let's skip audio features.
            if not isinstance(feature, FeatureAudioADPCM) and \
                not isinstance(feature, FeatureAudioADPCMSync):
                feature.add_listener(MyFeatureListener())
                self._device.enable_notifications(feature)

        # Getting notifications.
        while True:
            if self._device.wait_for_notifications(0.005):
                pass

    def get_device(self):
        """Get the handled device."""
        return self._device
        
        
class DeviceThread2(threading.Thread):
    """Class to handle a device in a thread."""

    def __init__(self, device, *args, **kwargs):
        """Constructor.

        Args:
            device (:class:`blue_st_sdk.node.Node`): The device to handle.
        """
        super(DeviceThread2, self).__init__(*args, **kwargs)
        self._device = device

    def run(self):
        """Run the thread."""

        # Connecting to the device.
        self._device.add_listener(MyNodeListener())
        print('Connecting to %s...' % (self._device.get_name()))
        if not self._device.connect():
            print('Connection failed.\n')
            return

        # Getting features.
        features = self._device.get_features()

        # Enabling notifications.
        for feature in features:
            # For simplicity let's skip audio features.
            if not isinstance(feature, FeatureAudioADPCM) and \
                not isinstance(feature, FeatureAudioADPCMSync):
                feature.add_listener(MyFeatureListener2())
                self._device.enable_notifications(feature)

        # Getting notifications.
        while True:
            if self._device.wait_for_notifications(0.005):
                pass

    def get_device(self):
        """Get the handled device."""
        return self._device


# MAIN APPLICATION

#
# Main application.
#
def main(argv):

    # Printing intro.
    #print_intro()
    MAC = 'c0:86:4b:31:28:48'
    MAC2 = 'c0:86:4e:30:49:4d'
    n = 0

    try:
        # Creating Bluetooth Manager.
        manager = Manager.instance()
        manager_listener = MyManagerListener()
        manager.add_listener(manager_listener)

        # Synchronous discovery of Bluetooth devices.
        print('Scanning Bluetooth devices...\n')
        manager.discover(SCANNING_TIME_s)

        # Getting discovered devices.
        discovered_devices = manager.get_nodes()

        # Selecting devices to connect.
        selected_devices = []
        for device in discovered_devices:
            if device.get_tag() == MAC:
                print('Device were found')
                selected_devices.append(device)
                n+=1
            if device.get_tag() == MAC2:
                print('Device 2 were found')
                selected_devices.append(device)
                n+=1
            if n == 2:
                break
                
        device_threads = []
        device_threads.append(DeviceThread(selected_devices[0]).start())
        device_threads.append(DeviceThread2(selected_devices[1]).start())

        #DeviceThread(selected_devices[0])
        #DeviceThread2(selected_devices[1])
        # Getting notifications.
        while True:
            pass

    except KeyboardInterrupt:
        try:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":

    main(sys.argv[1:])
