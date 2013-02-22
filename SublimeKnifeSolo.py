import sublime, sublime_plugin, subprocess, threading, Queue, time, os
from helper import AsynchronousFileReader, SublimeMessageManager

# for debug. Is there a better way to reload the external module ?
# import helper
# reload(helper)

class KnifeSolo(sublime_plugin.WindowCommand):

  def run(self):
    self.show_list()

  def show_list(self):
    window = sublime.active_window()
    self.settings = sublime.load_settings("SublimeKnifeSolo.sublime-settings")
    parameters = self.settings.get("parameters", [])

    self.items = []
    for p in parameters:
      command = "%s@%s" % (p["user"], p["host"])
      if "identity" in p: command = command + " -i " + p["identity"]
      if "port" in p:     command = command + " -p " + p["port"]
      if "password"in p:  command = command + " -P " + p["password"]
      self.items.append(command)

    window.show_quick_panel(self.items, self.panel_done,
        sublime.MONOSPACE_FONT)

  def panel_done(self, picked):
    if 0 > picked < len(self.results):
      return

    view = self.window.active_view()
    viewDir = os.path.split(view.file_name())[0]
    soloDir = findSoloFile(viewDir)
    if soloDir is None:
      errMassageManager = SublimeMessageManager(self.window, self.command())
      errMassageManager.showPanel()
      errMassageManager.write("ERROR: solo.rb is not found.")
      return

    # working dir
    cwd = soloDir

    # generate command
    knifePath = self.settings.get("path", "")
    command = knifePath + self.command() + self.items[picked]
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=True)

    self.messageManager = SublimeMessageManager(self.window, self.command())
    self.messageManager.showPanel()
    thread = threading.Thread(target=runKnife, args=(p, self.messageManager))
    thread.start()

    # http://docs.python.org/2/library/threading.html#threading.Thread.daemon
    # The entire Python program exits when no alive non-daemon threads are left.

  def command(self):
    pass

class KnifeSoloPrepareCommand(KnifeSolo):
  def command(self):
    return "knife solo prepare "

class KnifeSoloCookCommand(KnifeSolo):
  def command(self):
    return "knife solo cook "

def findSoloFile(dir_name):
  while dir_name != "/":
    soloFile = os.path.join(dir_name, "solo.rb")
    if os.path.isfile(soloFile):
      return dir_name
    dir_name = os.path.dirname(dir_name)
  return None

def runKnife(process, messageManager):
  # Launch the asynchronous readers of the process' stdout and stderr.
  stdout_queue = Queue.Queue()
  stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue, .1)
  stdout_reader.start()
  stderr_queue = Queue.Queue()
  stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue, .1)
  stderr_reader.start()

  while not stdout_reader.eof() or not stderr_reader.eof():
    while not stdout_queue.empty():
      sublime.set_timeout(lambda:messageManager.write(stdout_queue.get()), 0)
      time.sleep(.1)
    while not stderr_queue.empty():
      sublime.set_timeout(lambda:messageManager.write(stderr_queue.get()), 0)
      time.sleep(.1)

  stdout_reader.join()
  stderr_reader.join()

  process.stdout.close()
  process.stderr.close()
  sublime.set_timeout(lambda:messageManager.write(u"\n\n\n\n\nFINISH!!!"), 0)

def getEncoding(str):
  for encoding in ['utf-8', 'shift-jis', 'euc-jp']:
    try:
      str.decode(encoding)
      return encoding
    except:
      pass
  return None
