import thorpy
import pygame
from devices import Devices
from config import Config
from time import sleep
import os
from threading import Timer
from thorpy._utils.images import load_image
from thorpy.painting.painters.imageframe import ButtonImage

PROBE_EVENT = pygame.USEREVENT + 1
ACTION_EVENT = pygame.USEREVENT + 2

class MyThorpyApp(thorpy.Application):
    def __init__(self, size, caption=None, icon="thorpy", center=True, flags=0):
        global _SCREEN, _CURRENT_APPLICATION
        _CURRENT_APPLICATION = self
        self.size = tuple(size)
        self.caption = caption
        pygame.init()
        if center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.set_icon(icon)
        # w,h = pygame.display.set_mode((0,0),pygame.FULLSCREEN).get_size()
        # self.max_screen_size = (w,h)
        screen = pygame.display.set_mode(self.size, flags)
        if self.caption:
            pygame.display.set_caption(caption)
        _SCREEN = screen
        self.default_path = "./"

class Container(thorpy.Ghost):
    def set_visible(self, value):
        for elem in self.get_elements():
            elem.set_visible(value)
            elem.set_active(value)

class Selector(Container):

    def __init__(self, x, y, title, values, format, btn_plus, btn_minus, updater=None, cyclic=False):
        super().__init__()
        painter = thorpy.painters.basicframe.BasicFrame(color=(255, 255, 255))
        self.elem1 = thorpy.Element(title)
        self.elem1.set_painter(painter)
        self.elem1.set_size((120, 30), margins=(0,0))
        self.elem1.set_font_size(14)
        self.elem1.set_center_pos((60 + 120 * x, 40 + 80 * y - 12))
        self.elem2 = thorpy.Element(format)
        self.elem2.set_painter(painter)
        self.elem2.set_size((120, 30), margins=(0,0))
        self.elem2.set_font_size(18)
        self.elem2.set_center_pos((60 + 120 * x, 40 + 80 * y + 12))
        self.add_elements([self.elem1, self.elem2])
        self.updater = None
        self.values = values
        self.value = 0
        self.format = format
        self.value_index = 0
        self.show_value()
        self.updater = updater
        self.cyclic = cyclic
        if btn_plus:
            btn_plus.user_func = self.next_value
        if btn_minus:
            btn_minus.user_func = self.prev_value

    def show_value(self):
        if self.values:
            val = self.values[self.value_index]
        else:
            val = self.value
        if type(val) == tuple:
            str = self.format.format(*val)
        else:
            str = self.format.format(val)
        self.elem2.set_text(str)
        self.elem1.unblit_and_reblit()
        self.elem2.unblit_and_reblit()
        if self.updater is not None:
            self.updater()

    def next_value(self):
        self.value_index += 1
        if self.value_index >= len(self.values):
            if self.cyclic:
                self.value_index = 0
            else:
                self.value_index = len(self.values) - 1
        self.show_value()

    def prev_value(self):
        self.value_index -= 1
        if self.value_index < 0:
            if self.cyclic:
                self.value_index = len(self.values) - 1
            else:
                self.value_index = 0
        self.show_value()

    def get_value(self):
        if self.values:
            val = self.values[self.value_index]
        else:
            val = self.value
        return val

    def set_value(self, value):
        if self.values:
            idx = self.values.index(value)
            if idx >= 0:
                self.value_index = idx
        else:
            self.value = value
        self.show_value()

class Switch():

    def __init__(self, btn_on, btn_off, updater=None):
        self.updater = None
        self.btn_on = btn_on
        self.btn_on.user_func = self.on_click
        self.btn_off = btn_off
        self.btn_off.user_func = self.off_click
        self.set_value(False)
        self.updater = updater

    def set_value(self, value):
        if value:
            self.btn_on._press()
            self.btn_off._force_unpress()
            self.btn_off.unblit_and_reblit()
        else:
            self.btn_on._force_unpress()
            self.btn_on.unblit_and_reblit()
            self.btn_off._press()

    def get_value(self):
        return self.btn_on.toggled

    def on_click(self):
        self.btn_off._force_unpress()
        self.btn_off.unblit_and_reblit()
        if self.updater is not None:
            self.updater()

    def off_click(self):
        self.btn_on._force_unpress()
        self.btn_on.unblit_and_reblit()
        if self.updater is not None:
            self.updater()

