#custom libraries
import version
#SDS libraries
from sds2.utility.gadget_protocol import SubdialogController as gp
#dialog libraries
from dialog.label import Label
from dialog.value import Value
from dialog.entry import Entry
from dialog.listbox import Listbox
from dialog.combobox import Combobox
from dialog.checkbox import Checkbox
from dialog.choose_file import ChooseMtrl
from dialog.image import Image
from dialog.lockablefield import LockableEntry
from dialog.radio import Radio
from dialog.rules import Always, Changed
from dialog.dimension import DimensionStyled
import model as Model
import sys
import os.path
import Lists as menu
from shape import Shape


'''

This is where the user UI is made

ScreenController: class : that packs, packforgets, validates and 
in general manipulates the widgets available on the screen

build_ui : function : the bridge from the component to the 
screen controller called by CreateMultiEditableUI function
in the processable plugin

'''



class ScreenController:
	def graphical(self,frame):
		Label(frame, 'Safety cable holes cannot be made graphical and will update if processed')
	def general(self,frame):
		Label(frame,'Set Lenght to 0 to remove Clip')
		for face in ['NS','FS','Top','Bottom']:
			Label(frame,face+' Clip')
			setattr(self,face+'_SectionSize',ChooseMtrl(frame,face+'_SectionSize', ['Angle'], face+' Section Size:'))
			setattr(self,face+'_Length',Entry(frame,face+'_Length',DimensionStyled(),'Length of '+face+' angle:'))
			if face in ['NS','FS']:
				setattr(self,face+'_stbk',LockableEntry(frame,face+'_stbk_lock',face+'_stbk',DimensionStyled(),face+' stbk:'))
			setattr(self,face+'_LLV',Combobox(frame,face+'_LLV',['VT','HZ'],'Long leg :'))
			setattr(self,face+'_Offset',Entry(frame,face+'_Offset',DimensionStyled(),'Offset of '+face+' angle:'))
			#setattr(self,face+'_ColumnGage',Entry(frame,face+'_ColumnGage',DimensionStyled(),'Center-to-Center Spacing of '+face+' angle:'))
			setattr(self,face+'_Right_Aux_AngleGage',LockableEntry(frame,face+'_Right_Aux_AngleGageLock',face+'_Right_Aux_AngleGage',DimensionStyled(),'Gage '+face+' angle:'))
			setattr(self,face+'_ConnMtrl',Combobox(frame,face+'_ConnMtrl',['Bolted','Welded'],'Connection Type:'))
			setattr(self,face+'_Right_Aux_BoltRow',Entry(frame,face+'_Right_Aux_BoltRow',int,face+' Rows:'))
			setattr(self,face+'_Right_Aux_BoltColumn',Entry(frame,face+'_Right_Aux_BoltColumn',int,face+' Columns:'))
			setattr(self,face+'_Right_Aux_SpacingY',Entry(frame,face+'_Right_Aux_SpacingY',DimensionStyled(),face+' SpacingY:'))
			setattr(self,face+'_Right_Aux_SpacingX',Entry(frame,face+'_Right_Aux_SpacingX',DimensionStyled(),face+' SpacingX:'))
			setattr(self,face+'_Right_Aux_refX',Entry(frame,face+'_Right_Aux_refx',DimensionStyled(),face+' RefX:'))
			
			#Rules
			getattr(self,face+'_Length').AddRule(Changed, self._setsectionvalues(face))
			getattr(self,face+'_SectionSize').AddRule(Changed, self._setsectionvalues(face))
			getattr(self,face+'_LLV').AddRule(Always, self._setsectionvalues(face))
			if face in ['NS','FS']:
				getattr(self,face+'_stbk').lock.AddRule(Changed, self._setsectionvalues(face))
				getattr(self,face+'_stbk').entry.AddRule(Changed, self._setsectionvalues(face))
				getattr(self,face+'_Length').DisableIf(face+'_stbk_lock == True',[getattr(self,face+'_stbk').lock])
				getattr(self,face+'_Length').EnableIf(face+'_stbk_lock == False',[getattr(self,face+'_stbk').lock])


	def BoltSettings(self,frame):
		face = 'FS'#In case the faces ever need to be split
		setattr(self,face+'_BoltType',Combobox(frame, face+'_BoltType', menu.boltType,"Bolt type:"))
		setattr(self,face+'_Class',Radio(frame, face+'_Class', menu.fieldBolt, "Class:"))
		setattr(self,face+'_Direction',Checkbox(frame, face+'_Direction', "Flip direction"))
		setattr(self,face+'_Finish',Combobox(frame, face+'_Finish', menu.boltFinish, "Finish:"))
		setattr(self,face+'_BoltDia',Combobox(frame, face+'_BoltDia', menu.boltDiameter,"Bolt Diameter:"))
		setattr(self,face+'_HoleDia',LockableEntry(frame,face+'_HoleDiaLock',face+'_HoleDia',DimensionStyled(),'Hole Diameter:'))
		setattr(self,face+'_HoleType',Combobox(frame, face+'_HoleType', menu.holeType,"Hole Type:"))
		getattr(self,face+'_BoltDia').AddRule(Changed, self._setboltvalues())


	def _setboltvalues(self):
		return lambda evt: self.setboltvalues(evt)

	def setboltvalues(self, evt):
		face = 'FS'
		if not getattr(self,face+'_HoleDia').IsLocked():
			getattr(self,face+'_HoleDia').entry.Set(menu.holeDiameterNum[getattr(self,face+'_BoltDia').Get()])

	def _setsectionvalues(self, face):
		return lambda evt: self.setSectionvalues(evt, face)

	def setSectionvalues(self, evt , face):
		if not getattr(self,face+'_Right_Aux_AngleGage').IsLocked():
			a = Shape(getattr(self,face+'_SectionSize').Get())
			getattr(self,face+'_Right_Aux_AngleGage').entry.Set(a.LL_gage if getattr(self,face+'_LLV').Get() in 'VT' else a.SL_gage)
		a = Shape(self.Beam.section_size)
		if face in ['NS','FS'] and getattr(self,face+'_stbk').IsLocked():
			getattr(self,face+'_Length').Set(float(a.Depth) - (float(getattr(self,face+'_stbk').entry.Get()) *2.0))
		elif face in ['NS','FS'] and not getattr(self,face+'_stbk').IsLocked():
			getattr(self,face+'_stbk').entry.Set(0.0)
			getattr(self,face+'_Length').Set(float(a.Depth) - float(a.k)*2.0)




def build_ui(model, gadget_factory):
	controller = gp(model)
	self = ScreenController()
	self.Beam = Model.member(model[0].beam_m)	
	comp_column = gadget_factory.Column(
	controller,
	None,  # callback method, usually not necessary for columns
	'Moment Connection Clips',
	'',  #sort name
	'unique-form-name',
	defaultfold=True  # default state is open; defaults to False
	)
	gadget_factory.Leaf(
	comp_column,
	controller,
	self.general,  # no () here
	'General',
	'',  # sort name
	'unique-fold-id',
	defaultfold=True
	)
	gadget_factory.Leaf(
	comp_column,
	controller,
	self.BoltSettings,  # no () here
	'Bolt Settings',
	'',  # sort name
	'unique-fold-id',
	defaultfold=True
	)

#ADD A VALIDATIONS WHERE THE ENTRIES WONT ACCEPT ANYTHING BELOW ZERO.
#ADD A BANNER WITH AN IMAGE IN IT.