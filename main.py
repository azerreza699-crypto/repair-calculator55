from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase
import arabic_reshaper
import os

FONT_NAME = 'ArabicAndroidFont'

def init_arabic_font():
    android_system_fonts = [
        '/system/fonts/NotoNaskhArabic-Regular.ttf',
        '/system/fonts/NotoSansArabic-Regular.ttf',
        '/system/fonts/NotoSansArabicUI-Regular.ttf',
        '/system/fonts/DroidSansArabic.ttf'
    ]
    for font_path in android_system_fonts:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name=FONT_NAME, fn_regular=font_path)
                return FONT_NAME
            except Exception:
                pass
    return None

FONT_AR = init_arabic_font()

def ar(text):
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return reshaped[::-1]
    except Exception:
        return text

class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if FONT_AR:
            self.font_name = FONT_AR
        self.font_size = sp(13)
        self.color = (0.98, 0.98, 0.98, 1)
        self.background_normal = ''
        self.background_color = (0.16, 0.22, 0.30, 1)

class ResultCard(BoxLayout):
    def __init__(self, title, accent_color=(0.3, 0.65, 0.95, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = [dp(8), dp(4)]
        self.spacing = dp(6)
        self.size_hint_y = None
        self.height = dp(54)

        with self.canvas.before:
            Color(0.14, 0.17, 0.23, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8),])
            Color(0.22, 0.27, 0.35, 1)
            self.border = Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], dp(8)), width=dp(1))

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        accent_bar = BoxLayout(size_hint_x=None, width=dp(4))
        with accent_bar.canvas.before:
            Color(*accent_color)
            accent_bar.bar_rect = RoundedRectangle(pos=accent_bar.pos, size=accent_bar.size, radius=[dp(2),])
        accent_bar.bind(pos=lambda inst, val: setattr(accent_bar.bar_rect, 'pos', val),
                        size=lambda inst, val: setattr(accent_bar.bar_rect, 'size', val))

        text_layout = BoxLayout(orientation='vertical', spacing=dp(1))
        
        self.lbl_title = Label(
            text=ar(title),
            font_name=FONT_AR if FONT_AR else None,
            font_size=sp(10.5),
            color=(0.70, 0.76, 0.84, 1),
            halign='right',
            valign='middle'
        )
        self.lbl_title.bind(size=self.lbl_title.setter('text_size'))

        self.lbl_value = Label(
            text="0.00",
            font_name="Roboto",
            font_size=sp(14.5),
            bold=True,
            color=(0.95, 0.97, 1, 1),
            halign='right',
            valign='middle'
        )
        self.lbl_value.bind(size=self.lbl_value.setter('text_size'))

        text_layout.add_widget(self.lbl_title)
        text_layout.add_widget(self.lbl_value)

        self.add_widget(text_layout)
        self.add_widget(accent_bar)

    def _update_canvas(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
        self.border.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], dp(8))

