from ij import WindowManager, IJ

from java.lang.System import getProperty
from javax.swing import JScrollPane, JPanel, JLabel, JFrame, \
                        JButton, JCheckBox, ImageIcon, JSpinner, BoxLayout
from javax.swing.event import ChangeListener

from java.awt import Frame, GridLayout
from java.awt.event import ActionListener, MouseAdapter

import sys
sys.path.append(getProperty('fiji.dir') + '/plugins/Scripts/Plugins/Jymagor')
from Viewer import Viewer


# web resources
# http://fiji.sc/Jython_Scripting#Add_a_mouse_listener_to_the_canvas_of_every_open_image
# http://www.ini.uzh.ch/~acardona/fiji-tutorial/#s8
# https://wiki.python.org/jython/SwingExamples
# nice swing official API
# http://docs.oracle.com/javase/tutorial/uiswing/components/spinner.html
# http://docs.oracle.com/javase/6/docs/api/index.html?javax/swing/JSpinner.html


# Cleaning old instance of plugin (nice for debugging)
OldInstance = [w for w in Frame.getWindows() if w.visible and w.title == u'Jymagor']
if OldInstance:
    OldInstance[0].dispose() # output was a list

## degsin GUI
# Launch pane
curImp = JPanel()
curImp.setLayout(GridLayout(3, 1))

FindTargetBtn = JButton()
FindTargetBtn.setText('Find Target Stack')
curImp.add(FindTargetBtn)

#imp = WindowManager.getCurrentImage()
imp = IJ.getImage()
if imp:
    fname = imp.getTitle()
else:
    fname = 'None'
target = JLabel('Target: ' + fname)
curImp.add(target)

LaunchBtn = JButton()
LaunchBtn.setText('Launch/Update')
curImp.add(LaunchBtn)


class ML(MouseAdapter):
    def mousePressed(self, event):
        global imp, fname, target
        imp = IJ.getImage()
        nframes = imp.getNSlices()
        fname = imp.getTitle()
        if nframes>1 and not fname.startswith('dFoF movie of '):
            target.setText('Target: ' + fname)
            frame.pack()
FindTargetBtn.addMouseListener(ML())


class LaunchListener(ActionListener):
    def actionPerformed(self, event):
        if fname == 'None':
            return
        _Fst = int(Fst.getValue())
        _Fen = int(Fen.getValue())
        _Rst = int(Rst.getValue())
        _Ren = int(Ren.getValue())
        _dFoFmin = float(dFoFmin.getValue())
        _dFoFmax = float(dFoFmax.getValue())
        _NeedMovie = NeedMovie.isSelected()
        
        Viewer(imp, fname, _Fst, _Fen, _Rst, _Ren, _dFoFmin, _dFoFmax, _NeedMovie)
        
LaunchBtn.addActionListener(LaunchListener())


# Check box pane
CheckBoxes = JPanel()
CheckBoxes.setLayout(GridLayout(1, 2))


NeedMovie = JCheckBox('dFoF movie')
NeedMovie.setSelected(True)
CheckBoxes.add(NeedMovie)

Force4to1 = JCheckBox('Force 4:1')
Force4to1.setSelected(True)
CheckBoxes.add(Force4to1)

# spinner pane
spinners = JPanel()
spinners.setLayout(GridLayout(3, 3))

spinners.add(JLabel('F'))
Fst = JSpinner()
Fst.setValue(100)
spinners.add(Fst)
spinners.add(JLabel('-', JLabel.CENTER))
Fen = JSpinner()
Fen.setValue(300)
spinners.add(Fen)

spinners.add(JLabel('Res'))
Rst = JSpinner()
Rst.setValue(350)
spinners.add(Rst)
spinners.add(JLabel('-', JLabel.CENTER))
Ren = JSpinner()
Ren.setValue(450)
spinners.add(Ren)

# forget about float spin... 
# http://www.java2s.com/Code/Java/SWT-JFace-Eclipse/FloatingpointvaluesinSWTSpinner.htm
spinners.add(JLabel('dF/F %'))
dFoFmin = JSpinner()
dFoFmin.setValue(-10)
spinners.add(dFoFmin)
spinners.add(JLabel('-', JLabel.CENTER))
dFoFmax = JSpinner()
dFoFmax.setValue(40)
spinners.add(dFoFmax)

# http://docs.oracle.com/javase/6/docs/api/index.html?javax/swing/JSpinner.html
# why two Listeners? take this! http://stackoverflow.com/a/5184713/566035
def Update_dFoF(_min, _max):
    dFoF_name = 'dFoF map of ' + fname
    win_dFoFavg = WindowManager.getWindow(dFoF_name)
    if win_dFoFavg:
        _imp = win_dFoFavg.getImagePlus()
        _imp.getProcessor().setMinAndMax(_min, _max)
        _imp.updateAndDraw()
    dFoFmovie_name = 'dFoF movie of ' + fname
    win_dFoFmovie = WindowManager.getWindow(dFoFmovie_name)
    if win_dFoFmovie:
        _imp = win_dFoFmovie.getImagePlus()
        _imp.getProcessor().setMinAndMax(_min, _max)
        _imp.updateAndDraw()

class MaxSpinListener(ChangeListener):
    def stateChanged(self, event):
        _max = dFoFmax.getValue()
        if Force4to1.isSelected():
            _min = -abs(_max) / 4.0
            dFoFmin.setValue(_min)
        else:
            _min = dFoFmin.getValue()
        Update_dFoF(_min, _max)
dFoFmax.addChangeListener(MaxSpinListener())

class MinSpinListener(ChangeListener):
    def stateChanged(self, event):
        _min = dFoFmin.getValue()
        if Force4to1.isSelected():
            _max = abs(_min) * 4
            dFoFmax.setValue(_max)
        else:
            _max = dFoFmax.getValue()
        Update_dFoF(_min, _max)
dFoFmin.addChangeListener(MinSpinListener())


# main Frame
frame = JFrame("Jymagor")
icon = ImageIcon(getProperty('fiji.dir') + '/plugins/Scripts/Plugins/Jymagor/fish2.png')
frame.setIconImage(icon.getImage())

# taken from JCheckBox example at http://zetcode.com/gui/jythonswing/components/
frame.setLayout( BoxLayout(frame.getContentPane(), BoxLayout.Y_AXIS) )
frame.add(curImp)
frame.add(CheckBoxes)
frame.add(spinners)


# get the instance of the ImageJ main window
_ImageJ = IJ.getInstance()
frame.setLocation(_ImageJ.x+_ImageJ.width, _ImageJ.y)
frame.setSize(230, 250)

frame.setVisible(True)
