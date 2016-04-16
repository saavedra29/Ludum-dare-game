import tkinter as tk
import settings as set


MENU_BIG_FONTS = 'TkDefaultFont 14'

class Configuration(tk.Toplevel):
    def __init__(self, root):
        super(Configuration, self).__init__()
        self.root = root
        self.gameTypeVar = tk.IntVar()
        self.shapeL = tk.BooleanVar()
        self.shapeO = tk.BooleanVar()
        self.shapeI = tk.BooleanVar()
        self.shapeS = tk.BooleanVar()
        self.shapeT = tk.BooleanVar()
        self.shapeZ = tk.BooleanVar()
        self.shapeJ = tk.BooleanVar()
        self.shapeL.set(True)
        self.shapeO.set(True)
        self.shapeI.set(True)
        self.shapeS.set(True)
        self.shapeT.set(True)
        self.shapeZ.set(True)
        self.shapeJ.set(True)
        photoL = tk.PhotoImage(file='images/L.png')
        photoO = tk.PhotoImage(file='images/O.png')
        photoI = tk.PhotoImage(file='images/I.png')
        photoS = tk.PhotoImage(file='images/S.png')
        photoT = tk.PhotoImage(file='images/T.png')
        photoZ = tk.PhotoImage(file='images/Z.png')
        photoJ = tk.PhotoImage(file='images/J.png')


        # Toplevel window for configuration
        self.focus_set()
        self.grab_set()
        self.title='Configurations'


        # Dimensions frame
        self.dimensionsFrame = tk.Frame(self,
                                        borderwidth=2, relief=tk.GROOVE,
                                        padx=10, pady=10)
        self.dimensionsFrame.grid(row=0, column=0)
        self.dimensionLabel = tk.Label(self.dimensionsFrame,
                                       font=MENU_BIG_FONTS,
                                       text='Dimensions')
        self.dimensionLabel.grid(row=0, column=0, columnspan=2)
        self.heightLabel = tk.Label(self.dimensionsFrame, text='Height:')
        self.heightLabel.grid(row=1, sticky=tk.W)
        self.widthLabel = tk.Label(self.dimensionsFrame, text='Width:')
        self.widthLabel.grid(row=2, sticky=tk.W)
        self.boxSizeLabel= tk.Label(self.dimensionsFrame, text='Box Size:')
        self.boxSizeLabel.grid(row=3, sticky=tk.W)

        self.heightDefault = tk.StringVar(self)
        self.heightDefault.set(set.height)
        self.heightSpin = tk.Spinbox(self.dimensionsFrame, from_=15, to=35,
                                     width=3, textvariable=self.heightDefault)
        self.heightSpin.grid(row=1, column=1)

        self.widthDefault = tk.StringVar(self)
        self.widthDefault.set(set.width)
        self.widthSpin = tk.Spinbox(self.dimensionsFrame, from_=6, to=20,
                                    width=3, textvariable=self.widthDefault)
        self.widthSpin.grid(row=2, column=1)

        self.sizeDefault = tk.StringVar(self)
        self.sizeDefault.set(set.boxSize)
        self.boxSizeSpin = tk.Spinbox(self.dimensionsFrame, from_=10, to=100,
                                      width=3, textvariable=self.sizeDefault)
        self.boxSizeSpin.grid(row=3, column=1)

        # Game type frame
        self.gameTypeFrame = tk.Frame(self,
                                      borderwidth=2, relief=tk.GROOVE,
                                      padx=10, pady=10)
        self.gameTypeFrame.grid(row=1, column=0)
        self.gameLabel = tk.Label(self.gameTypeFrame,
                                  font=MENU_BIG_FONTS,
                                  text='Game Type')
        self.gameLabel.grid(row=0)
        self.normalGameRadio = tk.Radiobutton(self.gameTypeFrame,
                                              text='Normal',
                                              variable=self.gameTypeVar,
                                              value=1)
        self.normalGameRadio.grid(row=1, sticky=tk.W)
        self.pausedGameRadio= tk.Radiobutton(self.gameTypeFrame,
                                              text='Paused',
                                              variable=self.gameTypeVar,
                                              value=2)
        self.pausedGameRadio.grid(row=2, sticky=tk.W)
        self.changeSpeedGameRadio= tk.Radiobutton(self.gameTypeFrame,
                                              text='Change Speed',
                                              variable=self.gameTypeVar,
                                              value=3)
        self.changeSpeedGameRadio.grid(row=3, sticky=tk.W)


        # Select shapes frame
        self.selectShapesFrame = tk.Frame(self,
                                          borderwidth=2, relief=tk.GROOVE,
                                          padx=10, pady=10)
        self.selectShapesFrame.grid(row=0, column=1, rowspan=2)
        self.selectLabel = tk.Label(self.selectShapesFrame,
                                    text='Select Shapes', font=MENU_BIG_FONTS)
        self.selectLabel.grid(row=0, column=0)

        self.L_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoL,
                                      variable=self.shapeL, onvalue=True,
                                      offvalue=False)
        self.L_check.image = photoL
        self.L_check.grid(row=1, column=0)

        self.J_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoJ,
                                      variable=self.shapeJ, onvalue=True,
                                      offvalue=False)
        self.J_check.image = photoJ
        self.J_check.grid(row=2, column=0)

        self.O_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoO,
                                      variable=self.shapeO, onvalue=True,
                                      offvalue=False)
        self.O_check.image = photoO
        self.O_check.grid(row=3, column=0)

        self.I_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoI,
                                      variable=self.shapeI, onvalue=True,
                                      offvalue=False)
        self.I_check.image = photoI
        self.I_check.grid(row=4, column=0)

        self.Z_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoZ,
                                      variable=self.shapeZ, onvalue=True,
                                      offvalue=False)
        self.Z_check.image = photoZ
        self.Z_check.grid(row=5, column=0)

        self.S_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoS,
                                      variable=self.shapeS, onvalue=True,
                                      offvalue=False)
        self.S_check.image = photoS
        self.S_check.grid(row=6, column=0)

        self.T_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoT,
                                      variable=self.shapeT, onvalue=True,
                                      offvalue=False)
        self.T_check.image = photoT
        self.T_check.grid(row=7, column=0)

        self.resultFrame = tk.Frame(self,
                                          borderwidth=2, relief=tk.GROOVE,
                                          padx=10, pady=10)
        self.resultFrame.grid(row=2, column=0, rowspan=2, columnspan=2)
        cancelButton = tk.Button(self.resultFrame, text='Cancel',
                                 command=self.destroy)
        cancelButton.grid(column=0, row=0)

        submitButton = tk.Button(self.resultFrame, text='Submit',
                                      command=self.submit)
        submitButton.grid(column=1, row=0)

    def submit(self):
        set.shapeS = self.shapeS.get()
        set.shapeO = self.shapeO.get()
        set.shapeI = self.shapeI.get()
        set.shapeZ = self.shapeZ.get()
        set.shapeT = self.shapeT.get()
        set.shapeJ = self.shapeJ.get()
        set.shapeL = self.shapeL.get()
        atLeastOneSet = set.shapeS or set.shapeO or set.shapeI or \
            set.shapeZ or set.shapeT or set.shapeJ or set.shapeL
        if not atLeastOneSet:
            tk.messagebox.showinfo('Warning!!!', 'Please choose at least'
                                                 ' one shape.')
            return
        set.gameTypeVar = self.gameTypeVar.get()
        set.height = int(self.heightSpin.get())
        set.width = int(self.widthSpin.get())
        set.boxSize = int(self.boxSizeSpin.get())
        for child in self.root.winfo_children():
            if not child.__dict__['_name'] == self._name:
                child.destroy()
        self.root.startGame()
        self.destroy()
