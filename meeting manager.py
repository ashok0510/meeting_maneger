import clipboard
import webbrowser
import wx
import sqlite3

mydb=sqlite3.connect('mydatadatabase.db')

myCursor=mydb.cursor()

myCursor.execute('create table  if not exists meeting(name text, address text, password)')
mydb.commit()

class MyFrame(wx.Frame):
	def __init__(self):
		super().__init__(parent = None, title="meeting manager", size=(400, 150))
		panel = wx.Panel(self)
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		my_name = wx.StaticText(panel, id= -1, label="enter your meeting profile name")
		self.my_text = wx.TextCtrl(panel)
		my_sizer.Add(self.my_text, 0, wx.ALL | wx.EXPAND, 10)
		my_btn = wx.Button(panel, label="ok")
		my_btn.Bind(wx.EVT_BUTTON, self.on_press)
		my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 20)
		panel.SetSizer(my_sizer)

		fileMenu = wx.Menu()
		menuNew = fileMenu.Append(wx.ID_NEW, "add new meeting data")
		menuDel = fileMenu.Append(wx.ID_DELETE, "delete meeting data")
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"file")
		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
		self.Bind(wx.EVT_MENU, self.OnDelete, menuDel)
		self.Show()

	def OnDelete(self, e):
		dg = wx.TextEntryDialog(self, "enter your meeting name to delete","delete meeting data")
		if dg.ShowModal() == wx.ID_OK:
			data = dg.GetValue()
			d=(data,)
			myCursor.execute('''DELETE  FROM meeting WHERE name=?''', d)
			mydb.commit()
			print(myCursor.rowcount,"record is deleted")
		dg.Destroy()

	def OnNew(self, e):
		dlg = wx.TextEntryDialog(self, "enter your meeting name","enter your meeting info")
		if dlg.ShowModal() == wx.ID_OK:
			dlg2 = wx.TextEntryDialog(self, "enter your meeting URL","add your meeting data")
			if dlg2.ShowModal() == wx.ID_OK:
				dlg3 = wx.TextEntryDialog(self, "enter your meeting password","add meeting data")
				if dlg3.ShowModal() == wx.ID_OK:
					user = dlg .GetValue()
					url = dlg2.GetValue()
					password = dlg3.GetValue()
					val=(user, url, password)
					myCursor.execute('''INSERT INTO meeting (name, address, password) VALUES (?, ?, ?)''' , val)
					mydb.commit()
					print(myCursor.rowcount,"record is insert")
		dlg.Destroy()

	def on_press(self, event):
		enter = self.my_text.GetValue()
		adr=(enter, )
		myCursor.execute('''SELECT * FROM meeting WHERE name=?''', adr)
		myResult=myCursor.fetchall()
		for x in myResult:
			if enter == x[0]:
				webbrowser.open(x[1])
				clipboard.copy(x[2])


if __name__ == "__main__":
	app = wx.App()
	frame = MyFrame()
	app.MainLoop()