class Controller:

    def button(self, x, y, title, callback=None, togglable=False):
        try:
            painter = thorpy.painters.imageframe.ButtonImage(
                img_normal=os.path.join('imgs', '%s_normal.png' % title.lower()),
                img_pressed=os.path.join('imgs', '%s_pressed.png' % title.lower())
            )
        except:
            painter = thorpy.painters.imageframe.ButtonImage(
                img_normal=os.path.join('imgs', '%s_normal.png' % 'default'),
                img_pressed=os.path.join('imgs', '%s_pressed.png' % 'default')
            )
        try:
            inactive_painter = thorpy.painters.imageframe.ButtonImage(
                img_normal=os.path.join('imgs', '%s_inactive.png' % title.lower())
            )
        except:
            inactive_painter = thorpy.painters.imageframe.ButtonImage(
                img_normal=os.path.join('imgs', '%s_inactive.png' % 'default')
            )
        if togglable:
            btn = thorpy.Togglable('')
        else:
            btn = thorpy.Clickable('')
        btn.normal_painter = painter
        btn.inactive_painter = inactive_painter
        btn.set_painter(painter)
        btn.user_func = callback
        btn.finish()
        btn.set_center_pos((60 + 120 * x, 40 + 80 * y))
        return btn
        thorpy.make_image_button()

    def activate(self, elem):
        if not elem.active:
            elem.set_active(True)
            elem.change_painter(elem.normal_painter, autopress=False)
            elem.unblit_and_reblit()

    def deactivate(self, elem):
        if elem.active:
            elem.set_active(False)
            elem.change_painter(elem.inactive_painter, autopress=False)
            elem.unblit_and_reblit()

    def __init__(self):
        self.in_load = False
        self.app = MyThorpyApp(size=(480, 320), caption="EMDR Controller", icon='pygame')
        self.btn_start = self.button(0, 0, 'Play', self.start_click)
        self.btn_start24 = self.button(1, 0, 'Play24', self.start24_click)
        self.btn_stop = self.button(2, 0, 'Stop', self.stop_click)
        self.btn_pause = self.button(3, 0, 'Pause', self.pause_click, togglable=True)
        self.btn_lightbar = self.button(0, 1, 'Light', self.lightbar_click, togglable=True)
        self.btn_buzzer = self.button(0, 2, 'Buzzer', self.buzzer_click, togglable=True)
        self.btn_headphone = self.button(0, 3, 'Sound', self.headphone_click, togglable=True)
        # speed area
        self.sel_counter = Selector(2, 1, 'Zähler', None, '{0:d}', None, None)
        self.sel_counter.set_value(0)
        self.btn_speed_plus = self.button(1, 2, '+')
        self.btn_speed_minus = self.button(3, 2, '-')
        self.sel_speed = Selector(2, 2, 'Geschwindigk.', Config.speeds, '{0:d}/min', self.btn_speed_plus, self.btn_speed_minus, self.update_speed)
        self.box_speed = Container(elements=[
            self.sel_counter,
            self.btn_speed_plus,
            self.sel_speed,
            self.btn_speed_minus,
        ])
        # lightbar area
        self.btn_light_on = self.button(1, 1, 'On', togglable=True)
        self.btn_light_off = self.button(2, 1, 'Off', togglable=True)
        self.switch_light = Switch(self.btn_light_on, self.btn_light_off, self.update_light)
        self.btn_light_test = self.button(3, 1, 'Test', self.light_test_click, togglable=True)
        self.btn_light_color_plus = self.button(1, 2, '+')
        self.btn_light_color_minus = self.button(3, 2, '-')
        self.sel_light_color = Selector(2, 2, 'Farbe', Config.colors, '{0}', self.btn_light_color_plus, self.btn_light_color_minus, self.update_light, cyclic=True)
        self.btn_light_intens_plus = self.button(1, 3, '+')
        self.btn_light_intens_minus = self.button(3, 3, '-')
        self.sel_light_intens = Selector(2, 3, 'Helligkeit', Config.intensities, '{0:d}%', self.btn_light_intens_plus, self.btn_light_intens_minus, self.update_light)
        self.box_lightbar = Container(elements=[
            self.btn_light_on,
            self.btn_light_off,
            self.btn_light_test,
            self.btn_light_color_plus,
            self.sel_light_color,
            self.btn_light_color_minus,
            self.btn_light_intens_plus,
            self.sel_light_intens,
            self.btn_light_intens_minus,
        ])
        # buzzer area
        self.btn_buzzer_on = self.button(1, 1, 'On', togglable=True)
        self.btn_buzzer_off = self.button(2, 1, 'Off', togglable=True)
        self.switch_buzzer = Switch(self.btn_buzzer_on, self.btn_buzzer_off, self.update_buzzer)
        self.btn_buzzer_test = self.button(3, 1, 'Test', self.buzzer_test_click)
        self.btn_buzzer_duration_plus = self.button(1, 2, '+')
        self.btn_buzzer_duration_minus = self.button(3, 2, '-')
        self.sel_buzzer_duration = Selector(2, 2, 'Dauer', Config.durations, '{0:d} ms', self.btn_buzzer_duration_plus, self.btn_buzzer_duration_minus, self.update_buzzer)
        self.box_buzzer = Container(elements=[
            self.btn_buzzer_on,
            self.btn_buzzer_off,
            self.btn_buzzer_test,
            self.btn_buzzer_duration_plus,
            self.sel_buzzer_duration,
            self.btn_buzzer_duration_minus,
        ])
        # headphone area
        self.btn_headphone_on = self.button(1, 1, 'On', togglable=True)
        self.btn_headphone_off = self.button(2, 1, 'Off', togglable=True)
        self.switch_headphone = Switch(self.btn_headphone_on, self.btn_headphone_off, self.update_sound)
        self.btn_headphone_test = self.button(3, 1, 'Test', self.headphone_test_click)
        self.btn_headphone_volume_plus = self.button(1, 2, '+')
        self.btn_headphone_volume_minus = self.button(3, 2, '-')
        self.sel_headphone_volume = Selector(2, 2, 'Lautstärke', Config.volumes, '{0:d}%', self.btn_headphone_volume_plus, self.btn_headphone_volume_minus, self.update_sound)
        self.btn_headphone_tone_plus = self.button(1, 3, '+')
        self.btn_headphone_tone_minus = self.button(3, 3, '-')
        self.sel_headphone_tone = Selector(2, 3, 'Ton', Config.tones, '{0}', self.btn_headphone_tone_plus, self.btn_headphone_tone_minus, self.update_sound, cyclic=True)
        self.box_headphone = Container(elements=[
            self.btn_headphone_on,
            self.btn_headphone_off,
            self.btn_headphone_test,
            self.btn_headphone_volume_plus,
            self.sel_headphone_volume,
            self.btn_headphone_volume_minus,
            self.btn_headphone_tone_plus,
            self.sel_headphone_tone,
            self.btn_headphone_tone_minus,
        ])
        #
        self.back = thorpy.Background.make((255, 255, 255), elements=[
            self.btn_start,
            self.btn_start24,
            self.btn_stop,
            self.btn_pause,
            self.btn_lightbar,
            self.btn_buzzer,
            self.btn_headphone,
            self.box_speed,
            self.box_lightbar,
            self.box_buzzer,
            self.box_headphone,
        ])
        self.back.add_reaction(thorpy.Reaction(reacts_to=PROBE_EVENT, reac_func=self.check_usb))
        self.back.add_reaction(thorpy.Reaction(reacts_to=ACTION_EVENT, reac_func=self.action))
        self.menu = thorpy.Menu(self.back)
        self.config_mode()
        self.check_usb(None)
        self.reset_action()

    def lightbar_click(self):
        if self.btn_lightbar.toggled:
            self.set_area('lightbar')
        else:
            self.set_area('speed')

    def light_intense_plus_click(self):
        self.sel_light_intens.next_value()

    def light_intense_minus_click(self):
        self.sel_light_intens.prev_value()

    def buzzer_click(self):
        if self.btn_buzzer.toggled:
            self.set_area('buzzer')
        else:
            self.set_area('speed')

    def headphone_click(self):
        if self.btn_headphone.toggled:
            self.set_area('headphone')
        else:
            self.set_area('speed')

    def light_test_click(self):
        self.update_light()
        if self.btn_light_test.toggled:
            Devices.set_led(-1)
        else:
            Devices.set_led(0)

    def buzzer_test_click(self):
        self.update_buzzer()
        Devices.do_buzzer(True)
        sleep(1 + self.sel_buzzer_duration.get_value() / 1000)
        Devices.do_buzzer(False)

    def headphone_test_click(self):
        self.update_sound()
        Devices.do_sound(True)
        sleep(1)
        Devices.do_sound(False)

    def update_light(self):
        (color_name, r, g, b) = self.sel_light_color.get_value()
        intensity = self.sel_light_intens.get_value() / 100 * 0.7 # max. 70 % intensity
        r = round(r * intensity)
        g = round(g * intensity)
        b = round(b * intensity)
        color = r * 256 * 256 + g * 256 + b
        Devices.set_color(color)
        if self.btn_light_test.toggled:
            Devices.set_led(-1)
        if self.mode == 'action' and not self.switch_light.get_value():
            Devices.set_led(0)
        self.save_config()

    def update_buzzer(self):
        duration = self.sel_buzzer_duration.get_value()
        Devices.set_buzzer_duration(duration)
        self.save_config()

    def update_sound(self):
        (tone_name, frequency, duration) = self.sel_headphone_tone.get_value()
        volume = self.sel_headphone_volume.get_value() / 100
        Devices.set_tone(frequency, duration, volume)
        self.save_config()

    def update_speed(self):
        self.save_config()
        if self.mode == 'action':
            self.adjust_action_timer()

    def set_area(self, area):
        self.box_speed.set_visible(area == 'speed')
        self.box_lightbar.set_visible(area == 'lightbar')
        self.box_buzzer.set_visible(area == 'buzzer')
        self.box_headphone.set_visible(area == 'headphone')
        if self.btn_lightbar.toggled and area != 'lightbar':
            self.btn_lightbar._force_unpress()
        if self.btn_buzzer.toggled and area != 'buzzer':
            self.btn_buzzer._force_unpress()
        if self.btn_headphone.toggled and area != 'headphone':
            self.btn_headphone._force_unpress()
        if area != 'lightbar' and self.btn_light_test.toggled:
            self.btn_light_test._force_unpress()
            self.light_test_click()
        self.back.unblit_and_reblit()

    def load_config(self):
        try:
            self.in_load = True
            Config.load()
            self.sel_speed.set_value(Config.data.get('general.speed'))
            self.switch_light.set_value(Config.data.get('lightbar.on'))
            self.sel_light_color.set_value(Config.data.get('lightbar.color'))
            self.sel_light_intens.set_value(Config.data.get('lightbar.intensity'))
            self.switch_buzzer.set_value(Config.data.get('buzzer.on'))
            self.sel_buzzer_duration.set_value(Config.data.get('buzzer.duration'))
            self.switch_headphone.set_value(Config.data.get('headphone.on'))
            self.sel_headphone_tone.set_value(Config.data.get('headphone.tone'))
            self.sel_headphone_volume.set_value(Config.data.get('headphone.volume'))
        except:
            # do not crash with corrupt config file
            # it will be properly written on close
            pass
        self.in_load = False

    def save_config(self):
        if not self.in_load:
            Config.data['general.speed'] = self.sel_speed.get_value()
            Config.data['lightbar.on'] = self.switch_light.get_value()
            Config.data['lightbar.color'] = self.sel_light_color.get_value()
            Config.data['lightbar.intensity'] = self.sel_light_intens.get_value()
            Config.data['buzzer.on'] = self.switch_buzzer.get_value()
            Config.data['buzzer.duration'] = self.sel_buzzer_duration.get_value()
            Config.data['headphone.on'] = self.switch_headphone.get_value()
            Config.data['headphone.tone'] = self.sel_headphone_tone.get_value()
            Config.data['headphone.volume'] = self.sel_headphone_volume.get_value()
            Config.save()

    def config_mode(self):
        self.mode = 'config'
        # no need to disable action timer, since it is a one-shot-timer
        # enable periodic probing
        pygame.time.set_timer(PROBE_EVENT, 1000)
        # enable/disable buttons
        self.activate(self.btn_start)
        self.activate(self.btn_start24)
        if not self.btn_pause.toggled:
            self.deactivate(self.btn_stop)
            self.deactivate(self.btn_pause)

    def post_action(self):
        if self.mode == 'action':
            event = pygame.event.Event(ACTION_EVENT)
            try:
                pygame.event.post(event)
            except:
                # cath pygame error in case of overfull event pipe
                pass
            Timer(self.action_delay, self.post_action).start()

    def adjust_action_timer(self):
        # use python threading timer instead of pygame timer due to bad resolution of pygame timer
        # (typical 10ms)
        self.action_delay = (60 / self.sel_speed.get_value() / Devices.led_num / 2)

    def action_mode(self):
        self.mode = 'action'
        # disable periodic probing
        pygame.time.set_timer(PROBE_EVENT, 0)
        # prepare devices
        Devices.set_led(0)
        self.update_light()
        self.update_buzzer()
        self.update_sound()
        # enable action timer
        self.adjust_action_timer()
        Timer(self.action_delay, self.post_action).start()
        # enable/disable buttons
        self.deactivate(self.btn_start)
        self.deactivate(self.btn_start24)
        self.activate(self.btn_stop)
        self.activate(self.btn_pause)

    def run(self):
        self.load_config()
        self.set_area('speed')
        self.menu.play()
        self.save_config()
        Devices.set_led(0)
        self.app.quit()

    def start_click(self):
        self.set_area('speed')
        self.max_counter = 0
        self.reset_action()
        self.action_mode()

    def start24_click(self):
        self.set_area('speed')
        self.max_counter = 24
        self.reset_action()
        self.action_mode()

    def stop_click(self):
        self.config_mode()
        self.reset_action()

    def pause_click(self):
        if self.btn_pause.toggled:
            self.config_mode()
        else:
            self.action_mode()

    def check_usb(self, event):
        if self.mode == 'action':
            return
        Devices.probe()
        if Devices.buzzer_plugged_in():
            self.activate(self.btn_buzzer)
        else:
            self.deactivate(self.btn_buzzer)
        if Devices.lightbar_plugged_in():
            self.activate(self.btn_lightbar)
        else:
            self.deactivate(self.btn_lightbar)

    def reset_action(self):
        self.led_pos = 1
        self.direction = 1
        self.sel_counter.set_value(0)
        Devices.set_led(0)
        self.btn_pause._force_unpress()
        self.btn_pause.unblit_and_reblit()

    def action(self, event):
        if self.mode != 'action':
            return
        if self.switch_light.get_value():
            Devices.set_led(self.led_pos)
        if self.led_pos == 1:
            cntr = self.sel_counter.get_value() + 1
            self.sel_counter.set_value(cntr)
            if self.switch_buzzer.get_value():
                Devices.do_buzzer(True)
            if self.switch_headphone.get_value():
                Devices.do_sound(True)
            if self.direction == -1:
                self.direction = 1
            if cntr == self.max_counter:
                self.stop_click()
        if self.led_pos == Devices.led_num:
            if self.switch_buzzer.get_value():
                Devices.do_buzzer(False)
            if self.switch_headphone.get_value():
                Devices.do_sound(False)
            if self.direction == 1:
                self.direction = -1
        self.led_pos += self.direction


def main():
    controller = Controller()
    controller.run()

if __name__ == '__main__':
    main()