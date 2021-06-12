'''
    Created by Oliver J Post & Alexander Lashko

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name" : "Human Generator 3D",
    "author" : "OliverJPost",
    "description" : "Human Generator allows you to generate humans including clothing, poses and emotions",
    "blender" : (2, 83, 0),
    "version" : (2, 0, 4), #RELEASE update version number
    "location" : "Add-On Sidepanel > HumGen",
    "wiki_url": "http://humgen3d.com",
    "tracker_url": "http://humgen3d.com",
    "warning" : "",
    "category" : ""
}

import bpy #type: ignore
import sys, os
from bpy.utils import previews #type: ignore
from bpy.app.handlers import persistent #type: ignore

if __name__ != "HG3D":
    sys.modules['HG3D'] = sys.modules[__name__]

from . import auto_load
from . HG_UPDATE import check_update
from . HG_CONTENT_PACKS import *
from . user_interface import HG_UTILITY_UILISTS
from . HG_PROPS import *
auto_load.init()

########### startup procedure #########
@persistent
def HG_start(dummy):
    """Runs the activating class when a file is loaded or blender is opened
    """    
    bpy.ops.HG3D.activate()
    cpacks_refresh(None, bpy.context)
    check_update()

from . HG_PCOLL import  preview_collections

def _initiate_preview_collections():
    #initiate preview collections
    pcoll_names = [
    'humans',
    'poses',
    'outfit',
    'footwear',
    'hair',
    'face_hair',
    'expressions',
    'patterns',
    'textures'
    ]
    
    for pcoll_name in pcoll_names:
        preview_collections.setdefault(
            f"pcoll_{pcoll_name}",
            bpy.utils.previews.new()
            )
def _initiate_custom_icons():
    #load custom icons
    hg_icons = preview_collections.setdefault("hg_icons", bpy.utils.previews.new())
    hg_dir = os.path.join(os.path.dirname(__file__), 'icons') 
    icons = [
        'hair',
        'body',
        'face',
        'skin',
        'clothing',
        'footwear',
        'expression',
        'finalize',
        'simulation',
        'pose',
        'length',
        'cold',
        'warm',
        'normal',
        'inside',
        'outside',
        'male_true', 
        'male_false',
        'female_true',
        'female_false',
        'HG_icon',
        'humans',
        'textures',
        'eyes'
        ]
    for icon in icons:
        hg_icons.load(icon, os.path.join(hg_dir, icon + '.png'), 'IMAGE')
    preview_collections["hg_icons"] = hg_icons

def _initiate_ui_lists():
    sc = bpy.types.Scene
    # sc.outfits_col_m = bpy.props.CollectionProperty(type = HG_BATCH_UILIST.CLOTHING_ITEM_M) 
    # sc.outfits_col_m_index = bpy.props.IntProperty(name = "Index", default = 0)
    # sc.pose_col = bpy.props.CollectionProperty(type = HG_BATCH_UILIST.POSE_ITEM) 
    # sc.pose_col_index = bpy.props.IntProperty(name = "Index", default = 0)        
    # sc.expressions_col = bpy.props.CollectionProperty(type = HG_BATCH_UILIST.EXPRESSION_ITEM) 
    # sc.expressions_col_index = bpy.props.IntProperty(name = "Index", default = 0)      
    sc.contentpacks_col = bpy.props.CollectionProperty(type = HG_CONTENT_PACK) 
    sc.contentpacks_col_index = bpy.props.IntProperty(name = "Index", default = 0)     
    sc.installpacks_col = bpy.props.CollectionProperty(type = HG_INSTALLPACK) 
    sc.installpacks_col_index = bpy.props.IntProperty(name = "Index", default = 0)    
    sc.modapply_col = bpy.props.CollectionProperty(type = HG_UTILITY_UILISTS.MODAPPLY_ITEM) 
    sc.modapply_col_index = bpy.props.IntProperty(name = "Index", default = 0)     
    sc.shapekeys_col = bpy.props.CollectionProperty(type = HG_UTILITY_UILISTS.SHAPEKEY_ITEM) 
    sc.shapekeys_col_index = bpy.props.IntProperty(name = "Index", default = 0)   
    sc.savehair_col = bpy.props.CollectionProperty(type = HG_UTILITY_UILISTS.SAVEHAIR_ITEM) 
    sc.savehair_col_index = bpy.props.IntProperty(name = "Index", default = 0)  
    sc.saveoutfit_col = bpy.props.CollectionProperty(type = HG_UTILITY_UILISTS.SAVEOUTFIT_ITEM) 
    sc.saveoutfit_col_index = bpy.props.IntProperty(name = "Index", default = 0)

def register():
    #RELEASE remove print statements
    #RELEASE TURN OFF SSS
    auto_load.register()
    
    bpy.types.Scene.HG3D = bpy.props.PointerProperty(type=HG_SETTINGS) #Main props
    bpy.types.Object.HG = bpy.props.PointerProperty(type=HG_OBJECT_PROPS) #Object specific props

    _initiate_preview_collections()
    _initiate_custom_icons()
    _initiate_ui_lists()  

    #load handler
    if not HG_start in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(HG_start)

def unregister():
    auto_load.unregister()
    
    #remove handler
    if HG_start in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(HG_start)

    #remove pcolls
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

if __name__ == "__main__":
    register()