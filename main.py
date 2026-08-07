import flet as ft
import colors as c
from frontend.pages import tela_home as thm

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.padding = 0
        self.page.bgcolor = c.background

        self.page.theme = ft.Theme(
            system_overlay_style = ft.SystemOverlayStyle(
                status_bar_color = ft.Colors.TRANSPARENT,
                status_bar_icon_brightness = ft.Brightness.DARK,

                system_navigation_bar_color = c.branco,
                system_navigation_bar_icon_brightness = ft.Brightness.DARK
            )
        )

        self.tela_home = thm.Tela_Home(page)

        self.page.fonts = {
            'inter': 'fonts/Inter-VariableFont_opsz,wght.ttf'
        }

    async def pagina(self):
        self.page.add(
            ft.SafeArea(
                expand = True,
                content = await self.tela_home.tela()
            )
        )
  
async def execute( page: ft.Page):
    i = App(page)  
    await i.pagina()

# ft.run(execute, assets_dir = 'assets') 
ft.run(execute, view = ft.AppView.WEB_BROWSER, host = '0.0.0.0', assets_dir = 'assets')