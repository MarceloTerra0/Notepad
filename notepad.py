import PySimpleGUI as sg
import pathlib

class Notepad:
	def __init__(self, theme, info, body):

		sg.theme(theme)

		WIN_W = 90
		WIN_H = 25
		STARTUP = True
		filename = None

		self.file_new  = 'New.........(CTRL+N)'
		self.file_open = 'Open........(CTRL+O)'
		self.file_save = 'Save........(CTRL+S)'

		menu_layout = [['File', [self.file_new, self.file_open,self.file_save, 'Save As', '---', 'Exit']],
						['Tools',['Word Count', '---', 'Light Mode', 'Standard Mode', 'Dark Mode']],
						['Help',['About']]]

		layout = [[sg.Menu(menu_layout)],
				 [sg.Text(f'> {info} <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
				 [sg.Multiline(f'{body}',font=('Consolas', 12), size=(WIN_W,WIN_H), key='_BODY_')]]

		self.window = sg.Window('Notepad', layout=layout, margins=(0,0), resizable=True, return_keyboard_events=True)

	def new_file(self):
		self.window['_BODY_'].update(value='')
		self.window['_INFO_'].update(value='> New File <')

	def word_count(self):
		words = [w for w in self.values['_BODY_'].split(' ') if w!='\n'and w!=' ']
		word_count = len(words)
		sg.PopupQuick(f'Word Count: {word_count}', auto_close=False)

	def open_file(self):
	    filename = sg.popup_get_file('Open', no_window=True)
	    if filename:
	        file = pathlib.Path(filename)
	        self.window['_BODY_'].update(value=file.read_text())
	        self.window['_INFO_'].update(value=file.absolute())
	        return file

	def save_file(self,file):
		if file:
			file.write_text(self.values.get('_BODY_'))
		else:
			self.save_file_as()

	def save_file_as(self):
		filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
		if filename:
			file = pathlib.Path(filename)
			file.write_text(self.values.get('_BODY_'))
			self.window['_INFO_'].update(value=file.absolute())
			return file

	def about_me(self):
		sg.popup_no_wait('Hello there!')

	def run(self):
		global theme
		global running
		global bodyAndInfo
		filename = None
		flag = True
		while True:
			self.event, self.values = self.window.read(timeout=1)
			if flag:
				self.window['_BODY_'].expand(expand_x=True, expand_y=True)
				flag = False

			if self.event in (None, 'Exit'):
				running = False
				break
			if self.event in (self.file_new, 'n:78'):
				self.new_file()
			if self.event in (self.file_open, 'o:79'):
				filename = self.open_file()
			if self.event in (self.file_save, 's:83'):
				self.save_file(filename)
			if self.event in ('Save As',):
				filename = self.save_file_as()
			if self.event in ('Word Count',):
				self.word_count()
			if self.event in ('About',):
				self.about_me()
			if self.event in ('Light Mode',):
				theme = 'Default1'
				self.window.close()
				bodyAndInfo = (filename, self.values.get('_BODY_'))
				break
			if self.event in ('Standard Mode',):
				theme = 'DarkBlue'
				self.window.close()
				bodyAndInfo = (filename, self.values.get('_BODY_'))
				break
			if self.event in ('Dark Mode',):
				theme = 'DarkGrey'
				self.window.close()
				bodyAndInfo = (filename, self.values.get('_BODY_'))
				break
			if self.event != '__TIMEOUT__':
				#time.sleep(2)
				#self.window['_BODY_'].update(value=self.event)
				print(self.event)
				if self.event == u"\u2386":
					print("sexo?")

if __name__ == '__main__':
	theme = 'DarkBlue'
	running = True
	bodyAndInfo = ['Untitled','']
	while running:
		if not bodyAndInfo[0]:
			bodyAndInfo = ('Untitled', bodyAndInfo[1])
		notepad = Notepad(theme, bodyAndInfo[0],bodyAndInfo[1])
		notepad.run()
