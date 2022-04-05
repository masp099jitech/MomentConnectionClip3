from Designable.Proxies import RolledSection, Weld, Hole, Bolt
from Point3D import Point3D 
from point import Point
import model
from Transform3D import Transform3D
from shape import Shape
import BasisTesting as BT
import Lists
import math
from member import Member
from job import Job

#creates all the materials and returns them in an array to design for member


def addPlate(self,supp_m,e = 3.0, atts={}):
    m = model.member(self.member_number)
    s = Shape(m.section_size)
    short_len = 'short_depth' if ('HSS' in m.section_size) else 'WebThickness'
    vertex = {
        'Top':{
            'Width':BT.Mem_Y(self,self.member_number,y=1),
            'Length':BT.Mem_Z(self,self.member_number),
            'X':BT.Mem_X(self,self.member_number,x=e), 
            'holedir':-1,   
        },
        'Bottom':{
            'Width':BT.Mem_Y(self,self.member_number,y=-1),
            'Length':BT.Mem_Z(self,self.member_number),
            'X':BT.Mem_X(self,self.member_number,x=e),
            'holedir':1,
        },
        'NS':{
            'Width':BT.Mem_Z(self,self.member_number,z=1),
            'Length':BT.Mem_Y(self,self.member_number),
            'X':BT.Mem_X(self,self.member_number,x=e),
            'holedir':1,
        },
        'FS':{
            'Width':BT.Mem_Z(self,self.member_number,z=-1),
            'Length':BT.Mem_Y(self,self.member_number),
            'X':BT.Mem_X(self,self.member_number,x=e),
            'holedir':-1,
        },
    }
    thk = s.WebThickness+Shape(getattr(self,'NS_SectionSize')).thick if getattr(self,'FS_Length') > 0.0 and getattr(self,'NS_Length') > 0.0 else s.WebThickness
    doubleShear = getattr(self,'FS_Length') > 0.0 and getattr(self,'NS_Length') > 0.0
    for face in ['Top','Bottom','NS','FS']:
        if face in ['NS','FS']:
            if getattr(self,face+'_stbk_lock'):
                short_len = 'short_depth'
            else:
                short_len = 'short_depth' if ('HSS' in m.section_size) else 'WebThickness'
        else:
            short_len = 'Depth'
        thk2 = thk if 'S' in face else s.FlangeThickness
        thk1 = Shape(getattr(self,face+'_SectionSize')).thick
        if getattr(self,face+'_Length') > 0.0:
            pmain = (
                Point3D(m.ends[0].location) 
                + (vertex[face]['Width'] * getattr(s,short_len)/2)
                + vertex[face]['X'] 
                + (vertex[face]['Length']* getattr(self,face+'_Offset'))
            )
            #print(getattr(self,face+'_Aux_ED'))
            pt1 = pmain - vertex[face]['Length'] * (getattr(self,face+'_Length')/2)
            pt2 = pmain + vertex[face]['Length'] * (getattr(self,face+'_Length')/2)
            pthole = pmain + vertex[face]['Width']*(getattr(self,face+'_Right_Aux_AngleGage')) 

            pt1, pt2 = swap(self,pt1,pt2, t= True if face in ['Bottom','NS'] else False)
            R = addAngle(self,face,pt1,pt2)
            if getattr(self,face+'_ConnMtrl') in 'Bolted':
                H = holeAdd(self,R,face,pthole)
                #BT.addRndBarProxy(self,self.member_number, pthole, vertex[face]['X'], 5.0, 0.25,  color = (0,0,0)).Add()
                ptboltholes = []
                for d in [-1,1]:
                    ptholewref = pthole+(getattr(self,face+'_Right_Aux_refx'))*vertex[face]['Length']*d
                    for r in range(0,(getattr(self,face+'_Right_Aux_BoltRow'))):
                        for c in range(0,(getattr(self,face+'_Right_Aux_BoltColumn'))):
                            pt = ptholewref+(getattr(self,face+'_Right_Aux_SpacingX')*r)*vertex[face]['Width']+(getattr(self,face+'_Right_Aux_SpacingY')*c)*vertex[face]['Length']*d
                            if pt not in ptboltholes:
                                #BT.addRndBarProxy(self,self.member_number, pt,  vertex[face]['X'], 5.0, 0.25,  color = (0,0,0)).Add()
                                boltHoles(self,pt,BT.Mem_X(self,self.member_number),0.385,Shape(getattr(self,face+'_SectionSize')).thick)
                HoleMatch(self,H,supp_m.materials[0])
                #if (face in 'NS' and not doubleShear) or face not in 'NS': #DOUBLE SHEAR ON
                    #HoleMatch(self,H,m.materials[0])
                    #for i in [1,-1]:
                        #ptbolt = pthole + (vertex[face]['Length'] * getattr(self,face+'_ColumnGage')/2 * i )
                        #boltHoles(self, ptbolt, vertex[face]['Width'] , thk1, thk2)

