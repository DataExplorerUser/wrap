from wrap import RectWrappingCollection
import dearpygui.dearpygui as dpg
import random
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

dpg.create_context()

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
       "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip " \
       "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu " \
       "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt " \
       "mollit anim id est laborum."

txt_values = text.split(' ')
txt_values = [i for i in txt_values[:-1]] + [txt_values[-1]]

ta = [RectWrappingCollection(text_align=0)]

with dpg.font_registry():
    f_font0 = dpg.add_font("whitneylight.otf", 45, tag="f_45")
    f_font1 = dpg.add_font("firaCode-medium.ttf", 35, tag="f_28")
    f_font2 = dpg.add_font("whitneylight.otf", 30, tag="f_30")

dpg.create_viewport()

with dpg.window(width=640, height=800) as main:
    with dpg.group() as g:
        def update_pos(widget):
            pos = list(ta[0].get_sizes())

            offset_x, offset_y = dpg.get_item_pos(widget)
            for i, rect in enumerate(dpg.get_item_children(widget, 1)):
                x, y = pos[i]
                dpg.set_item_pos(rect, (offset_x + x, offset_y + y))


        def set_wrap(value, widget):
            dpg.set_value('w0', value)
            ta[0].set_wrap(value)
            update_pos(widget)


        def set_line_fixed_height(value, widget):
            dpg.set_value('w_line_fixed_height_text', value if value != 0 else '(auto/adaptive)')
            ta[0].set_line_fixed_height(value)
            update_pos(widget)


        def set_line_height(value, widget):
            ta[0].set_line_height(value)
            update_pos(widget)


        def set_align(value, widget):
            values = {'left': 0, 'center': 1, 'right': 2, 'justified': 3}
            ta[0].set_align(values[value])
            update_pos(widget)


        w_wrap_control = dpg.add_drag_float(
            label="wrap width",
            default_value=800,
            max_value=1200,
            callback=lambda s, a, u: set_wrap(a, 'rich_container')
        )

        dpg.bind_item_font(w_wrap_control, f_font2)

        w_line_fixed_height_control = dpg.add_drag_float(
            label="line fixed height (px)",
            default_value=44,
            max_value=80,
            speed=0.5,
            callback=lambda s, a, u: set_line_fixed_height(a, 'rich_container')
        )
        w_line_fixed_height_text = dpg.add_text(dpg.get_value(w_line_fixed_height_control),
                                                tag='w_line_fixed_height_text')
        dpg.bind_item_font(w_line_fixed_height_control, f_font2)

        dpg.bind_item_font(w_line_fixed_height_text, f_font2)

        w_align_control = dpg.add_radio_button(
            ("left", "center", "right", "justified"),
            label="align",
            default_value="left",
            callback=lambda s, a, u: set_align(a, 'rich_container'),
            horizontal=True,
        )
        dpg.bind_item_font(w_align_control, f_font2)

        with dpg.group(tag='rich_container') as rich_container:
            last_font = None

            # Everything below is random play adding widgets, looping from the word list
            for i, word in enumerate(txt_values):
                random.seed(i)
                font = f_font0 if random.randint(0, 10) % 10 else f_font1

                color = None
                if font != last_font:
                    last_font = font
                    color = (random.randint(150, 255), random.randint(50, 255), random.randint(0, 255), 255)
                text_widget = dpg.add_text(
                    word,
                    pos=(0, 0),
                    parent=rich_container,
                    tag=f'ft_{i}',
                    color=color,

                )
                if font:
                    dpg.bind_item_font(text_widget, font)

                # Just a callback for the button
                def update_both():
                    set_align('justified', 'rich_container')
                    dpg.set_value(w_align_control, 'justified')


                # Adding a button
                if i == 15:
                    dpg.add_button(
                        label="Click me",
                        callback=update_both,
                    )


            # /

            # add_rects loops the cointainer children, reading their sizes and 'mapping' their stack index when its added
            def add_rects():
                for i, widget in enumerate(dpg.get_item_children(rich_container, 1)):
                    if dpg.get_item_type(widget) == 'mvAppItemType::mvText':
                        font = dpg.get_item_font(widget)
                        ta[0].add_rect(
                            *dpg.get_text_size(
                                dpg.get_value(widget),
                                font=font
                            )
                        )
                    else:
                        ta[0].add_rect(*dpg.get_item_rect_size(widget))
                set_wrap(dpg.get_value(w_wrap_control), 'rich_container')
                set_line_fixed_height(dpg.get_value(w_line_fixed_height_control), 'rich_container')
                set_align(dpg.get_value(w_align_control), 'rich_container')

            dpg.set_frame_callback(3, add_rects)

        w0 = dpg.add_text(dpg.get_value(w_wrap_control), tag='w0')

dpg.set_primary_window(window=main, value=True)
dpg.set_viewport_width(1300)
dpg.set_viewport_height(1000)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()
dpg.destroy_context()