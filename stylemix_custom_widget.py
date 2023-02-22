# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import imgui
from gui_utils import imgui_utils
 # importing module
import time
#----------------------------------------------------------------------------

class StyleMixingLauraWidget:
    def __init__(self, viz):
        self.viz        = viz
        self.seed_def   = 1000
        self.seed       = self.seed_def
        self.animate    = False
        self.enables    = []
        self.contador   = 0
        self.multiple_images = False
      

    @imgui_utils.scoped_by_object_id
    def __call__(self, show=True):
        viz = self.viz
        num_ws = viz.result.get('num_ws', 0)
        num_enables = viz.result.get('num_ws', 111)
        self.enables += [False] * max(num_enables - len(self.enables), 0)
        self.caracteristicas = [0,0,0]

        if show:
            imgui.text('Stylemix')
            imgui.same_line(viz.label_w)
            with imgui_utils.item_width(viz.font_size * 11), imgui_utils.grayed_out(num_ws == 0):
                _changed, self.seed = imgui.input_int('##seed', self.seed)
            imgui.same_line(viz.label_w + viz.font_size * 11 + viz.spacing)
            with imgui_utils.grayed_out(num_ws == 0):
                _clicked, self.animate = imgui.checkbox('Anim', self.animate)
                if (_clicked == True):
                    self.multiple_images = True


            # LAURA
            if (self.multiple_images == True and self.viz.capture_widget.disabled_time == 0):
                print ("click")
                self.viz.capture_widget.dump_image = True
                self.viz.capture_widget.defer_frames = 2
                self.viz.capture_widget.disabled_time = 0.5    
            pos2 = imgui.get_content_region_max()[0] - 1 - viz.button_w
            pos1 = pos2 - imgui.get_text_line_height() - viz.spacing
            pos0 = viz.label_w + viz.font_size * 12
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, [0, 0])
            




            # para solo colocar 3 botones, caracteristicas suaves, duras y suaves


            imgui.same_line(round(pos0 + 50  + (pos1 - pos0) * (0 / (4 - 1))))
            if 0 == 0:
                imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3)
            with imgui_utils.grayed_out(num_ws == 0):
                _clicked, self.enables[11] = imgui.checkbox('carac. fuertes', self.enables[11])
            if imgui.is_item_hovered():
                imgui.set_tooltip(f'{11}')


            imgui.same_line(round(pos0 + (pos1 - pos0) * (1 / (3 - 1))))
            if 0 == 0:
                imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3)
            with imgui_utils.grayed_out(num_ws == 0):
                _clicked, self.enables[0] = imgui.checkbox('carac. media', self.enables[0])
            if imgui.is_item_hovered():
                imgui.set_tooltip(f'{0}')


            imgui.same_line(round(pos0-50 + (pos1 - pos0) * (2 / (3 - 1))))
            if 0 == 0:
                imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3)
            with imgui_utils.grayed_out(num_ws == 0):
                _clicked, self.enables[13] = imgui.checkbox('carac. suaves', self.enables[13])
            if imgui.is_item_hovered():
                imgui.set_tooltip(f'{13}')
            
            if (self.enables[0]  == True):
                self.enables[1] = True
                self.enables[2] = True
                self.enables[3] = True
                self.enables[4] = True
                self.enables[5] = True
                 
            else :
                self.enables[1] = False
                self.enables[2] = False
                self.enables[3] = False
                self.enables[4] = False
                if (self.enables[11]  == False):
                     self.enables[5] = False
                      
              

            if (self.enables[11]  == True):

                self.enables[5] = True
                self.enables[3] = True
                self.enables[7] = True
                self.enables[8] = True
                self.enables[9] = True
                self.enables[10] = True
 
            else :
                if (self.enables[0]  == False):
                     self.enables[5] = False
                self.enables[3] = False
                self.enables[7] = False
                self.enables[8] = False
                self.enables[9] = False
                self.enables[10] = False 



            if (self.enables[13]  == True):
                self.enables[12] = True
                self.enables[14] = True
                self.enables[15] = True
 
            else :

                self.enables[12] = False
                self.enables[14] = False
                self.enables[15] = False


            for idx in range(num_enables):
                """
                imgui.same_line(round(pos0 + (pos1 - pos0) * (idx / (num_enables - 1))))
                if idx == 0:
                    imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3)
                with imgui_utils.grayed_out(num_ws == 0):
                    _clicked, self.enables[idx] = imgui.checkbox(f'##{idx}', self.enables[idx])
                if imgui.is_item_hovered():
                    imgui.set_tooltip(f'{idx}')

               
                if (self.viz.capture_widget.contador % 100 < 50):
                    self.enables[0] = True
                    self.enables[1] = True
                    self.enables[2] = True
                    self.enables[3] = True
                    self.enables[4] = True
                    self.enables[5] = True
                    self.enables[3] = True

                    self.enables[10] = False
                    self.enables[11] = False
                    self.enables[12] = False
                    self.enables[13] = False
                else:
                    self.enables[0] = False
                    self.enables[1] = False
                    self.enables[2] = False
                    self.enables[3] = False
                    self.enables[4] = False
                    self.enables[5] = False
                    self.enables[3] = False

                    self.enables[10] = True
                    self.enables[11] = True
                    self.enables[12] = True
                    self.enables[13] = True
                """
            imgui.pop_style_var(1)

            imgui.same_line(pos2)
            imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 3)
            with imgui_utils.grayed_out(num_ws == 0):
                if imgui_utils.button('Reset', width=-1, enabled=(self.seed != self.seed_def or self.animate or any(self.enables[:num_enables]))):
                    self.seed = self.seed_def
                    self.animate = False
                    self.enables = [False] * num_enables

        self.contador = self.contador  + 1
        if any(self.enables[:num_ws]):
            viz.args.stylemix_idx = [idx for idx, enable in enumerate(self.enables) if enable]
            viz.args.stylemix_seed = self.seed & ((1 << 32) - 1)
           # viz.args.stylemix_seed_last = self.contador % 20

        
        
        
        if self.animate:
            
            if (self.contador % 10 ==0):
                self.seed += 1
        
      # viz.args.stylemix_seed_last = self.contador % 20
#----------------------------------------------------------------------------