def swap(self,pt1,pt2, t=True):
    if t:
        return pt2, pt1
    else:
        return pt1,pt2

def TransformT(self, TransMat = [0.0,0.0,0.0], RotMat = [0.0,0.0,0.0], T = None):
    T.Translate(Point3D(TransMat[0],TransMat[1],TransMat[2]))
    T.RotateX(RotMat[0])
    T.RotateY(RotMat[1])
    T.RotateZ(RotMat[2])
    return T

def addAngle(self,face, pt1,pt2,i=0):
    R = RolledSection()
    R.Member = self.member_number
    R.WorkpointSlopeDistance = getattr(self,face+'_Length')
    R.MaterialGrade = Job().angle_conn_specs 
    R.ToeInOrOut = 'In'#getattr(self,end+'_'+face+'_ToeInOut') #if side in 'NS' else 'Out',
    R.IsLongLegVerticalMaterial = getattr(self,face+'_LLV')+'.' #if getattr(self,'LLT') in 'Supporting' else 'HZ.'
    R.SectionSize = getattr(self,face+'_SectionSize')#'L4x4x5/8'# getattr(self,'sectionSize')
    R.Point1 = Point(pt1)
    R.Point2 = Point(pt2)
    R.mtrl_is_main = 'No',
    R.MaterialColor3d = 'Medium_miscMem'
    R.Add()
    return R


def holeAdd(self,m,face, P = None):#1
    h = Hole()
    #h.MaterialFace = face
    h.Material = m
    h.ReferenceOffsetX = float(getattr(self,face+'_Right_Aux_refx'))
    h.ReferenceOffsetY = 0.0
    h.Columns = int(getattr(self,face+'_Right_Aux_BoltColumn'))
    h.Rows = int(getattr(self,face+'_Right_Aux_BoltRow'))
    h.SpacingX = float(getattr(self,face+'_Right_Aux_SpacingX'))
    h.SpacingY = float(getattr(self,face+'_Right_Aux_SpacingY'))
    h.pt1 = Point(P) 
    h.Diameter = float(getattr(self,'FS'+'_HoleDia'))
    h.HoleType = str(getattr(self,'FS'+'_HoleType'))
    h.GroupRotation = 0
    h.Locate =  'Below'
    h.Matchable = 'Yes' 
    h.BoltDiameter = float(Lists.boltDiameterNum[getattr(self,'FS'+'_BoltDia')])
    h.BoltType = str(getattr(self,'FS'+'_BoltType'))
    h.ShowWindow = 'No'
    h.ShouldBeValid = 'Yes' #this should always be yes unless its an option in the UI
    h.Create()
    return h

def _HoleMatch(self, mat, P):
    try:
        return HoleMatch(self, mat, mat2,supmat)
    except Exception, e:
        pass

def HoleMatch(self, hole, P, suppmat = 0):
    h = Hole()
    h.Material = [P,]
    h.Holes = [hole,]
    h.Create()

def boltHoles(self, pt, basis, thk1, thk2):#3
    bolt1 = Bolt()
    bolt1.HeadPoint = Point(pt + basis * thk1)
    bolt1.NutPoint = Point(pt - basis * thk2)
    bolt1.Direction = "In" if getattr(self,'FS'+'_Direction') else "Out"
    bolt1.Member = Member(self.member_number)
    bolt1.Diameter = Lists.boltDiameterNum[getattr(self,'FS'+'_BoltDia')]
    bolt1.Length = boltLength(self,thk1+thk2,getattr(self,'FS'+'_BoltDia'))
    bolt1.Grip = thk1+thk2
    bolt1.Finish = getattr(self,'FS'+'_Finish')
    bolt1.PrimaryNutType = "Heavy hex"
    bolt1.PrimaryNutGrade = "A563"
    bolt1.PrimaryNutWasher.TypeDescription = "Hardened"
    bolt1.PrimaryNutWasher.GradeDescription = "F436"
    bolt1.BoltType = getattr(self,'FS'+'_BoltType')
    bolt1.IsTensionControl = "No" 
    bolt1.Boltless = "No"
    bolt1.IsFieldBolt = getattr(self,'FS'+'_Class')
    bolt1.HillsideWasherAngle = 0
    bolt1.ShowWindow = 'No'
    bolt1.Direction = "Out" 
    bolt1.SuppressWarnings = "Yes"
    bolt1.AddPointToPoint()

def boltLength(self,grip,boltDia,washer = .177):
    boltNutThk = {"1/2 in":0.6875,"5/8 in":.875,"3/4 in":1,"7/8 in":1.125,"1 in":1.25,"1 1/8 in": 1.5}
    return x_round(self,grip + washer + boltNutThk[boltDia])

def x_round(self,x):
    return math.ceil(x*4)/4  