
import uno
import unohelper

from com.sun.star.lang import (XSingleComponentFactory, 
    XServiceInfo)

class Factory(unohelper.Base, XSingleComponentFactory, XServiceInfo):
    """ This factory instantiate new window content. 
    Registration of this class have to be there under 
    /org.openoffice.Office.UI/WindowContentFactories/Registered/ContentFactories.
    See its schema for detail. """
    
    # Implementation name should be match with name of 
    # the configuration node and FactoryImplementation value.
    IMPLE_NAME = "com.addon.autotextaddon"
    SERVICE_NAMES = IMPLE_NAME,
    
    @classmethod
    def get_imple(klass):
        return klass, klass.IMPLE_NAME, klass.SERVICE_NAMES
    
    def __init__(self, ctx, *args):
        self.ctx = ctx
        print("init")
    
    # XSingleComponentFactory
    def createInstanceWithContext(self, ctx):
        # No way to get the parent frame, not called
        return self.createInstanceWithArgumentsAndContext((), ctx)
    
    def createInstanceWithArgumentsAndContext(self, args, ctx):
        try:
            return create_window(ctx, args)
        except Exception as e:
            print(e)
    
    # XServiceInfo
    def supportedServiceNames(self):
        return self.SERVICE_NAMES
    
    def supportsService(self, name):
        return name in self.SERVICE_NAMES
    
    def getImplementationName(self):
        return self.IMPLE_NAME


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(*Factory.get_imple())


from com.sun.star.awt import WindowDescriptor, Rectangle
from com.sun.star.awt.WindowClass import SIMPLE
from com.sun.star.awt.WindowAttribute import SHOW, BORDER, SIZEABLE, MOVEABLE, CLOSEABLE
from com.sun.star.awt.VclWindowPeerAttribute import CLIPCHILDREN
from com.sun.star.awt.PosSize import POS, SIZE
from com.sun.star.beans import NamedValue


# Valid resource URL for docking window starts with 
# private:resource/dockingwindow. And valid name for them are 
# 9800 - 9809 (only 10 docking windows can be created).
# See lcl_checkDockingWindowID function defined in 
# source/sfx2/source/dialog/dockwin.cxx.
# If the name of dockingwindow conflict with other windows provided by 
# other extensions, strange result would be happen.
RESOURCE_URL = "private:resource/dockingwindow/9809"

EXT_ID = "com.addon.autotextaddon"

def create_window(ctx, args):
    """ Creates docking window. 
        @param ctx component context
        @param args arguments passed by the window content factory manager.
        @return new docking window
    """
    def create(name):
        return ctx.getServiceManager().createInstanceWithContext(name, ctx)
    
    if not args: return None
    
    frame = None # frame of parent document window
    for arg in args:
        name = arg.Name
        if name == "ResourceURL":
            if arg.Value != RESOURCE_URL:
                return None
        elif name == "Frame":
            frame = arg.Value
    
    if frame is None: return None # ToDo: raise exception
    
    # this dialog has no title and placed at the top left corner.
    dialog1 = "vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog1.xdl"
    window = None
    if True:
        toolkit = create("com.sun.star.awt.Toolkit")
        parent = frame.getContainerWindow()
        
        # Creates outer window
        # title name of this window is defined in WindowState configuration.
        desc = WindowDescriptor(SIMPLE, "window", parent, 0, Rectangle(0, 0, 100, 100), 
                SHOW | SIZEABLE | MOVEABLE | CLOSEABLE | CLIPCHILDREN)
        window = toolkit.createWindow(desc)
        
        # Create inner window from dialog
        dp = create("com.sun.star.awt.ContainerWindowProvider")
        child = dp.createContainerWindow(dialog1, "", window, None)
        child.setVisible(True)
        #child.setPosSize(0, 0, 0, 0, POS)  # if the dialog is not placed at 
                                            # top left corner
        child.getControl("CommandButton1").addActionListener(ActionListener(ctx))
        window.addWindowListener(WindowResizeListener(child))
    else:
        # shows tab control
        tabs = create("com.sun.star.comp.framework.TabWindowService")
        n = tabs.insertTab() # Create new tab, return value is tab id
        # Valid properties are: 
        # Title, ToolTip, PageURL, EventHdl, Image, Disabled.
        v1 = NamedValue("PageURL", dialog1)
        v2 = NamedValue("Title", "Test")
        v3 = NamedValue("EventHdl", ContainerWindowHandler(ctx, frame))
        tabs.setTabProps(n, (v1, v2, v3))
        tabs.activateTab(n) # each page should be activated after the creation
        
        window = tabs.Window # real window
    return window

# for normal window based dockingwindow

from com.sun.star.awt import XWindowListener, XActionListener

class ActionListener(unohelper.Base, XActionListener):
    
    def __init__(self, ctx):
        self.ctx = ctx
    
    def disposing(self, ev):
        pass
    
    # XActionListener
    def actionPerformed(self, ev):
        dialog = ev.Source.getContext()
        field = dialog.getControl("TextField1")
        self.message(dialog.getPeer(), field.getText())
    
    def message(self, parent, message):
        show_message(self.ctx, parent, message)


class WindowResizeListener(unohelper.Base, XWindowListener):
    
    def __init__(self, dialog):
        self.dialog = dialog
    
    def disposing(self, ev):
        pass
    
    # XWindowListener
    def windowMoved(self, ev):
        pass
    def windowShown(self, ev):
        pass
    def windowHidden(self, ev):
        pass
    
    def windowResized(self, ev):
        # extends inner window to match with the outer window
        if self.dialog:
            self.dialog.setPosSize(0, 0, ev.Width, ev.Height, SIZE)
            # ToDo: resize dialog elements


