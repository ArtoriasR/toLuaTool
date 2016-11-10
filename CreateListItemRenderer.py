import sublime, sublime_plugin,time,getpass

class CreateListItemRendererCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sels = view.sel()
        selContent = ''
        if len(sels) > 0 :
            sels = sels[0]

        regionStr = view.substr(sels)

        for s in regionStr.split('\n'):
            selContent += '\t' + s + '\n';
        view.run_command('cut')

        curtime = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
        content = 'MyClass = {}\n'
        content = content + '\n'
        content = content + '--[[\n  @athor ' + getpass.getuser() +'\n  @desc \n  @date ' + curtime + '\n]]--'
        content = content + '\n'
        content = content + '\nfunction MyClass.create()\n'
        content = content + '\t'
        content = content + 'local this = ListItemRenderer.create()\n'
        content = content + '\tthis.Class = MyClass\n'
        content = content + '\tthis.name = "MyClass"\n'
        content = content + '\n'
        content = content + '\tfunction this.Start()\n'
        content = content + '\t\t\n'
        content = content + '\tend\n\n'
        content = content + '\tfunction this.UpdateView()\n'
        content = content + '\t\t\n'
        content = content + '\tend\n\n'
        content = content + '\tfunction this.OnDisable()\n'
        content = content + '\t\t\n'
        content = content + '\tend\n\n'
        content = content + '\treturn this'
        content = content + '\nend'
        view.insert(edit,0,content)
        sublime.set_clipboard('')