class RepairItemCard(BoxLayout):
    def __init__(self, item_num, remove_callback, calc_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(200)
        self.padding = dp(10)
        self.calc_callback = calc_callback

        with self.canvas.before:
            Color(0.14, 0.17, 0.23, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10),])
            Color(0.22, 0.27, 0.35, 1)
            self.border = Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], dp(10)), width=dp(1))

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(6))

        btn_remove = Button(
            text="X",
            size_hint_x=None,
            width=dp(36),
            background_normal='',
            background_color=(0.85, 0.25, 0.28, 1),
            font_size=sp(14),
            bold=True,
            font_name="Roboto"
        )
        btn_remove.bind(on_press=lambda instance: remove_callback(self))
        header.add_widget(btn_remove)

        self.opt_ecran3 = ar("شاشة قسمة ثلاثة")
        self.opt_ecran2 = ar("شاشة قسمة اثنين")
        self.opt_akhar = ar("إصلاح آخر")
        self.opt_khsara2 = ar("خسارة قسمة اثنين")
        self.opt_khsara3 = ar("خسارة قسمة ثلاثة")

        self.type_spinner = Spinner(
            text=self.opt_ecran3,
            values=(
                self.opt_ecran3, 
                self.opt_ecran2, 
                self.opt_akhar, 
                self.opt_khsara2, 
                self.opt_khsara3
            ),
            font_name=FONT_AR if FONT_AR else None,
            option_cls=CustomSpinnerOption,
            size_hint_x=0.54,
            font_size=sp(12.5),
            bold=True,
            color=(0.4, 0.85, 1, 1),
            background_normal='',
            background_color=(0.11, 0.16, 0.23, 1)
        )
        self.type_spinner.bind(text=self.on_type_change)
        header.add_widget(self.type_spinner)

        header.add_widget(
            Label(
                text=f"{item_num} : " + ar("إصلاح رقم"),
                font_name=FONT_AR if FONT_AR else None,
                font_size=sp(13.5),
                bold=True,
                color=(0.35, 0.75, 1, 1),
                size_hint_x=0.36
            )
        )

        self.add_widget(header)

        self.grid = GridLayout(cols=2, spacing=dp(6), size_hint_y=None, height=dp(130))

        self.lbl_price = Label(text=ar("سعر الزبون:"), font_name=FONT_AR if FONT_AR else None, font_size=sp(13), color=(0.8, 0.85, 0.92, 1))
        self.txt_price = TextInput(font_name="Roboto", input_filter='float', multiline=False, font_size=sp(15), background_normal='', background_color=(0.08, 0.10, 0.14, 1), foreground_color=(1, 1, 1, 1), padding=[dp(8), dp(6)])
        self.txt_price.bind(text=lambda inst, val: self.calc_callback(None))

        self.lbl_dakhili = Label(text=ar("سعر بياس داخلي:"), font_name=FONT_AR if FONT_AR else None, font_size=sp(13), color=(0.8, 0.85, 0.92, 1))
        self.txt_dakhili = TextInput(font_name="Roboto", input_filter='float', multiline=False, font_size=sp(15), background_normal='', background_color=(0.08, 0.10, 0.14, 1), foreground_color=(1, 1, 1, 1), padding=[dp(8), dp(6)])
        self.txt_dakhili.bind(text=lambda inst, val: self.calc_callback(None))

        self.lbl_khariji = Label(text=ar("سعر بياس خارجي:"), font_name=FONT_AR if FONT_AR else None, font_size=sp(13), color=(0.8, 0.85, 0.92, 1))
        self.txt_khariji = TextInput(font_name="Roboto", input_filter='float', multiline=False, font_size=sp(15), background_normal='', background_color=(0.08, 0.10, 0.14, 1), foreground_color=(1, 1, 1, 1), padding=[dp(8), dp(6)])
        self.txt_khariji.bind(text=lambda inst, val: self.calc_callback(None))

        self.lbl_loss = Label(text=ar("مبلغ الخسارة:"), font_name=FONT_AR if FONT_AR else None, font_size=sp(13), color=(0.95, 0.45, 0.45, 1))
        self.txt_loss = TextInput(font_name="Roboto", input_filter='float', multiline=False, font_size=sp(15), background_normal='', background_color=(0.08, 0.10, 0.14, 1), foreground_color=(1, 1, 1, 1), padding=[dp(8), dp(6)])
        self.txt_loss.bind(text=lambda inst, val: self.calc_callback(None))

        self.add_widget(self.grid)
        self.build_inputs(is_loss=False)

    def build_inputs(self, is_loss=False):
        self.grid.clear_widgets()
        if is_loss:
            self.grid.height = dp(42)
            self.height = dp(112)
            self.grid.add_widget(self.lbl_loss)
            self.grid.add_widget(self.txt_loss)
        else:
            self.grid.height = dp(130)
            self.height = dp(200)
            self.grid.add_widget(self.lbl_price)
            self.grid.add_widget(self.txt_price)
            self.grid.add_widget(self.lbl_dakhili)
            self.grid.add_widget(self.txt_dakhili)
            self.grid.add_widget(self.lbl_khariji)
            self.grid.add_widget(self.txt_khariji)

    def on_type_change(self, spinner, text):
        is_loss = (text in (self.opt_khsara2, self.opt_khsara3))
        self.build_inputs(is_loss)
        self.calc_callback(None)

    def _update_canvas(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
        self.border.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], dp(10))

