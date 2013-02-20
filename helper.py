import sublime, threading, Queue

# I was referring to this. Thank you
# http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading
class AsynchronousFileReader(threading.Thread):
  def __init__(self, fd, queue):
    assert isinstance(queue, Queue.Queue)
    assert callable(fd.readline)
    threading.Thread.__init__(self)
    self._fd = fd
    self._queue = queue

  def run(self):
    '''The body of the tread: read lines and put them on the queue.'''
    for line in iter(self._fd.readline, ''):
      self._queue.put(line)

  def eof(self):
    '''Check whether there is no more content to expect.'''
    return not self.is_alive() and self._queue.empty()

class SublimeMessageManager():

  def __init__(self, window, panelName):
    self.window = window
    self.panelName = panelName
    self.view = None

  def showPanel(self):
    self.view = self.window.get_output_panel(self.panelName)
    self.view.set_read_only(False)

    self.view.set_read_only(False)
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(0))
    self.view.set_read_only(True)

    self.window.run_command('show_panel', {'panel': 'output.' + self.panelName})

  def write(self, text):
    if self.view is not None:
      self.view.set_read_only(False)
      edit = self.view.begin_edit()
      self.view.insert(edit, self.view.size(), text)
      self.view.end_edit(edit)
      self.view.set_read_only(True)
