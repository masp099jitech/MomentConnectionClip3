from Component import RegisterComponentType
from component_tools import RegisterComponentAddCommand
from MomentConnectionClips3 import MomentConnectionClips3
import Commands
import os.path



'''
Here is where the component and its image is added to the
SDS2 interface fore user selection

?Should be able to manipulate code here so that
the user can add a new one but the old versions can still run?

'''
image32 = os.path.join( os.path.dirname( __file__ ), "Images/32x32.png" )
image64 = os.path.join( os.path.dirname( __file__ ), "Images/64x64.png" )
icon32 = Commands.Icon(image32)
icon64 = Commands.Icon(image64)

RegisterComponentType(MomentConnectionClips3, MomentConnectionClips3.Name)
RegisterComponentAddCommand(MomentConnectionClips3, icons = Commands.IconSet((icon32,icon64)))
