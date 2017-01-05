import sublime, sublime_plugin,time,getpass

class CreateLuaPanelBaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        #当前视图
        view = self.view
        #当前选择的区域
        sels = view.sel()
        selContent = ''
        if len(sels) > 0 :
            #获取以一个选中区域
            sels = sels[0]
        #获取选中区域内容
        regionStr = view.substr(sels)
        #重新拼接字符串--前面插入一个tab
        for s in regionStr.split('\n'):
            selContent += '\t' + s + '\n';
        #剪切掉当前选中的内容
        view.run_command('cut')
        #获取当前时间
        curtime = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
        content = 'MyPanel = {}\n'
        content = content + '\n'
        content = content + '--[[\n  @athor ' + getpass.getuser() +'\n  @desc \n  @date ' + curtime + '\n]]--'
        content = content + '\n'
        content = content + '\nfunction MyPanel.create()\n'
        content = content + '\t'
        content = content + 'local this = LuaPanelBase.create()\n'
        content = content + '\tthis.Class = MyPanel\n'
        content = content + '\tthis.name = "MyPanel"\n'
        content = content + '\n'
        content = content + '\tfunction this.onActive()\n'
        content = content + '\t\t\n'
        content = content + '\tend\n'
        content = content + '\n'
        content = content + '\tfunction this.onDisactive()\n'
        content = content + '\t\t\n'
        content = content + '\tend\n'
        content = content + '\n'
        content = content + '\treturn this'
        content = content + '\nend'
        view.insert(edit,0,content)
        #清空剪切板
        sublime.set_clipboard('')
