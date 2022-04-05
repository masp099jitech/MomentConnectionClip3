#CUSTOM LIBS
import edit as EditorUI
from version import versionControl
#SDS LIBS
import model
import member
from shape import Shape
import Transform3D as x3d
from Point3D import Point3D 
from Component import PrepareComponentForMember as PrepComp
from kwargmixin.kwargmixin import KWArgMixin as KM
from sds2.utility.gadget_protocol import GadgetComponent as GC
from Designable.ProcessableComponent import ProcessableComponent as DPC
import BasisTesting as BT
from Material import addPlate as plate
import Bounding as B
import Lists
#AUX LIBS
import sys
import os



'''
mainComp: class: the object that sds2 will instantiate and interact with
to produce the desired result.

functions SDS2 tries to call:

IsAllowedOnMember
Factory
SetReferencePointForMemberUI
MembersCurrentlyObserved
Add
DesignForMember
CreateCustomMultiEditableUI

'''
@versionControl
class MomentConnectionClips3(GC, DPC,KM):
    Name = 'JITECH Moment Connection Clips'
    ends = ['left','right']

    #CONSTRUCTOR
    def __init__(self, **kwargs):
        versionControl.init_factory()(self, **kwargs)#has to go first to avoid error
        DPC.__init__(self, **kwargs)
        KM.__init__(self, **kwargs)

    ''' sets the default values'''
    def defaults(self):
        s = Shape(model.member(self.member_number).section_size)
        self.length = self.Beam_Flange_Width()/2 - self.Beam_Web_Thickness()/2
        for face in ['NS','FS','Top','Bottom']:
            a = Shape(getattr(self,face+'_SectionSize'))
            setattr(self,face+'_AngleGage',a.LL_gage if getattr(self,face+'_LLV') else a.SL_gage)
            setattr(self,face+'_ColumnGage',s.gage if face in ['Top','Bottom'] else getattr(self,face+'_Length')-(Lists.edgeDistance[getattr(self,'FS'+'_BoltDia')]*2))
            setattr(self,face+'_Right_Aux_refx',Shape(self.right_supporting_member().section_size).gage/2)
            if s.depth - (s.k*2) < (1.25*2)+(getattr(self,face+'_Right_Aux_refx')*2.0)+((getattr(self,face+'_Right_Aux_BoltColumn')-1)*2)*getattr(self,face+'_Right_Aux_SpacingX'):
                weblen = 0.0
            else:
                weblen = s.depth - (s.k*2)
            setattr(self,face+'_Length',s.short_depth if face in ['Top','Bottom'] else weblen)
        setattr(self,'FS'+'_HoleDia',Lists.holeDiameterNum[getattr(self,'FS'+'_BoltDia')])
        pass

    def IsAllowedOnMember(self, mn):
        return model.member(mn).member_type == model.Column

    def MembersCurrentlyObserved(self):
        mems = [self.member_number]
        mems.append(self.left_supporting_member())
        mems.append(self.right_supporting_member())
        return mems
    '''instantiates component and sets attributes
    Recieves: host-
    member universe - 
    Returns: instance of component
    '''
    @classmethod
    def Factory(cls, host, member_universe):
        mainClass = cls()#instantiation
        PrepComp(mainClass, host)#connecting to host
        mainClass.SetReferencePoint(ref_point)
        return mainClass

    '''sets reference point relative to the top left
    Recieves: mn - member number
    '''
    def SetReferencePointForMemberUI(self, mn):
        self.ref_point = Point3D(0.,0.,0.)#x,y,z
        return self.ref_point #x,y,z

    '''Takes in uder input
    Recieves: mn - member number
    '''
    def Add(self, mn):
        PrepComp(self, mn)
        self.beam_m = self.beam.member_number
        self.defaults()
        return self.SetReferencePointForMemberUI(mn)
    '''set materials
    recieves: mn - member number
    '''
    def DesignForMember(self, mn):
        matfuncs = []
        mats = []
        if self.Top:
            plate(self, model.member(self.right_supporting_member().number),e = self.Beam_Lenght())
        return True

    #INHERITED FROM GADGET PROTOCOL
    '''set UI
    recieves: mn - member number
    '''
    @staticmethod #without this you need a third param
    def CreateCustomMultiEditableUI(model, gadget_factory):
        EditorUI.build_ui(model, gadget_factory)
        return True
    @property
    def beam(self):
        return model.member(self.member_number)
    @property
    def Xform(self):
        return x3d.MemberIndexTransform(self.member_number)
    @property
    def X(self):
        return self.Xform.GetBasisVectorX()
    @property
    def Y(self):
        return self.Xform.GetBasisVectorY()
    @property
    def Z(self):
        return self.Xform.GetBasisVectorZ()
    @property
    def T(self):
        return self.Xform.GetTranslation()
    def left_supporting_member(self):
        try:
            m = member.Member(self.member_number)
            return model.member(m.LeftEnd.Nodes[0])
        except:
            return None
    def right_supporting_member(self):
        try:
            m = member.Member(self.member_number)
            return model.member(m.RightEnd.Nodes[0])
        except:
            return None
    def Beam_Lenght(self):
        return self.beam.dtl_length
    def Beam_Depth(self):
        return Shape(self.beam.section_size).Depth
    def Beam_K(self):
        return Shape(Beam.section_size).k
    def Beam_Flange_Width(self):
        return Shape(self.beam.section_size).short_depth
    def Beam_Flange_Thickness(self):
        return Shape(self.beam.section_size).FlangeThickness
    def Beam_Web_Thickness(self):
        return Shape(model.member(self.beam.member_number).section_size).WebThickness
    def Beam_k(self):
        return Shape(model.member(self.beam.member_number).section_size).k - self.Beam_Web_Thickness()
    def Beam_Left_Elevation(self):
        return Point3D(self.beam.ends[0].location).z
    def Beam_Right_Elevation(self):
        return Point3D(self.beam.ends[1].location).z
        #AUXILLARY FUNCTIONS 
    #takes the string returns from elevations and converts it to an array of dimensions in inches
    def Elevations(self):
        var = self.elevations.split(',')
        arr = []
        for item in var:
            n = self.convertToInches(item)
            if n not in arr: 
                arr.append(n)
        return arr

    #takes a string and returns the dimension as a float in inches
    def convertToInches(self, num):
        try:
            result = 0
            if ('-' in num):
                var = num.split('-')
                result = result + (float(var[0])*12.0)
                del var[0]
            else:
                var = [num]
            for n in var:
                num = num.strip()
                if (" " in n):
                    arr = n.split(" ")
                    for i in arr:
                        i.replace(" ", "")
                        if ('/' in i):
                            fraction = i.split("/")
                            result = result + (float(fraction[0])/float(fraction[1]))
                        elif (i == ''):
                            pass
                        else:
                            result = result + float(i)
                elif ('/' in n):
                    fraction =n.split("/")
                    result = result + (float(fraction[0])/float(fraction[1]))
                else: 
                    result = result + float(n)
            return result
        except:
            sys.stdout.write('CONVERSION ERROR: A dimensions incorrectly formatted please fix')
            return 0   