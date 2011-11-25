#!/usr/bin/python2.6
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
import os
import numpy
from PIL import Image
from pnm import pnm_header
from phase import find_phase
from detect import detect_stripes
from split import insert_pagefeed

def interpolate(channels, scanline, scanline_2, phase, phase_2, target):
  """Alpha blend two scanlines. Takes two scanlines and their phases, and
  returns an interpolated scanline with the phase where we want it."""
  if phase == phase_2:
    alpha = 1
  else:
    alpha = (target - phase) / (phase_2 - phase)
  s1 = numpy.frombuffer(scanline, dtype=numpy.uint8)
  s2 = numpy.frombuffer(scanline_2, dtype=numpy.uint8)
  f = numpy.asfarray(s2) * alpha + numpy.asfarray(s1) * (1 - alpha)
  return numpy.asarray(f, dtype=numpy.uint8).tostring()

def has_wrapped(prev_phase, phase, period):
  """Has the phase wrapped around?"""
  if prev_phase - phase > period * 0.7:
    return True
  else:
    return False

def straighten(prev_scanline, channels, instream, outstream):
  """Straighten an entire book page"""
  linesize = len(prev_scanline)
  w = linesize // channels
  prev_phase, period = find_phase(prev_scanline, channels)
  scanline = instream.read(linesize)
  if len(scanline) != linesize:
    return False
  phase, period = find_phase(scanline, channels)
  target = prev_phase
  n = 0
  while detect_stripes(scanline, channels):
    if has_wrapped(prev_phase, phase, period):
      target -= period
      prev_phase -= period
    if phase < target:
      prev_phase, prev_scanline = phase, scanline
      scanline = instream.read(linesize)
      if len(scanline) != linesize:
        return False
      phase, period = find_phase(scanline, channels)
    elif prev_phase > target:
      target += 1
    else:
      line = interpolate(channels, prev_scanline, scanline,
                         prev_phase, phase, target)
      outstream.write(line)
      outstream.flush()
      n += 1
      target += 1
  if n == 0:
    return
  insert_pagefeed(linesize)

def process(instream, outstream):
  """Dewobble the entire image."""
  linewidth, linecount, channels = pnm_header()
  linesize = linewidth * channels
  while True:
    scanline = instream.read(linesize)
    if len(scanline) != linesize:
      break
    if detect_stripes(scanline, channels):
      straighten(scanline, channels, instream, outstream)

if __name__ == "__main__":
  process(sys.stdin, sys.stdout)