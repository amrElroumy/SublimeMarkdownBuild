import sublime
import sublime_plugin
import os
import tempfile
import webbrowser
import markdown2_python.markdown2 as markdown2
import markdown_python as markdown

#import ctypes
#from functools import partial


# TODO: set focus back to sublime after build
# TODO: option to embedded the css into the file or using external file
# TODO: Some way to make html prettier?
class MarkdownBuild(sublime_plugin.WindowCommand):
    def run(self):
        #hwnd = sublime.active_window().hwnd()
        s = sublime.load_settings("MarkdownBuild.sublime-settings")
        output_html = s.get("output_html", False)
        open_html_in = s.get("open_html_in", "browser")
        use_css = s.get("use_css", True)
        charset = s.get("charset", "UTF-8")
        markdown_extensions = s.get("extensions", [])
        markdown_version = s.get("markdown_implementation", 2)     # Default version [1]

        view = self.window.active_view()
        if not view:
            return
        file_name = view.file_name()
        if not file_name:
            return
        contents = view.substr(sublime.Region(0, view.size()))

        # Use the proper markdown version
        if(markdown_version == 2):
            md = markdown2.markdown(contents, extras=markdown_extensions)
        elif (markdown_version == 1):
            md = markdown.markdown(contents)
        else:
            # Invalid Version Number, notify user to update the sublime-settings file
            sublime.message_dialog("The markdown version in \"MarkdownBuild.sublime-settings\" is invalid.\nAvailable versions: 1, 2")
            return

        html = '<html><meta charset="' + charset + '">'
        if use_css:
            css = os.path.join(sublime.packages_path(), 'MarkdownBuild', 'markdown.css')
            if (os.path.isfile(css)):
                styles = open(css, 'r').read()
                html += '<style>' + styles + '</style>'
        html += "<body>" + md + "</body></html>"

        if output_html:
            html_name = os.path.splitext(file_name)[0]
            html_name = html_name + ".html"
            output = open(html_name, 'w')
        else:
            output = tempfile.NamedTemporaryFile(delete=False, suffix='.html')

        output.write(html.encode('UTF-8'))
        output.close()

        if open_html_in == "both":
            webbrowser.open("file://" + output.name)
            self.window.open_file(output.name)
        elif open_html_in == "sublime":
            self.window.open_file(output.name)
        else:
            webbrowser.open("file://" + output.name)
        #sublime.set_timeout(partial(ctypes.windll.user32.SwitchToThisWindow,sublime.active_window().hwnd(), 0), 250)
        #sublime.set_timeout(partial(ctypes.windll.user32.ShowWindow,sublime.active_window().hwnd(), 5), 500)
        #sublime.set_timeout(partial(ctypes.windll.user32.SetActiveWindow,sublime.active_window().hwnd()), 500)
        #sublime.set_timeout(partial(ctypes.windll.user32.SetFocus,sublime.active_window().hwnd()), 250)
