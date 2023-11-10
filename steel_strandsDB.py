# -*- coding: mbcs -*-  
# -* - coding:UTF-8 -*-  
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
from abaqusGui import sendCommand

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class SteelStrandsDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Steel Strands Creator',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            
        # sendCommand("spring_batch")
        # sendCommand("reload(spring_batch)")
        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Next')
        # text = FXText(p=self, opts=TEXT_WORDWRAP|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        # text.setText(str(mdb.models.keys()))

        model_cb = AFXComboBox(p=self, ncols=0, nvis=1, text='Model:', tgt=form.name_modelKw, sel=0)
        model_cb.setMaxVisible(10)
        for model in mdb.models.keys():
            model_cb.appendItem(model)
        if not form.name_modelKw.getValue() in mdb.models.keys():
            form.name_modelKw.setValue(mdb.models.keys()[0])

        sketch_XY_cb = AFXComboBox(p=self, ncols=0, nvis=1, text='Sketch XY:', tgt=form.name_skxyKw, sel=0)
        sketch_XY_cb.setMaxVisible(10)
        FXCheckButton(p=self, text='Invert X-Y', tgt= form.logic_invertxyKw, )

        sketch_XZ_cb = AFXComboBox(p=self, ncols=0, nvis=1, text='Sketch XZ:', tgt=form.name_skxzKw, sel=0)
        sketch_XZ_cb.setMaxVisible(10)
        FXCheckButton(p=self, text='Invert X-Z', tgt= form.logic_invertxzKw, )

        for model in mdb.models.keys():
            for sketch in mdb.models[model].sketches.keys():
                sketch_XY_cb.appendItem(model + '|' + sketch)
                sketch_XZ_cb.appendItem(model + '|' + sketch)
        
        if not form.name_skxyKw.getValue():
            form.name_skxyKw.setValue(model + '|' + mdb.models[model].sketches.keys()[0])

        if not form.name_skxzKw.getValue():
            form.name_skxzKw.setValue(model + '|' + mdb.models[model].sketches.keys()[0])

        tolerance = AFXTextField(p=self, ncols=12, labelText='Tolerance:', tgt=form.epsKw, sel=0)
        tolerance.setText('1e-7')
