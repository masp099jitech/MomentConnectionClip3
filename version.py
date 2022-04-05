from sds2.componentmetamorphoses import ComponentMetamorphoses as CM
from metamorphoses import Version, Attr, FutureAttr


'''
this is the version control of the component
here is where you would transform, rename and add attributes
added attributes require a new version
'''

attributes = [
    [
        #General
        ('kickerSectionSize', 'L3x3x1/4'),
        ('matGrade', 'A36'),
        ('Top', True),
        ('Bottom', True),
        ('beam_m', None),
        ],
        [
        ('Faces',[]),
        ('Top_Length',12.0),
        ('Bottom_Length',12.0),
        ('NS_Length',0.0),
        ('FS_Length',0.0),
        ('Top_SectionSize','L3x3x1/4'),
        ('Bottom_SectionSize','L3x3x1/4'),
        ('NS_SectionSize','L3x3x1/4'),
        ('FS_SectionSize','L3x3x1/4'),
        ('Top_Offset',0.0),
        ('Bottom_Offset',0.0),
        ('NS_Offset',0.0),
        ('FS_Offset',0.0),#_AngleGage
        ],
        [
        ('Top_Left_Host_AngleGage',0.0),
        ('Bottom_Left_Host_AngleGage',0.0),
        ('NS_Left_Host_AngleGage',0.0),
        ('FS_Left_Host_AngleGage',0.0),
        ('Top_Left_Aux_AngleGage',0.0),
        ('Bottom_Left_Aux_AngleGage',0.0),
        ('NS_Left_Aux_AngleGage',0.0),
        ('FS_Left_Aux_AngleGage',0.0),
        ],
        [
        ('Top_ConnMtrl','Bolted'),
        ('Bottom_ConnMtrl','Bolted'),
        ('NS_ConnMtrl','Bolted'),
        ('FS_ConnMtrl','Bolted'),        
        ],
        [
        ('Top_LLV','VT'),
        ('Bottom_LLV','VT'),
        ('NS_LLV','VT'),
        ('FS_LLV','VT'),
        ('FS_BoltDia','3/4 in'),
        ('FS_HoleDia',0.0),
        ('FS_HoleDiaLock',False),
        ('FS_Finish','Black'),
        ('FS_Direction',False),
        ('FS_Class','Field'),
        ('FS_BoltType','F1852N'),
        ('FS_HoleType','Standard Round'),
        ],
        [
        ('Top_Left_Host_AngleGageLock',False),
        ('Bottom_Left_Host__AngleGageLock',False),
        ('NS_Left_Host__AngleGageLock',False),
        ('FS_Left_Host__AngleGageLock',False),
        ],
        [
        ('Top_stbk',0.0),
        ('Bottom_stbk',0.0),
        ('NS_stbk',0.0),
        ('FS_stbk',0.0),
        ('Top_stbk_lock',False),
        ('Bottom_stbk_lock',False),
        ('NS_stbk_lock',False),
        ('FS_stbk_lock',False),
        ],
        [
        ('Top_Left_Aux_BoltRow',1),
        ('Bottom_Left_Aux_BoltRow',1),
        ('NS_Left_Aux_BoltRow',1),
        ('FS_Left_Aux_BoltRow',1),
        ('Top_Left_Aux_BoltColumn',1),
        ('Bottom_Left_Aux_BoltColumn',1),
        ('NS_Left_Aux_BoltColumn',1),
        ('FS_Left_Aux_BoltColumn',1),
        ('Top_Left_Aux_SpacingY',1.0),
        ('Bottom_Left_Aux_SpacingY',1.0),
        ('NS_Left_Aux_SpacingY',1.0),
        ('FS_Left_Aux_SpacingY',1.0),
        ('Top_Left_Aux_SpacingX',1.0),
        ('Bottom_Left_Aux_SpacingX',1.0),
        ('NS_Left_Aux_SpacingX',1.0),
        ('FS_Left_Aux_SpacingX',1.0),
        ('Top_Left_Aux_refx',1.0),
        ('Bottom_Left_Aux_refx',1.0),
        ('NS_Left_Aux_refx',1.0),
        ('FS_Left_Aux_refx',1.0),
        ],
        [
        ('Top_Right_Aux_BoltRow',1),
        ('Bottom_Right_Aux_BoltRow',1),
        ('NS_Right_Aux_BoltRow',1),
        ('FS_Right_Aux_BoltRow',1),
        ('Top_Right_Aux_BoltColumn',1),
        ('Bottom_Right_Aux_BoltColumn',1),
        ('NS_Right_Aux_BoltColumn',1),
        ('FS_Right_Aux_BoltColumn',1),
        ('Top_Right_Aux_SpacingY',1.0),
        ('Bottom_Right_Aux_SpacingY',1.0),
        ('NS_Right_Aux_SpacingY',1.0),
        ('FS_Right_Aux_SpacingY',1.0),
        ('Top_Right_Aux_SpacingX',1.0),
        ('Bottom_Right_Aux_SpacingX',1.0),
        ('NS_Right_Aux_SpacingX',1.0),
        ('FS_Right_Aux_SpacingX',1.0),
        ('Top_Right_Aux_refx',1.0),
        ('Bottom_Right_Aux_refx',1.0),
        ('NS_Right_Aux_refx',1.0),
        ('FS_Right_Aux_refx',1.0),
        ],
        [
        ('Top_Left_Host_BoltRow',1),
        ('Bottom_Left_Host_BoltRow',1),
        ('NS_Left_Host_BoltRow',1),
        ('FS_Left_Host_BoltRow',1),
        ('Top_Left_Host_BoltColumn',1),
        ('Bottom_Left_Host_BoltColumn',1),
        ('NS_Left_Host_BoltColumn',1),
        ('FS_Left_Host_BoltColumn',1),
        ('Top_Left_Host_SpacingY',1.0),
        ('Bottom_Left_Host_SpacingY',1.0),
        ('NS_Left_Host_SpacingY',1.0),
        ('FS_Left_Host_SpacingY',1.0),
        ('Top_Left_Host_SpacingX',1.0),
        ('Bottom_Left_Host_SpacingX',1.0),
        ('NS_Left_Host_SpacingX',1.0),
        ('FS_Left_Host_SpacingX',1.0),
        ('Top_Left_Host_refx',1.0),
        ('Bottom_Left_Host_refx',1.0),
        ('NS_Left_Host_refx',1.0),
        ('FS_Left_Host_refx',1.0),
        ],
        [
        ('Top_Right_Host_BoltRow',1),
        ('Bottom_Right_Host_BoltRow',1),
        ('NS_Right_Host_BoltRow',1),
        ('FS_Right_Host_BoltRow',1),
        ('Top_Right_Host_BoltColumn',1),
        ('Bottom_Right_Host_BoltColumn',1),
        ('NS_Right_Host_BoltColumn',1),
        ('FS_Right_Host_BoltColumn',1),
        ('Top_Right_Host_SpacingY',1.0),
        ('Bottom_Right_Host_SpacingY',1.0),
        ('NS_Right_Host_SpacingY',1.0),
        ('FS_Right_Host_SpacingY',1.0),
        ('Top_Right_Host_SpacingX',1.0),
        ('Bottom_Right_Host_SpacingX',1.0),
        ('NS_Right_Host_SpacingX',1.0),
        ('FS_Right_Host_SpacingX',1.0),
        ('Top_Right_Host_refx',1.0),
        ('Bottom_Right_Host_refx',1.0),
        ('NS_Right_Host_refx',1.0),
        ('FS_Right_Host_refx',1.0),
        ],
        [
        ('Top_Right_Host_AngleGage',0.0),
        ('Bottom_Right_Host_AngleGage',0.0),
        ('NS_Right_Host_AngleGage',0.0),
        ('FS_Right_Host_AngleGage',0.0),
        ('Top_Right_Aux_AngleGage',0.0),
        ('Bottom_Right_Aux_AngleGage',0.0),
        ('NS_Right_Aux_AngleGage',0.0),
        ('FS_Right_Aux_AngleGage',0.0),

        ('Top_Right_Aux_AngleGageLock',False),
        ('Bottom_Right_Aux_AngleGageLock',False),
        ('NS_Right_Aux_AngleGageLock',False),
        ('FS_Right_Aux_AngleGageLock',False),
        ('Top_Left_Aux_AngleGageLock',False),
        ('Bottom_Left_Aux_AngleGageLock',False),
        ('NS_Left_Aux_AngleGageLock',False),
        ('FS_Left_Aux_AngleGageLock',False),
        ('Top_Right_Host_AngleGageLock',False),
        ('Bottom_Right_Host_AngleGageLock',False),
        ('NS_Right_Host_AngleGageLock',False),
        ('FS_Right_Host_AngleGageLock',False),

        ],

    ]


class versionControl(CM):
    versions = {}
    arg = []

    for ver in range(0,len(attributes)):
        curratts = [[],[]]  
        for attr in attributes[ver]:
            #print(ver, attr[0], attr[1])
            curratts.append(Attr(attr[0], attr[1]))


        if ver == 0:
            versions[ver] = Version(*curratts)

        else:
            versions[ver] = Version(versions[ver-1], *curratts)




        
