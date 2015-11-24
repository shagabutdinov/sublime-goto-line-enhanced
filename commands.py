import sublime
import sublime_plugin
import re

try:
  from QuickSearchEnhanced.quick_search import panels
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
   "GotoLineEnhanced plugin for installation instructions; to disable this " +
   "message remove this plugin; message: " + str(error))
  raise error

class PromptGotoLine(sublime_plugin.TextCommand):
  def run(self, edit, start_with_current = False):
    label = 'Tab for goto; Esc for cancel'

    current = ''
    if start_with_current and len(self.view.sel()) > 0:
      current, _ = self.view.rowcol(self.view.sel()[0].a)
      current += 1

    panels.create([label], None, self._close, None, str(current),
      [['goto_line', True]], self._create).show()

    self.initial_viewport_position = self.view.viewport_position()

  def _close(self, panel):
    self.view.show(self.view.sel()[0])
    if not getattr(panel, 'success', False):
      self.view.set_viewport_position(self.initial_viewport_position)

    callback = lambda: panel.get_opener().erase_regions('goto_line_enhanced')
    sublime.set_timeout(callback, 100)

  def _create(self, panel):
    view = panel.get_panel()
    view.sel().clear()
    view.sel().add(sublime.Region(0, 0))
    view.set_overwrite_status(True)

def get_panel():
  panel = panels.get_current()
  goto_panel = panel and panel.get_caller('goto_line')
  if goto_panel == None:
    return None

  return panel

def shift(view, point):
  string = view.substr(view.line(point))
  shift_match = re.search(r'(?<!\n)(\S|$)', string)
  if shift_match != None:
    point += shift_match.start(1)

  return point

def convert_query_to_point(view, query, options = {}):
  if re.match(r'\d+', query) == None:
    return

  query = re.sub(r'\D', '', query)
  max_line, _ = view.rowcol(view.size())
  line = int(query) - 1
  if line > max_line:
    line = max_line

  point = view.text_point(line, 0)

  if 'position' in options and options['position'] == 'end':
    point = view.line(point).b
  else:
    point = shift(view, point)

  return point

def convert_query_to_region(view, query, options = {}):
  start = end = convert_query_to_point(view, query, options)

  if start == None or end == None:
    return None

  if 'select' in options and options['select']:
    start = view.sel()[0].begin()
    if 'position' not in options or options['position'] == None:
      if end > start:
        end = view.line(end).b
      else:
        end = shift(view, view.line(end).a)

  return sublime.Region(start, end)

class GotoLineComplete(sublime_plugin.TextCommand):
  def run(self, edit, position = None, select = False):
    panel = get_panel()
    if panel == None:
      return

    view, query = panel.get_opener(), panel.get_current_text()
    region = convert_query_to_region(view, query, {
      'position': position,
      'select': select,
    })

    view.sel().clear()
    view.sel().add(region)
    panel.close(None, False)
    view.show(region)
    setattr(panel, 'success', True)

class GotoLineInsertZero(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.insert(edit, 0, '0')

class GotoLineFilterQuery(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = get_panel()
    if panel == None:
      return

    view = panel.get_opener()

    all = sublime.Region(0, self.view.size())
    query = self.view.substr(all)
    new_query = self._filter_line(view, query)

    if new_query != query:
      saved_selection = self.view.sel()[0]
      self.view.replace(edit, all, new_query)

    if len(self.view.sel()) == 1:
      sel = self.view.sel()[0]
      max_line, _ = view.rowcol(view.size())
      should_goto_beginning = (sel.a == sel.b and sel.a == self.view.size() and
        sel.a == len(str(max_line)))

      if should_goto_beginning:
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(0, 0))

  def _filter_line(self, view, line):
    replace = [('n', '0'), ('m', '1'), (',', '2'), ('.', '3'), ('j', '4'),
      ('k', '5'), ('l', '6'), ('u', '7'), ('i', '8'), ('o', '9')]

    for character, number in replace:
      line = line.replace(character, number)

    line = re.sub(r'[^\d]', '', line)
    if line == '':
      return ''

    max_line, _ = view.rowcol(view.size())
    max_line += 1 # because indexes starts with 1
    if len(line) > len(str(max_line)):
      line = line[0:len(str(max_line))]

    return line

class InputHelper(sublime_plugin.EventListener):
  def on_modified_async(self, view):
    panel = get_panel()
    if panel == None or panel.get_panel().id() != view.id():
      return

    view.run_command('goto_line_filter_query')

    view, query = panel.get_opener(), panel.get_current_text()
    region = convert_query_to_region(view, query)
    if region == None:
      return None

    region = view.full_line(region)
    view.add_regions('goto_line_enhanced', [region], 'string')
    view.show(region)