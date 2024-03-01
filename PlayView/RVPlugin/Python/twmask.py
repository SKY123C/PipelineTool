from rv import commands, rvtypes, extra_commands, runtime, rvui
import os
import time

class DisplayInfo(rvtypes.MinorMode):

    def __init__(self):
        rvtypes.MinorMode.__init__(self)

        self.init("displayInfo", [("post-render", self.new_source_callback, "")], None)
        self._drawOnPresentation = False
        self._isLoad = False
        self._source_list = []
        self._source_dict = {}

    # def new_source_callback(self, event):
    #     ...
    #     self._source_list = list(commands.nodesOfType("RVFileSource"))
    #     self.addOverlay()
    #     event.reject()
    def new_source_callback(self, event):
        for source in commands.nodesOfType("RVFileSource"):
            if source not in self._source_dict:
                self._source_dict[source] = 0
            count = self._source_dict[source]
            attr_res = commands.sourceAttributes(source)
            if attr_res and not count:
                bSuccess = self.addOverlay([source])
                if bSuccess:
                    self._source_dict[source] = count + 1
        event.reject()

    def activate(self):
        rvtypes.MinorMode.activate(self)
        self.addOverlay()
        extra_commands.displayFeedback("CGTeamWork display info", 3.0)  

    def deactivate(self):
        self.removeOverlay()
        rvtypes.MinorMode.deactivate(self)
        extra_commands.displayFeedback("CGTeamWork deactivated", 3.0) 

    def doText(self, overlay, overlayName, active = True, textval = "n/a", hpos = 0.0, vpos = 0.0, orig = "bottom-left", tscale = 1.0, labeltype = ""):
        
        overlayAttr = '%s.text:%s' % (overlay, overlayName)
        textcolor = [0.0,1.0,0.0,1.0]
        textsize =  0.0015 * tscale

        if (not commands.propertyExists('%s.position' % overlayAttr)):
            # Now the main text
            commands.newProperty('%s.position' % overlayAttr, commands.FloatType, 2)
            commands.newProperty('%s.origin' % overlayAttr, commands.StringType, 1)
            commands.newProperty('%s.color' % overlayAttr, commands.FloatType, 4)
            commands.newProperty('%s.spacing' % overlayAttr, commands.FloatType, 1)
            commands.newProperty('%s.size' % overlayAttr, commands.FloatType, 1)
            commands.newProperty('%s.scale' % overlayAttr, commands.FloatType, 1)
            commands.newProperty('%s.rotation' % overlayAttr, commands.FloatType, 1)
            commands.newProperty("%s.font" % overlayAttr, commands.StringType, 1)
            commands.newProperty("%s.text" % overlayAttr, commands.StringType, 1)
            commands.newProperty('%s.debug' % overlayAttr, commands.IntType, 1)
            commands.newProperty('%s.active' % overlayAttr, commands.IntType, 1)

        # Now the main text
        
        commands.setFloatProperty('%s.position' % overlayAttr, [ float(hpos), float(vpos) ], True)
        commands.setStringProperty('%s.origin' % overlayAttr, [orig], True)
        commands.setFloatProperty('%s.color' % overlayAttr, textcolor, True)
        commands.setFloatProperty('%s.spacing' % overlayAttr, [ 1.0 ], True)
        commands.setFloatProperty('%s.size' % overlayAttr, [ textsize ], True)
        commands.setFloatProperty('%s.scale' % overlayAttr, [ 1.0 ], True)
        commands.setFloatProperty('%s.rotation' % overlayAttr, [ 0.0 ], True)
        commands.setStringProperty("%s.text" % overlayAttr, [textval], True)
        commands.setIntProperty('%s.debug' % overlayAttr, [ 0 ], True)
        commands.setIntProperty('%s.active' % overlayAttr, [ 1 ], True)

    def removeOverlay(self):
        sources = []
        allsources = []
        allsources = commands.nodesOfType("RVFileSource")
        if not allsources:
            return
        sources = list(set(allsources))

        for source in sources:

            # Iterate overlays
            overlays = extra_commands.associatedNodes("RVOverlay",source)                                           
            for overlay in overlays:
                nodeProps = commands.properties(overlay)
                for np in nodeProps:
                    if "shot" in np:
                        if commands.propertyExists(np):
                            commands.deleteProperty(np)

    def addOverlay(self, sources=None):

        allsources = []
        allsources = sources if sources else commands.nodesOfType("RVFileSource")
        if not allsources:
            return
        sources = list(set(allsources))

        for source in sources:
            # Iterate overlays
            overlays = extra_commands.associatedNodes("RVOverlay",source)
            label = self.get_mask_label(source, ['shot_entity', 'task_entity', 'task_account', 'task_last_submit_time', 'task_task_leader_status'], ['Shot: ', 'Stage: ', 'Author: ', 'Time: ', 'Status: '])
            if not label:
                return                                        
            for overlay in overlays:
                # SHOT/ASSET/ARTIST
                self.doText( overlay, "shot", True, label,
                    -0.75, -0.45, "bottom-left", 1)

                # Switch overlay on
                overlayAttr = '%s.overlay.show' % overlay
                if (not commands.propertyExists(overlayAttr)):
                    commands.newProperty(overlayAttr, commands.IntType, 1)
                commands.setIntProperty(overlayAttr, [ 1 ], True)
        return True
    
    def get_mask_label(self, source, param_list, label_list):
        result = ''
        if len(param_list) != len(label_list):
            return
        e_list = [commands.propertyExists(source + f'.attributes.comment_{i}') for i in param_list]
        if not all(e_list):
            return
        label_value_list = zip(label_list, [commands.getStringProperty(source + f'.attributes.comment_{param}')[0]for param in param_list])
        metadata_value_list = self.get_other_metadata_attr(source)
        for label, value in list(label_value_list) + metadata_value_list:
            pak = label + value + '\n'
            result += pak
        result = result[0:-1]if result else result
        return result

    def get_other_metadata_attr(self, source):
        result = []
        for attr_tuple in commands.sourceAttributes(source):
            attr = attr_tuple[0]
            value = attr_tuple[1]
            if attr == "Movie/Comment":
                key_value_list = value.split(" ")
                for i in key_value_list:
                    key_value = i.split(":")
                    key = key_value[0].replace("comment_", "")
                    result.append([key + ": ", key_value[1]])
        return result
                


def createMode():
    return DisplayInfo()