class RepairCalcApp(App):
    def build(self):
        self.title = "حاسبة الصيانة"
        self.repair_count = 0

        main_layout = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(6))
        with main_layout.canvas.before:
            Color(0.07, 0.08, 0.10, 1)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        title_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(34), spacing=dp(2))
        title_label = Label(
            text=ar("حاسبة صيانة الهواتف"),
            font_name=FONT_AR if FONT_AR else None,
            font_size=sp(19),
            bold=True,
            color=(0.35, 0.75, 1, 1)
        )
        title_box.add_widget(title_label)
        main_layout.add_widget(title_box)

        top_btn_layout = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=None, height=dp(38))

        btn_add = Button(
            text=ar("إضافة إصلاح"),
            font_name=FONT_AR if FONT_AR else None,
            background_normal='',
            background_color=(0.10, 0.65, 0.45, 1),
            font_size=sp(14),
            bold=True
        )
        btn_add.bind(on_press=self.add_repair_item)

        btn_reset = Button(
            text=ar("مسح الكل"),
            font_name=FONT_AR if FONT_AR else None,
            background_normal='',
            background_color=(0.82, 0.22, 0.25, 1),
            font_size=sp(14),
            bold=True
        )
        btn_reset.bind(on_press=self.reset_all)

        top_btn_layout.add_widget(btn_add)
        top_btn_layout.add_widget(btn_reset)
        main_layout.add_widget(top_btn_layout)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.items_container = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
        self.items_container.bind(minimum_height=self.items_container.setter('height'))
        self.scroll.add_widget(self.items_container)
        main_layout.add_widget(self.scroll)

        self.add_repair_item(None)

        btn_calc = Button(
            text=ar("حساب الكل"),
            font_name=FONT_AR if FONT_AR else None,
            size_hint_y=None,
            height=dp(42),
            background_normal='',
            background_color=(0.12, 0.48, 0.90, 1),
            font_size=sp(16),
            bold=True
        )
        btn_calc.bind(on_press=self.calculate_all)
        main_layout.add_widget(btn_calc)

        results_container = GridLayout(
            cols=2,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(174)
        )

        self.frame_dakhili = ResultCard("مجموع البياس الداخلي", accent_color=(0.35, 0.65, 0.95, 1))
        results_container.add_widget(self.frame_dakhili)

        self.frame_khariji = ResultCard("مجموع البياس الخارجي", accent_color=(0.65, 0.45, 0.95, 1))
        results_container.add_widget(self.frame_khariji)

        self.frame_total_piec = ResultCard("إجمالي قطع الغيار", accent_color=(0.55, 0.60, 0.70, 1))
        results_container.add_widget(self.frame_total_piec)

        self.frame_amil = ResultCard("فائدة العامل الإجمالية", accent_color=(0.10, 0.65, 0.45, 1))
        results_container.add_widget(self.frame_amil)

        self.frame_moulai = ResultCard("فائدة مولاي الإجمالية", accent_color=(0.12, 0.48, 0.90, 1))
        results_container.add_widget(self.frame_moulai)

        self.frame_amil_plus_piec = ResultCard("فائدة العامل والقطع", accent_color=(0.95, 0.60, 0.10, 1))
        results_container.add_widget(self.frame_amil_plus_piec)

        main_layout.add_widget(results_container)

        return main_layout

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def add_repair_item(self, instance):
        self.repair_count += 1
        item = RepairItemCard(self.repair_count, self.remove_repair_item, self.calculate_all)
        self.items_container.add_widget(item)

    def remove_repair_item(self, item_widget):
        if len(self.items_container.children) > 1:
            self.items_container.remove_widget(item_widget)
        else:
            item_widget.txt_price.text = ""
            item_widget.txt_dakhili.text = ""
            item_widget.txt_khariji.text = ""
            item_widget.txt_loss.text = ""
        self.calculate_all(None)

    def reset_all(self, instance):
        self.items_container.clear_widgets()
        self.repair_count = 0
        self.add_repair_item(None)

        self.frame_dakhili.lbl_value.text = "0.00"
        self.frame_khariji.lbl_value.text = "0.00"
        self.frame_total_piec.lbl_value.text = "0.00"
        self.frame_amil.lbl_value.text = "0.00"
        self.frame_moulai.lbl_value.text = "0.00"
        self.frame_amil_plus_piec.lbl_value.text = "0.00"

    def calculate_all(self, instance):
        total_dakhili = 0.0
        total_khariji = 0.0
        total_faida_moulai = 0.0
        total_faida_amil = 0.0

        for item in self.items_container.children:
            try:
                rep_type = item.type_spinner.text
                is_loss = (rep_type in (item.opt_khsara2, item.opt_khsara3))

                if is_loss:
                    loss_val = float(item.txt_loss.text) if item.txt_loss.text else 0.0
                    dakhili = 0.0
                    khariji = 0.0
                    faida_item = -loss_val
                else:
                    price = float(item.txt_price.text) if item.txt_price.text else 0.0
                    dakhili = float(item.txt_dakhili.text) if item.txt_dakhili.text else 0.0
                    khariji = float(item.txt_khariji.text) if item.txt_khariji.text else 0.0
                    faida_item = price - (dakhili + khariji)

                if rep_type == item.opt_ecran3 or rep_type == item.opt_khsara3:
                    moulai_item = (faida_item * 2.0) / 3.0
                    amil_item = faida_item / 3.0
                else:
                    moulai_item = faida_item / 2.0
                    amil_item = faida_item / 2.0

                total_dakhili += dakhili
                total_khariji += khariji
                total_faida_moulai += moulai_item
                total_faida_amil += amil_item

            except ValueError:
                pass

        total_piec = total_dakhili + total_khariji
        amil_plus_piec = total_faida_amil + total_piec

        self.frame_dakhili.lbl_value.text = f"{total_dakhili:,.2f}"
        self.frame_khariji.lbl_value.text = f"{total_khariji:,.2f}"
        self.frame_total_piec.lbl_value.text = f"{total_piec:,.2f}"
        self.frame_amil.lbl_value.text = f"{total_faida_amil:,.2f}"
        self.frame_moulai.lbl_value.text = f"{total_faida_moulai:,.2f}"
        self.frame_amil_plus_piec.lbl_value.text = f"{amil_plus_piec:,.2f}"

if __name__ == "__main__":
    RepairCalcApp().run()
      
