
from plate_layout import BntPlateLayout
from point import PointLocate
import member
import model
from point import Point
from Point3D import Point3D
import Transform3D
from mtrl_list import MtrlLocate
from Designable.Proxies import RndBar


overlap_len = 2.0
step_len = 12.0
step_h = 5.7394
t = 0.375#thickness
tread_n = 15
space = 13.0384
width = 44
radius = 0.15

def main():
    results = model.PreOrPostSelection("Select Beam", filter_fn=lambda m: model.IsMember(m) and (m.member_type == model.Beam))
    if not results[0]: return
    for m in results[1]:
        mem = member.Member(m.number)
    pass


def returnT2(Mn):
    n=[
    Mem_Xform(Mn).GetBasisVectorX(),
    Mem_Xform(Mn).GetBasisVectorY(),
    Mem_Xform(Mn).GetBasisVectorZ()
    ]
    return n

def Mem_Xform(Mn):
    return Transform3D.MemberIndexTransform(Mn)



if __name__ == "__main__":
    print(main())


