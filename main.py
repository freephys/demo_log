import sys
import functools
import time
from collections import defaultdict
import os
from datetime import datetime
class StackTrace(object):
  def __init__(self, with_call=True, with_return=False,
                     with_exception=False, max_depth=-1):
      self._frame_dict = {}
      self._options = set()
      self._max_depth = max_depth
      self.func_time = defaultdict(float)
      self.func_time_max = 0
      self.call_stack_timer = []
      self.ret = []
      self.logger = '/content/drive' + datetime.now().strftime("%Y_%m_%d")+".log"
      if with_call: self._options.add('call')
      if with_return: self._options.add('return')
      if with_exception: self._options.add('exception')

  def __call__(self, frame, event, arg):
      #ret = []
      if event == 'call':
          back_frame = frame.f_back
          start = time.time()
          if back_frame in self._frame_dict:
              self._frame_dict[frame] = self._frame_dict[back_frame] + 1
          else:
              self._frame_dict[frame] = 0
          self.call_stack_timer.append(time.time())

      depth = self._frame_dict[frame]

      if event in self._options\
        and (self._max_depth<0\
             or depth <= self._max_depth):
          self.ret.append(frame.f_code.co_name)
          self.ret.append('[%s]'%event)
          if event == 'return':
             if self.call_stack_timer:
                  start_time = self.call_stack_timer.pop(-1)
             else:
                  start_time = None
             if start_time:
                  call_time = time.time() - start_time
                  #print(start_time,time.time(),call_time)
                  #self.func_time[full_name] += call_time
                  if call_time != None:
                      self.ret.append(str(arg or "") + " " +str(call_time) + " seconds")
             else:
                  self.ret.append(arg)
          elif event == 'exception':
              self.ret.append(repr(arg[0]))
          self.ret.append('in %s line:%s'%(frame.f_code.co_filename, frame.f_lineno))
      if self.ret:
          print("%s%s"%('  '*depth, '\t'.join([str(i) for i in self.ret])))
          #self.logger.info("%s%s"%('  '*depth, '\t'.join([str(i) for i in ret])))
          #with open(self.logger, 'a') as fp:
          #    fp.write("%s%s"%('  '*depth, '\t'.join([str(i) for i in ret])))
      return self

def stack_trace(**kw):
  def entangle(func):
      @functools.wraps(func)
      def wrapper(*args, **kwargs):
          st = StackTrace(**kw)
          sys.settrace(st)
          try:
              return func(*args, **kwargs)
          finally:
              sys.settrace(None)
              print(st.logger)
              with open('/content/drive.log', 'w') as fp:
                fp.write("%s"%('\t'.join([str(i) for i in st.ret])))
              #print("%s%s"%('  ', '\t'.join([str(i) for i in st.ret])))
      return wrapper
  return entangle
