from appJar import gui
from . import version, chronicle
import os


class AppWindow(object):
    def __init__(self):
        self.gui = gui(title='Chroniclr', geom='640x480', useTtk=True)
        self.gui.setTtkTheme('arc')
        self.chr = chronicle.Chronicle()
        self.selectedYear = None
        self.selectedEntry = None
        self.unsavedChanges = False
        self.openFile = 'New Chronicle'
        self.openFilePath = ''
        self.gui.setTitle('Chroniclr - {0}'.format(self.openFile))
        self.entryEditMode = False

        self.defineControls()
        self.defineWindowOptions()
        self.gui.go()


    def setHasUnsavedChanges(self):
        self.unsavedChanges = True
        self.gui.setTitle('Chroniclr - {0}*'.format(self.openFile))

    
    def resetHasUnsavedChanges(self):
        self.unsavedChanges = False
        self.gui.setTitle('Chroniclr - {0}'.format(self.openFile))


    def confirmUnsavedChanges(self):
        if self.unsavedChanges:
            rst = self.gui.yesNoBox(
                title='Unsaved Changes',
                message='Doing this will result in any unsaved changes being lost, continue?'
            )
            if rst:
                return True
            else:
                return False
        else:
            return True


    def updateYearList(self):
        c = self.chr
        yearList = []
        for year in c.data.keys():
            yearList.append(year)
        yearList.sort()
        self.gui.updateListBox(title='chronicleYearView', select=False, items=yearList)


    def updateEntryList(self):
        if not self.selectedYear == None:
            c = self.chr
            entryList = []
            for entry in c.data[self.selectedYear]:
                entryList.append(entry['id'])
            entryList.sort()
            self.gui.updateListBox(title='chronicleEntryView', select=False, items=entryList)


    def getEntryText(self):
        if not self.selectedYear == None:
            if not self.selectedEntry == None:
                for entry in self.chr.data[self.selectedYear]:
                    if entry['id'] == self.selectedEntry:
                        return entry['entry']
        return None


    def handleEvt_changeView(self, argList):
        change = self.gui.getListBox(argList)
        if len(change) == 0:
            vChange = None
        else:
            vChange = change[0]

        if argList == 'chronicleYearView':
            # Change Year
            self.selectedYear = vChange
            self.updateEntryList()
        elif argList == 'chronicleEntryView':
            # Change Entry
            self.selectedEntry = vChange


    def handleBtn_Exit(self):
        self.gui.stop()

    
    def handle_Exit(self):
        return self.confirmUnsavedChanges()


    def setOpenFile(self, name: str, path: str):
        self.openFile = name
        self.openFilePath = path


    def handleBtn_New(self):
        if self.confirmUnsavedChanges():
            self.chr = chronicle.Chronicle()
        self.updateYearList()
        self.updateEntryList()
        self.setOpenFile('New Chronicle', '')
        self.resetHasUnsavedChanges()


    def handleBtn_Save(self):
        if not self.openFilePath == '':
            self.chr.write(self.openFilePath)
            self.resetHasUnsavedChanges()
            print('Wrote chronicle to {0}'.format(self.openFilePath))
        else:
            self.handleBtn_SaveAs()
            


    def handleBtn_SaveAs(self):
        # Save as
        fn = self.gui.saveBox(
            title='Save Chronicle',
            fileTypes=[('Chronicle Data', '*.chronicle')]
        )
        if not fn == '':
            self.chr.write(fn)
            self.setOpenFile(os.path.basename(fn), fn)
            self.resetHasUnsavedChanges()
            print('Wrote chronicle to {0}'.format(fn))


    def handleBtn_Export(self):
        self.gui.infoBox(
            title='Information',
            message='Sorry, exporting is not implemented yet! :c'
        )


    def handleBtn_Load(self):
        if self.confirmUnsavedChanges():
            fn = self.gui.openBox(
                title='Load Chronicle',
                fileTypes=[('Chronicle Data', '*.chronicle')]
            )
            if not fn == '':
                self.chr.load(fn)
                self.setOpenFile(os.path.basename(fn), fn)
                self.resetHasUnsavedChanges()
                self.updateYearList()
                self.updateEntryList()


    def handleBtn_addEntry(self):
        if self.selectedYear == None:
            self.gui.errorBox(
                title='Error',
                message='You must select a year before adding entries!'
            )
        else:
            self.gui.setTextArea('entryText', '')
            self.entryEditMode = False
            self.gui.showSubWindow('Entry Editor')

    
    def handleBtn_removeEntry(self):
        if not self.selectedEntry == None:
            self.chr.removeEntry(self.selectedYear, self.selectedEntry)
            self.updateEntryList()
            self.setHasUnsavedChanges()


    def handleBtn_editEntry(self):
        if self.selectedYear == None:
            self.gui.errorBox(
                title='Error',
                message='You must select a year before editing entries!'
            )
        else:
            if self.selectedEntry == None:
                self.gui.errorBox(
                    title='Error',
                    message='You must select an entry to edit!'
                )
            else:
                for item in self.chr.data[self.selectedYear]:
                    if item['id'] == self.selectedEntry:
                        txt = item['entry']
                self.gui.setTextArea('entryText', txt)
                self.entryEditMode = True
                self.gui.showSubWindow('Entry Editor')


    def handleBtn_addYear(self):
        newYear = self.gui.integerBox(
            title='Add Year',
            message='Enter new year'
        )
        if not newYear == None:
            self.chr.addYear(newYear)
            self.updateYearList()
            self.setHasUnsavedChanges()

    
    def handleBtn_removeYear(self):
        if not self.selectedYear == None:
            self.chr.removeYear(self.selectedYear)
            self.updateYearList()
            self.updateEntryList()
            self.setHasUnsavedChanges()


    def handleBtn_entryEditSave(self):
        txt = self.gui.getTextArea('entryText')
        self.gui.clearTextArea('entryText')
        if txt == '':
            self.gui.errorBox(
                title='Error',
                message='Entries cannot be empty!',
                parent='Entry Editor'
            )
        else:
            if self.entryEditMode:
                # Edit
                print('Edit {0}[{1}]'.format(self.selectedYear, self.selectedEntry))
                for item in self.chr.data[self.selectedYear]:
                    if item['id'] == self.selectedEntry:
                        item['entry'] = txt
            else:
                # New
                print('New entry in {0}'.format(self.selectedYear))
                self.chr.addEntry(self.selectedYear, txt)
                self.updateEntryList()
            self.gui.hideSubWindow('Entry Editor')
            self.setHasUnsavedChanges()


    def showEULA_dialog(self):
        self.gui.showSubWindow('EULA')


    def showLicense_dialog(self):
        self.gui.showSubWindow('License Information')


    def showAbout_dialog(self):
        self.gui.showSubWindow('About Chroniclr')


    def handleBtn_entryEditCancel(self):
        self.gui.clearTextArea('entryText')
        self.gui.hideSubWindow('Entry Editor')


    def defineWindowOptions(self):
        app = self.gui

        app.setIcon(image='icon.ico')
        app.setResizable(canResize=False)


    def defineControls(self):
        app = self.gui
        app.setStopFunction(self.handle_Exit)

        nameList = ['New', 'Open', 'Save', 'Save as...', '-', 'Export', '-', 'Exit']
        funcList = [self.handleBtn_New, self.handleBtn_Load, self.handleBtn_Save, self.handleBtn_SaveAs, self.handleBtn_Export, self.handleBtn_Exit]

        app.createMenu('File')
        i = 0
        for name in nameList:
            if name == '-':
                app.addMenuSeparator('File')
            else:
                app.addMenuItem('File', name, funcList[i])
                i += 1

        app.createMenu('About')
        app.addMenuItem('About', 'About Chroniclr...', self.showAbout_dialog)
        app.addMenuItem('About', 'EULA', self.showEULA_dialog)
        app.addMenuItem('About', 'License', self.showLicense_dialog)

        app.startLabelFrame('Year', row=1, column=0)
        app.setSticky('news')
        app.addListBox(name='chronicleYearView')
        app.setListBoxMulti('chronicleYearView', multi=False)
        app.setListBoxChangeFunction('chronicleYearView', self.handleEvt_changeView)
        app.setListBoxGroup('chronicleYearView')
        app.addButton(title='Add Year', func=self.handleBtn_addYear)
        app.addButton(title='Remove Year', func=self.handleBtn_removeYear)
        app.stopLabelFrame()

        app.startLabelFrame('Entries', row=1, column=1)
        app.setSticky('news')
        app.addListBox(name='chronicleEntryView')
        app.setListBoxMulti('chronicleEntryView', multi=False)
        app.setListBoxChangeFunction('chronicleEntryView', self.handleEvt_changeView)
        app.setListBoxGroup('chronicleEntryView')
        app.addButton(title='Add Entry', func=self.handleBtn_addEntry)
        app.addButton(title='Edit Entry', func=self.handleBtn_editEntry)
        app.addButton(title='Remove Entry', func=self.handleBtn_removeEntry)
        app.stopLabelFrame()

        app.startSubWindow(name='Entry Editor', modal=True)
        app.setSticky('news')
        app.setSize(400, 265)
        app.setIcon(image='icon.ico')
        app.setResizable(canResize=False)
        app.addScrolledTextArea('entryText', 0, 0)
        app.addButton(title='Save Entry', func=self.handleBtn_entryEditSave)
        app.addButton(title='Cancel', func=self.handleBtn_entryEditCancel)
        app.stopSubWindow()

        app.startSubWindow(name='EULA', modal=True)
        app.setSize(400, 400)
        app.setSticky('news')
        app.setIcon(image='icon.ico')
        app.setResizable(canResize=False)
        app.addScrolledTextArea('eulaText')
        with open('EULA.txt', 'r') as eulaFile:
            txt = eulaFile.read()
        app.setTextArea('eulaText', txt)
        app.setTextAreaState('eulaText', 'disabled')
        app.stopSubWindow()

        app.startSubWindow(name='About Chroniclr', modal=True)
        app.setSize(400, 400)
        app.setSticky('nw')
        app.setIcon(image='icon.ico')
        app.setResizable(canResize=False)
        app.addLabel('l1', '    Chroniclr - Crusader Kings 2 Chronicling Utility:\n\n\tVersion {0}\n\tCopyright 2018 Nicholas J Burley'.format(version.APP_VERSION))
        app.addLabel('l2', '    Libraries:\n\n\tappJar\n\tVersion 0.93\n\tCopyright 2015-2017 Richard Jarvis')
        app.stopSubWindow()

        app.startSubWindow(name='License Information', modal=True)
        app.setSize(400, 400)
        app.setSticky('news')
        app.setIcon(image='icon.ico')
        app.setResizable(canResize=False)
        app.addScrolledTextArea('licenseText')
        with open('LICENSE', 'r') as lFile:
            txt = lFile.read()
        app.setTextArea('licenseText', txt)
        app.setTextAreaState('licenseText', 'disabled')
        app.stopSubWindow()