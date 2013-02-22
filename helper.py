import sublime, threading, Queue, time

# I was referring to this. Thank you
# http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading
class AsynchronousFileReader(threading.Thread):
  def __init__(self, fd, queue, sleepTime=0):
    assert isinstance(queue, Queue.Queue)
    assert callable(fd.readline)
    threading.Thread.__init__(self)
    self._fd = fd
    self._queue = queue
    self._sleepTime = sleepTime

  def run(self):
    '''The body of the tread: read lines and put them on the queue.'''
    for line in iter(self._fd.readline, ''):
      self._queue.put(line)
      time.sleep(self._sleepTime)

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

    edit = self.view.begin_edit()
    self.view.erase(edit, sublime.Region(0, self.view.size()))
    self.view.end_edit(edit)
    self.view.show(self.view.size())

    self.window.run_command('show_panel', {'panel': 'output.' + self.panelName})

  def write(self, text):
    self.view.set_read_only(False)
    edit = self.view.begin_edit()
    self.view.insert(edit, self.view.size(), text)
    self.view.end_edit(edit)
    self.view.set_read_only(True)

    self.scroll()

  def scroll(self):
    (cur_row, _) = self.view.rowcol(self.view.size())
    self.view.show(self.view.text_point(cur_row, 0))