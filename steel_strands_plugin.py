# -*- coding: mbcs -*-  
# -* - coding:UTF-8 -*-  
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class Steel_strands_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='run',
            objectName='steel_strands', registerQuery=False)
        
        pickedDefault = ''
        
        self.logic_invertxyKw = AFXBoolKeyword(self.cmd, 'logic_invert_xy', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.logic_invertxzKw = AFXBoolKeyword(self.cmd, 'logic_invert_xz', AFXBoolKeyword.TRUE_FALSE, True, False)

        self.epsKw = AFXFloatKeyword(self.cmd, 'num_eps', True, 5)

        self.name_modelKw = AFXStringKeyword(self.cmd, 'name_model', True, '')
        self.name_skxyKw = AFXStringKeyword(self.cmd, 'name_skxy', True, '')
        self.name_skxzKw = AFXStringKeyword(self.cmd, 'name_skxz', True, '')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):
        
        import steel_strandsDB
        reload(steel_strandsDB)
        return steel_strandsDB.SteelStrandsDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='steel_strands', 
    object=Steel_strands_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import steel_strands',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
