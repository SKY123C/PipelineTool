from rv import rvtypes, commands

class CommandsInit(rvtypes.MinorMode):
    "A simple example that shows how to make shift-Z start/stop playback"

    def __init__(self):
        rvtypes.MinorMode.__init__(self)
        self.init("pyhello", [("new-source", self.setSRGBColorSpace, "")], None)

    def activate(self):
        pass
    
    def setSRGBColorSpace(self, event):
        for i in commands.nodesOfType("RVLinearize"):
            self.reset(i)
            commands.setIntProperty(i + '.color.sRGB2linear', [1], True)
        event.reject()

    def reset(self, line_node):
        commands.setIntProperty(line_node + '.color.logtype', [0], True)
        commands.setIntProperty(line_node + '.color.Rec709ToLinear', [0], True)
        commands.setFloatProperty(line_node + '.color.fileGamma', [1.0], True)


def createMode():
    return CommandsInit()
