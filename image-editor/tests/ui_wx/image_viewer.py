import wx


class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')

        self.panel = wx.Panel(self.frame)

        instructions = 'Browse for an image'
        img = wx.Image(800, 640)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img))

        instruction_label = wx.StaticText(self.panel, label=instructions)
        self.photo_text = wx.TextCtrl(self.panel, size=(200, -1))
        browse_button = wx.Button(self.panel, label='Browse')
        browse_button.Bind(wx.EVT_BUTTON, self.on_browse)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.main_sizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                            0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(instruction_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photo_text, 0, wx.ALL, 5)
        self.sizer.Add(browse_button, 0, wx.ALL, 5)
        self.main_sizer.Add(self.sizer, 0, wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self.frame)

        self.panel.Layout()

        self.frame.Show()

    def on_browse(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg|"
        dialog = wx.FileDialog(
            None, "Choose a file",
            # wildcard=wildcard
        )
        if dialog.ShowModal() == wx.ID_OK:
            self.photo_text.SetValue(dialog.GetPath())
        dialog.Destroy()

        file_path = self.photo_text.GetValue()
        img = wx.Image(file_path, wx.BITMAP_TYPE_ANY)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.panel.Refresh()


if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
