import flet as ft
import colors as c
from frontend.widgets_globais import alert_dialogs as at

async def dropdown(
    page: ft.Page,
    titulo: str = 'Dropdow',
    hint_text: str = 'Toque para selecionar',
    margin: ft.Margin = 0,
    
):
    
    alert = at.AlertDialog_stepper(page, 'Serviços', 'Continuar')
    await alert.inicializar()

    return ft.Column(
        margin = margin,
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.START,
        
        controls = [
            ft.Text(
                value = titulo,
                style = ft.TextStyle(
                    size = 14, color = c.preto_icons,
                    font_family = 'inter'
                )
            ),

            ft.Container(
                height = 74,
                expand = True,
                border_radius = 28,
                bgcolor = c.branco,
                shadow = c.shadow_leve(),
                alignment = ft.Alignment.CENTER,

                content = ft.Row(
                    controls = [
                        ft.Text(
                            value = hint_text,
                            style = ft.TextStyle(
                                size = 16, color = c.preto_icons
                            ),

                            margin = ft.Margin(left = 24)
                        )
                    ]
                ),

                on_click = lambda e: alert.abrir(e),
                ink = True
            )
        ]
    )

