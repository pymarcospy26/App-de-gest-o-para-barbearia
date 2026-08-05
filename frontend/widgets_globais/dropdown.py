import flet as ft
import colors as c

class Dropdown:
    def __init__(self, page, buscar_dados, funcao_de_click, titulo = 'Escolha', titulo_interno = 'Selecionar itens'):
        self.page = page
        self.titulo = titulo
        self.titulo_interno = titulo_interno

        self.funcao_click = funcao_de_click
        self.buscar_dados = buscar_dados

        # def dropdown2(
        # page: ft.Page,
        # titulo: str = 'Dropdow',
        # hint_text: str = 'Escolha uma opção',
        # on_click: Funcao | None = None,
        # icon_categoria: ft.Icon | None = None,
        # margin: ft.Margin = 0,

        self.dropdown = self.Drop()

    def Abrir_drop(self, e = None):
        self.dropdown.controls[1].border = ft.Border.all(width = 2, color = c.lilas_calmo)
        self.dropdown.controls[1].update()
    
    def Drop(self):
        return ft.Column(
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.START,
            
            controls = [
                ft.Text(
                    value = self.titulo,
                    style = ft.TextStyle(size = 12, color = c.sub_textos)
                ),

                ft.Container(
                    height = 60,
                    expand = True,
                    border_radius = 18,
                    bgcolor = c.branco,
                    alignment = ft.Alignment.CENTER,
                    border = ft.Border.all(width = 2, color = c.bordas),

                    content = ft.Text(
                        value = self.titulo_interno,
                        style = ft.TextStyle(
                            size = 16, color = c.textos
                        )
                    ),

                    on_click = self.funcao_click,
                    ink = True
                )
            ]
        )