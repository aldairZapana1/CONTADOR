from collections import defaultdict
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# Fondo gris claro
Window.clearcolor = (0.95, 0.95, 0.95, 1)
Window.size = (400, 680)


class CustomButton(Button):
    """Botón con estilo para pantalla táctil"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0.85, 0.85, 0.85, 1)
        self.color = (0, 0, 0, 1)
        self.bold = True


# ==========================================
# PANTALLA 1: INGRESO DE DATOS
# ==========================================
class PantallaIngreso(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(
            orientation="vertical", padding=10, spacing=8
        )

        # 1. Cabecera (Número de pallet + Título)
        frame_top = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=45, spacing=8
        )

        self.lbl_num_pallet = Label(
            text="1", font_size="22sp", bold=True, color=(0, 0, 0, 1), size_hint_x=0.2
        )

        lbl_titulo = Label(
            text="pallet palta", font_size="20sp", bold=True, color=(0, 0, 0, 1)
        )

        frame_top.add_widget(self.lbl_num_pallet)
        frame_top.add_widget(lbl_titulo)
        main_layout.add_widget(frame_top)

        # 2. Entradas Lote y Calibre
        grid_inputs = GridLayout(
            cols=2, size_hint_y=None, height=120, spacing=8, row_default_height=50
        )

        lbl_lote = Label(
            text="lote:", font_size="20sp", bold=True, color=(0, 0, 0, 1), size_hint_x=0.35
        )

        self.txt_lote = TextInput(
            font_size="20sp", multiline=False, padding_y=[10, 10], write_tab=False
        )
        self.txt_lote.bind(focus=self.on_focus_lote)

        lbl_calibre = Label(
            text="calibre:", font_size="20sp", bold=True, color=(0, 0, 0, 1), size_hint_x=0.35
        )

        self.txt_calibre = TextInput(
            font_size="20sp", multiline=False, padding_y=[10, 10], write_tab=False
        )
        self.txt_calibre.bind(focus=self.on_focus_calibre)

        grid_inputs.add_widget(lbl_lote)
        grid_inputs.add_widget(self.txt_lote)
        grid_inputs.add_widget(lbl_calibre)
        grid_inputs.add_widget(self.txt_calibre)
        main_layout.add_widget(grid_inputs)

        self.campo_activo = "lote"

        # 3. Contadores
        frame_info = BoxLayout(
            orientation="vertical", size_hint_y=None, height=40, spacing=2
        )

        self.lbl_lotes_guardados = Label(
            text="lotes guardados:0",
            font_size="13sp",
            bold=True,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        self.lbl_lotes_guardados.bind(size=self.lbl_lotes_guardados.setter("text_size"))

        self.lbl_pallets_guardados = Label(
            text="pallets guardados:0",
            font_size="13sp",
            bold=True,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        self.lbl_pallets_guardados.bind(size=self.lbl_pallets_guardados.setter("text_size"))

        frame_info.add_widget(self.lbl_lotes_guardados)
        frame_info.add_widget(self.lbl_pallets_guardados)
        main_layout.add_widget(frame_info)

        # 4. Botón VER RESUMEN
        frame_resumen = BoxLayout(size_hint_y=None, height=35, orientation="horizontal")
        frame_resumen.add_widget(BoxLayout())

        btn_ver_resumen = CustomButton(text="VER RESUMEN", font_size="12sp", size_hint_x=0.45)
        btn_ver_resumen.bind(on_release=self.ir_a_resumen)
        frame_resumen.add_widget(btn_ver_resumen)

        main_layout.add_widget(frame_resumen)

        # 5. TECLADO Y ACCIONES TOTALMENTE SIMÉTRICO
        frame_teclado_panel = BoxLayout(orientation="horizontal", spacing=4, size_hint_y=1)

        # A) Matriz Numérica de 3 Columnas puras (4 filas x 3 columnas)
        grid_numeros = GridLayout(cols=3, spacing=4, size_hint_x=0.72)

        # Creamos los 12 botones del bloque del teclado de forma directa
        b1 = CustomButton(text="1", font_size="22sp")
        b1.bind(on_release=lambda x: self.presionar_numero("1"))
        b2 = CustomButton(text="2", font_size="22sp")
        b2.bind(on_release=lambda x: self.presionar_numero("2"))
        b3 = CustomButton(text="3", font_size="22sp")
        b3.bind(on_release=lambda x: self.presionar_numero("3"))

        b4 = CustomButton(text="4", font_size="22sp")
        b4.bind(on_release=lambda x: self.presionar_numero("4"))
        b5 = CustomButton(text="5", font_size="22sp")
        b5.bind(on_release=lambda x: self.presionar_numero("5"))
        b6 = CustomButton(text="6", font_size="22sp")
        b6.bind(on_release=lambda x: self.presionar_numero("6"))

        b7 = CustomButton(text="7", font_size="22sp")
        b7.bind(on_release=lambda x: self.presionar_numero("7"))
        b8 = CustomButton(text="8", font_size="22sp")
        b8.bind(on_release=lambda x: self.presionar_numero("8"))
        b9 = CustomButton(text="9", font_size="22sp")
        b9.bind(on_release=lambda x: self.presionar_numero("9"))

        b0 = CustomButton(text="0", font_size="22sp")
        b0.bind(on_release=lambda x: self.presionar_numero("0"))

        btn_borrar = CustomButton(text="Borrar", font_size="16sp")
        btn_borrar.bind(on_release=self.presionar_borrar)

        # Celda invisible para mantener el grid perfecto de 4x3 sin deformaciones
        vacio = Label()

        # Añadimos al GridLayout en orden perfecto
        grid_numeros.add_widget(b1)
        grid_numeros.add_widget(b2)
        grid_numeros.add_widget(b3)

        grid_numeros.add_widget(b4)
        grid_numeros.add_widget(b5)
        grid_numeros.add_widget(b6)

        grid_numeros.add_widget(b7)
        grid_numeros.add_widget(b8)
        grid_numeros.add_widget(b9)

        grid_numeros.add_widget(b0)
        grid_numeros.add_widget(btn_borrar)
        grid_numeros.add_widget(vacio)  # Rellena la última casilla para que '0' y 'Borrar' midan idéntico al 1,2,3

        # B) Columna de acciones (Guardar y Consolidar Pallet)
        col_acciones = BoxLayout(orientation="vertical", spacing=4, size_hint_x=0.28)

        btn_guardar = CustomButton(text="guardar", font_size="16sp")
        btn_guardar.bind(on_release=self.guardar_item)

        btn_consolidar = CustomButton(
            text="consolidar\npallet", font_size="14sp", halign="center"
        )
        btn_consolidar.bind(on_release=self.consolidar_pallet)

        col_acciones.add_widget(btn_guardar)
        col_acciones.add_widget(btn_consolidar)

        frame_teclado_panel.add_widget(grid_numeros)
        frame_teclado_panel.add_widget(col_acciones)

        main_layout.add_widget(frame_teclado_panel)
        self.add_widget(main_layout)

    # --- LÓGICA DE TECLADO Y ACCIONES ---

    def on_focus_lote(self, instance, value):
        if value:
            self.campo_activo = "lote"

    def on_focus_calibre(self, instance, value):
        if value:
            self.campo_activo = "calibre"

    def presionar_numero(self, num):
        if self.campo_activo == "lote":
            self.txt_lote.text += num
        else:
            self.txt_calibre.text += num

    def presionar_borrar(self, instance):
        if self.campo_activo == "lote":
            self.txt_lote.text = self.txt_lote.text[:-1]
        else:
            self.txt_calibre.text = self.txt_calibre.text[:-1]

    def guardar_item(self, instance):
        app = App.get_running_app()
        lote = self.txt_lote.text.strip()
        calibre = self.txt_calibre.text.strip()

        if not lote or not calibre:
            self.mostrar_alerta("Atención", "Por favor ingrese el Lote y el Calibre.")
            return

        encontrado = False
        for item in app.pallet_actual_items:
            if item["lote"] == lote and item["calibre"] == calibre:
                item["cantidad"] += 1
                encontrado = True
                break

        if not encontrado:
            app.pallet_actual_items.append({"lote": lote, "calibre": calibre, "cantidad": 1})

        self.txt_lote.text = ""
        self.txt_calibre.text = ""
        self.txt_lote.focus = True
        self.actualizar_contadores()

    def consolidar_pallet(self, instance):
        app = App.get_running_app()
        if not app.pallet_actual_items:
            self.mostrar_alerta("Atención", "No hay datos ingresados en el pallet actual.")
            return

        app.informe_pallets[app.numero_pallet] = list(app.pallet_actual_items)
        app.numero_pallet += 1
        self.lbl_num_pallet.text = str(app.numero_pallet)
        app.pallet_actual_items.clear()

        self.txt_lote.text = ""
        self.txt_calibre.text = ""
        self.txt_lote.focus = True
        self.actualizar_contadores()

    def ir_a_resumen(self, instance):
        app = App.get_running_app()
        if not app.informe_pallets and not app.pallet_actual_items:
            self.mostrar_alerta("Atención", "No hay datos registrados para generar el resumen.")
            return

        app.resumen_generado = True
        self.manager.get_screen("resumen").actualizar_vista_informe()
        self.manager.current = "resumen"

    def actualizar_contadores(self):
        app = App.get_running_app()
        total_cajas = sum(
            item["cantidad"] for items in app.informe_pallets.values() for item in items
        ) + sum(item["cantidad"] for item in app.pallet_actual_items)

        tot_pallets = len(app.informe_pallets)
        self.lbl_lotes_guardados.text = f"lotes guardados:{total_cajas}"
        self.lbl_pallets_guardados.text = f"pallets guardados:{tot_pallets}"

    def mostrar_alerta(self, titulo, mensaje):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=mensaje, font_size="14sp", color=(1, 1, 1, 1)))
        btn_ok = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(btn_ok)

        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.3), auto_dismiss=False)
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()


# ==========================================
# PANTALLA 2: INFORME Y RESUMEN
# ==========================================
class PantallaResumen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.lbl_informe_titulo = Label(
            text="informe 1",
            font_size="20sp",
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=35,
        )
        layout.add_widget(self.lbl_informe_titulo)

        scroll = ScrollView(size_hint=(1, 1))
        self.txt_reporte = Label(
            text="",
            font_size="14sp",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            halign="left",
            valign="top",
        )
        self.txt_reporte.bind(
            texture_size=lambda instance, value: setattr(instance, "height", value[1])
        )
        self.txt_reporte.bind(
            width=lambda instance, value: setattr(instance, "text_size", (value, None))
        )

        scroll.add_widget(self.txt_reporte)
        layout.add_widget(scroll)

        frame_bot = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=45, spacing=10
        )

        btn_regresar = CustomButton(text="REGRESAR", font_size="14sp")
        btn_regresar.bind(on_release=lambda x: setattr(self.manager, "current", "ingreso"))

        btn_nuevo = CustomButton(text="comenzar nuevo\ninforme", font_size="11sp", halign="center")
        btn_nuevo.bind(on_release=self.nuevo_informe)

        frame_bot.add_widget(btn_regresar)
        frame_bot.add_widget(btn_nuevo)

        layout.add_widget(frame_bot)
        self.add_widget(layout)

    def actualizar_vista_informe(self):
        app = App.get_running_app()
        self.lbl_informe_titulo.text = f"informe {app.numero_informe}"

        texto_salida = ""

        for num_p, items in app.informe_pallets.items():
            texto_salida += f"pallet {num_p}\n"
            for item in items:
                texto_salida += f"  lote: {item['lote']} calibre :{item['calibre']} cantidad: {item['cantidad']}\n"
            texto_salida += "\n"

        if app.pallet_actual_items:
            texto_salida += f"pallet {app.numero_pallet} (en proceso...)\n"
            for item in app.pallet_actual_items:
                texto_salida += f"  lote: {item['lote']} calibre :{item['calibre']} cantidad: {item['cantidad']}\n"
            texto_salida += "\n"

        if app.resumen_generado:
            texto_salida += "resumen\n"
            todos = dict(app.informe_pallets)
            if app.pallet_actual_items:
                todos[app.numero_pallet] = app.pallet_actual_items

            tot_pallets = len(todos)
            agrupado = defaultdict(int)
            lotes_unicos = set()

            for items in todos.values():
                for item in items:
                    agrupado[(item["lote"], item["calibre"])] += item["cantidad"]
                    lotes_unicos.add(item["lote"])

            texto_salida += f"  pallets:{tot_pallets}  cantidad de lotes:{len(lotes_unicos)}\n\n"

            for (lote, calibre), cant_tot in agrupado.items():
                texto_salida += f"  lote:{lote} calibre {calibre} cantidad: {cant_tot}\n"

        self.txt_reporte.text = texto_salida

    def nuevo_informe(self, instance):
        app = App.get_running_app()
        app.numero_informe += 1
        app.numero_pallet = 1
        app.pallet_actual_items.clear()
        app.informe_pallets.clear()
        app.resumen_generado = False

        screen_ingreso = self.manager.get_screen("ingreso")
        screen_ingreso.lbl_num_pallet.text = "1"
        screen_ingreso.txt_lote.text = ""
        screen_ingreso.txt_calibre.text = ""
        screen_ingreso.actualizar_contadores()

        self.manager.current = "ingreso"


# ==========================================
# APLICACIÓN PRINCIPAL
# ==========================================
class PalletsApp(App):

    def build(self):
        self.numero_informe = 1
        self.numero_pallet = 1
        self.pallet_actual_items = []
        self.informe_pallets = {}
        self.resumen_generado = False

        sm = ScreenManager()
        sm.add_widget(PantallaIngreso(name="ingreso"))
        sm.add_widget(PantallaResumen(name="resumen"))
        return sm


if __name__ == "__main__":
    PalletsApp().run()