# for com.sun.star.comp.framework.TabWindowService based dockingwindow

from com.sun.star.awt import (XContainerWindowEventHandler, 
        XActionListener)

class ContainerWindowHandler(unohelper.Base, XContainerWindowEventHandler, XActionListener):
    
    def __init__(self, ctx, frame):
        self.ctx = ctx
        self.frame = frame
        self.parent = None
    
    def create(self, name):
        return self.ctx.getServiceManager().createInstanceWithContext(name, self.ctx)
    
    # XContainerWindowEventHandler
    def callHandlerMethod(self, window, obj, name):
        if name == "external_event":
            if obj == "initialize":
                self._initialize(window)
    
    def getSupportedMethodNames(self):
        return "external_event",
    
    def _initialize(self, window):
        btn = window.getControl("CommandButton1")
        btn.setActionCommand("btn1")
        btn.addActionListener(self)
    
    def disposing(self, ev):
        pass
    
    # XActionListener
    def actionPerformed(self, ev):
        cmd = ev.ActionCommand
        dialog = ev.Source.getContext()
        if cmd == "btn1":
            field = dialog.getControl("TextField1")
            self.message(dialog.getPeer(), field.getText())
    
    def message(self, parent, message):
        show_message(self.ctx, parent, message)


# Tool functions

def create_service(ctx, name, args=None):
    """ Create service with args if required. """
    smgr = ctx.getServiceManager()
    if args:
        return smgr.createInstanceWithArgumentsAndContext(name, args, ctx)
    else:
        return smgr.createInstanceWithContext(name, ctx)


from com.sun.star.awt import Rectangle

def show_message(ctx, peer, message, title="", type="messbox", buttons=1):
    """ Show text in message box. """
    older_imple = check_method_parameter(
        ctx, "com.sun.star.awt.XMessageBoxFactory", 
        "createMessageBox", 1, "com.sun.star.awt.Rectangle")
    
    if older_imple:
        box = peer.getToolkit().createMessageBox(
            peer, Rectangle(), type, buttons, title, message)
    else:
        name = {"messbox": "MESSAGEBOX", "infobox": "INFOBOX", 
                "warningbox": "WARNINGBOX", "errorbox": "ERRORBOX", 
                "querybox": "QUERYBOX"}[type]
        _type = uno.getConstantByName("com.sun.star.awt.MessageBoxType." + name)
        box = peer.getToolkit().createMessageBox(
                    peer, _type, buttons, title, message)
    n = box.execute()
    box.dispose()
    return n


def check_method_parameter(ctx, interface_name, method_name, param_index, param_type):
    """ Check the method has specific type parameter at the specific position. """
    cr = create_service(ctx, "com.sun.star.reflection.CoreReflection")
    try:
        idl = cr.forName(interface_name)
        m = idl.getMethod(method_name)
        if m:
            info = m.getParameterInfos()[param_index]
            return info.aType.getName() == param_type
    except:
        pass
    return False



from com.sun.star.task import XJobExecutor

class Switcher(unohelper.Base, XJobExecutor, XServiceInfo):
    # Not used
    
    IMPLE_NAME = "mytools.task.Switcher"
    SERVICE_NAMES = IMPLE_NAME,
    
    @staticmethod
    def get_imple(klass):
        return klass, klass.IMPLE_NAME, klass.SERVICE_NAMES
    
    def __init__(self, ctx, *args):
        self.ctx = ctx
    
    def trigger(self, arg):
        desktop = create_service(self.ctx, "com.sun.star.frame.Desktop")
        doc = desktop.getCurrentComponent()
        layoutmgr = doc.getCurrentController().getFrame().LayoutManager
        
        if layoutmgr.isElementVisible(RESOURCE_URL):
            layoutmgr.hideElement(RESOURCE_URL)
        else:
            layoutmgr.requestElement(RESOURCE_URL)
        
    # XServiceInfo
    def supportedServiceNames(self):
        return self.SERVICE_NAMES
    
    def supportsService(self, name):
        return name in self.SERVICE_NAMES
    
    def getImplementationName(self):
        return self.IMPLE_NAME


#g_ImplementationHelper.addImplementation(*Switcher.get_imple())

"""
' Switch through layout manager.
const RESOURCE_URL = "private:resource/dockingwindow/9809"

Sub SwitchDockingWindow
  layoutmgr = ThisComponent.getCurrentController().getFrame().LayoutManager
  if layoutmgr.isElementVisible(RESOURCE_URL) then
    layoutmgr.hideElement(RESOURCE_URL)
  else
    layoutmgr.requestElement(RESOURCE_URL)
  end if
End Sub
"""

"""
' Way to show/hide docking window through dispatch framework.
Sub ShowDockingWindow()
  id = 9809
  a = "DockingWindow" & CStr(id - 9800)
  p = CreateUnoStruct("com.sun.star.beans.PropertyValue")
  p.Name = a
  p.Value = True ' show or hide(False)
  
  dp = CreateUnoService("com.sun.star.frame.DispatchHelper")
  dp.executeDispatch(ThisComponent.getCurrentController().getFrame(), _
      ".uno:" & a, "_self", 0, Array(p))

End Sub
"""
