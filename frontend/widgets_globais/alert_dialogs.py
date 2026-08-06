import flet as ft
import banco as bd
import icons as ic
import colors as c
import unicodedata
import variaveis_globais as vg

class AlertDialog_stepper:
    def __init__(
        self, page,
        titulo = 'Selecionar item', text_button = 'Salvar'
    ):
        self.page = page
        self.titulo = titulo
        self.text_button = text_button

        self.servicos_atendimento = {}
        self.totais = 0

        self.margin_lateral_interna = 25
        self.largura_page = self.page.width

        self.dialog_aberto = False

        self.armazenamento_controles = {}
        self.armazenamento_tags = {}

    def adicao_steppers(self, setor, servico, valor):
        stepper = self.stepper_control(
            servico = servico,
            valor = valor,
            text_total = self.dialog.data['barra_inferior'].content.controls[0].controls[1]
        )
                                
        valors = f'R$ {valor:.2f}'.replace('.', ',')

        controle = ft.Container(
            expand = True,
            border_radius = 0,
            border = ft.Border(bottom = ft.BorderSide(width = 0.04, color = c.preto_icons)),
            margin = ft.Margin(left = self.margin_lateral_interna, right = self.margin_lateral_interna),
                                                                    
            data = {
                'setor': setor,
                'servico': servico,
                'valor': valor,
                'stepper': stepper
            },
                                                                        
            content = ft.Row(
                margin = 0,
                height = 84,
                expand = True,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                
                controls = [
                    ft.Column(
                        height = 45,
                        spacing = 0,
                        expand = True,
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.START,
                
                        controls = [
                            ft.Text(
                                expand = True,
                                max_lines = 1,
                                value = servico,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                style = ft.TextStyle(size = 16, color = c.preto_icons, font_family = 'inter'),
                            ),

                            ft.Text(
                                expand = True,
                                max_lines = 1,
                                value = valors,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                style = ft.TextStyle(size = 14, color = c.preto_icons, font_family = 'inter', weight = ft.FontWeight.W_300),
                            )
                        ]
                    ),
                            
                    stepper
                ]
            )
        )
        
        self.dialog.data['lista'].controls.append(controle)

        return controle

    def recarregar_lista(self, e):
        botao = e.control
        setor = botao.data['setor']
        lista = self.dialog.data['lista']

        lista.controls.clear()
        lista.alignment = ft.MainAxisAlignment.CENTER
        lista.controls.append(ft.ProgressRing(color = c.lilas_calmo, height = 80, width = 80))

        for tag in self.armazenamento_tags:
            self.armazenamento_tags[tag].bgcolor = c.branco
            self.armazenamento_tags[tag].content.color = c.textos
            self.armazenamento_tags[tag].update()

        botao.bgcolor = c.lilas
        botao.content.color = c.branco

        botao.update()

        async def carregar_nova_lista():
            lista.controls.clear()
            lista.alignment = ft.MainAxisAlignment.START

            for controle in self.armazenamento_controles:       #   BUSCA O ID/SERVICO CONTAINER DENTRO DO DICIONÁRIO
                box = self.armazenamento_controles[controle]    #   ARMAZENA O CONTAINER

                if setor != 'Todos':
                    if box.data['setor'] == setor:
                        lista.controls.append(box)

                else:
                    lista.controls.append(box)
            
            lista.update()
            self.dialog.data['tags'].update()

        self.page.run_task(carregar_nova_lista)

    async def inicializar(self):
        self.dados_carregados = False
        self.dialog = self.alertdialog()

    async def carregar_dados(self):
        setores = await bd.setores()
        servicos_valors = await bd.servico_valor()

        self.dialog.data['lista'].alignment = ft.MainAxisAlignment.START

        self.dialog.data['lista'].controls.clear()

        tag_todos = ft.Container(
            height = 56,
            bgcolor = c.lilas,
            border_radius = 22,
            shadow = c.shadow_leve(),
            alignment = ft.Alignment.CENTER,
            padding = ft.Padding(left = 26, right = 26),
            margin = ft.Margin(left = self.margin_lateral_interna),
                        
            content = ft.Text(
                value = 'Todos',
                style = ft.TextStyle(
                    size = 14, color = c.branco
                )
            ),

            data = {
                'setor': 'Todos'
            },

            on_click = self.recarregar_lista
        )

        self.dialog.data['tags'].controls.append(tag_todos)

        self.armazenamento_tags['Todos'] = tag_todos
        
        for setor in setores[:3]:
            tag = ft.Container(
                height = 54,
                bgcolor = c.branco,
                border_radius = 22,
                shadow = c.shadow_leve(),
                alignment = ft.Alignment.CENTER,
                padding = ft.Padding(left = 26, right = 26),
                data = {
                    'setor': setor
                },
            
                content = ft.Text(
                    value = setor,
                    style = ft.TextStyle(
                        size = 14, color = c.textos
                    )
                ),
                ink = True,
                on_click = self.recarregar_lista
            )

            self.armazenamento_tags[setor] = tag
            self.dialog.data['tags'].controls.append(tag)
            self.dialog.data['tags'].update()
                
        for setor_reserva, servico, valor in servicos_valors:
            controle = self.adicao_steppers(setor_reserva, servico, valor)
            self.armazenamento_controles[controle.data['servico']] = controle
    
        self.dialog.data['lista'].update()
        self.dialog.data['tags'].update()

        self.dados_carregados = True

    def pesquisa_servicos(self, e):
        digitado = e.control.value
        self.dialog.data['lista'].controls.clear()

        controles = []

        def normalizar_letras(texto):
            texto = unicodedata.normalize('NFD', texto)
            texto = ''.join(
                letra
                for letra in texto
                if unicodedata.category(letra) != 'Mn'
            )

            return texto.lower()

        palavras = normalizar_letras(digitado).split()

        for servico in self.armazenamento_controles:
            texto_servico = normalizar_letras(servico)

            if all(palavra in texto_servico for palavra in palavras):
                self.dialog.data['lista'].alignment = ft.MainAxisAlignment.START
                controles.append(self.armazenamento_controles[servico])

        if len(controles) == 0:
            error = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                controls = [
                    ic.svg_icon(
                        'not_found_busca',
                        size = 50, color = c.preto_icons
                    ),

                    ft.Text(
                        value = 'Sem resultados\npara essa busca',
                        size = 16, color = c.preto_icons,
                        font_family = 'inter', text_align = ft.TextAlign.CENTER
                    ),
                ]
            )
            self.dialog.data['lista'].alignment = ft.MainAxisAlignment.CENTER
            self.dialog.data['lista'].controls.append(error)

            return
        
        self.dialog.data['lista'].controls.extend(controles)

    def barra_pesquisa(self):
        return ft.Stack(
            height = 74,
            alignment = ft.Alignment.CENTER,

            controls = [
                ft.Container(
                    left = 0,
                    right = 0,
                    expand = True,
                    bgcolor = c.branco,
                    border_radius = 24,
                    shadow = c.shadow_leve(),
                    
                    margin = ft.Margin(
                        left = self.margin_lateral_interna, right = self.margin_lateral_interna
                    ),

                    content = ft.TextField(
                        expand = True,
                        border_radius = 24,
                        content_padding = ft.Padding(left = 50, top = 21, bottom = 21),

                        bgcolor = c.branco,
                        border = ft.Border.all(width = 0.6),
                        border_color = ft.Colors.TRANSPARENT,
                        focused_border_color = c.lilas_calmo,

                        text_style = ft.TextStyle(
                            size = 16, color = c.textos,
                            font_family = 'inter'
                        ),

                        hint_text = 'Buscar servico',
                        hint_style = ft.TextStyle(
                            size = 16, color = c.sub_textos,
                            font_family = 'inter'
                        ),

                        on_focus = self.pesquisa_servicos,
                        on_change = self.pesquisa_servicos
                    )
                ),
                
                ic.svg_icon(
                    path = 'lupa',
                    size = 30, color = c.sub_textos,
                    left = 38
                )
            ]
        )

    def alertdialog(self):  
        self.barra_inferior = ft.Container(
            height = 110,
            bgcolor = c.branco,
            shadow = c.shadow_leve(x = 0, y = -4),

            border_radius = ft.BorderRadius(
                top_left = 0,
                top_right = 0,
                bottom_left = 34,
                bottom_right = 34
            ),

            content = ft.Row(
                expand = True,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,
        
                controls = [
                    ft.Column(
                        spacing = 0,
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.START,
        
                        controls = [
                            ft.Text(
                                value = 'Total', margin = ft.Margin(left = self.margin_lateral_interna),
                                style = ft.TextStyle(size = 14, color = c.sub_textos, font_family = 'inter')
                            ),
        
                            ft.Text(
                                value = 'R$ 0,00', margin = ft.Margin(left = self.margin_lateral_interna),
                                style = ft.TextStyle(size = 22, color = c.preto_icons, font_family = 'inter')
                            ),
                            
                            ft.Row(height = 6),
                        ]
                    ),
        
                    ft.Container(
                        height = 58,
                        gradient = c.gradiente_top_bottom(c.gradiente_botoes),
                        margin = ft.Margin(
                            right = self.margin_lateral_interna,
                        ),
                                        
                        border_radius = 24,
                        alignment = ft.Alignment.CENTER,
        
                        content = ft.Text(
                            value = self.text_button,
                            style = ft.TextStyle(
                                size = 16, color = c.branco, font_family = 'inter',
                            ),

                            margin = ft.Margin(left = 26, right = 26)
                        ),
                    )
                ]
            )
        )
        
        self.lista_options = ft.Column(
            spacing = 0,
            expand = True,
            scroll = ft.ScrollMode.AUTO,

            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,

            controls = [ft.ProgressRing(color = c.lilas_calmo, height = 100, width = 100)]
        )

        self.tags_sugestoes = ft.Row(
            margin = ft.Margin(top = 6),
            scroll = ft.ScrollMode.AUTO,
            alignment = ft.MainAxisAlignment.START,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,

            controls = []
        )

        self.control_alert = ft.AlertDialog(
            modal = False,             #   ATIVAR QUANDO TIVER O BOTÃO DE FECHAR
            expand = True,
            actions_padding = 0,
            content_padding = 0,
            bgcolor = c.background,
            shape = ft.RoundedRectangleBorder(radius = 34),
            inset_padding = ft.Padding(left = vg.margin_left, right = vg.margin_right, bottom = 0),

            data = {
                'tags': self.tags_sugestoes,
                'lista': self.lista_options,
                'barra_inferior': self.barra_inferior,
                'barra_pesquisa': self.barra_pesquisa,
            },

            title = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Text(
                        value = self.titulo,
                        style = ft.TextStyle(size = 22, color = c.preto_icons, font_family = 'inter')
                    ),

                    ft.Container(
                        width = 64,
                        height = 64,
                        border_radius = 24,
                        bgcolor = ft.Colors.TRANSPARENT,
                        alignment = ft.Alignment.CENTER,

                        content = ft.Icon(
                            icon = ft.CupertinoIcons.XMARK,
                            size = 24, color = c.preto_icons
                        ),

                        on_click = self.fechar,
                        ink = True
                    )
                ],
            ),
            
            title_padding = ft.Padding(
                left = self.margin_lateral_interna,
                right = self.margin_lateral_interna,
                top = 26,
            ),

            content = ft.Column(
                spacing = 0,
                expand = True,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Column(
                        expand = True,
                        alignment = ft.MainAxisAlignment.START,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        controls = [
                            self.barra_pesquisa(),
                            self.tags_sugestoes,
                            self.lista_options,
                        ]
                    ),

                    self.barra_inferior,
                ]
            )
        )

        return self.control_alert

    def abrir(self, e = None):
        if self.dialog.open:
            return

        self.totais = 0
        self.servicos_atendimento.clear()

        self.dialog.content.height = self.page.height * 3 / 4
        self.dialog.content.width = self.page.width

        self.dialog_aberto = True

        self.page.show_dialog(self.dialog)
        self.page.update()

        if not self.dados_carregados:
            self.page.run_task(self.carregar_dados)

    def fechar(self, e = None):
        self.dialog_aberto = False

        self.page.pop_dialog()
        self.page.update()

    def status_quant_stepper(self, e):
        controle = e.control
        servico = controle.data['servico']
        valor = controle.data['valor']
        campo = controle.data['campo']
        btn_inverso = controle.data['btn_inverso']

        quantidade = 0

        if controle.data['acao'] == 'subtrair' and int(campo.value) <= 0:
            return

        if controle.data['acao'] == 'somar':
            if int(campo.value) == 0:
                controle.bgcolor = c.lilas
                controle.content.color = c.branco

                btn_inverso.opacity = 1
                btn_inverso.on_click = self.status_quant_stepper

                btn_inverso.update()
                controle.update()

            quantidade = int(campo.value)
            quantidade += 1

            self.servicos_atendimento[servico] = {
                'valor': valor,
                'quantidade': quantidade,
                'total': valor * quantidade
            }

            campo.value = quantidade
            campo.update()

        else:
            quantidade = int(campo.value)
            quantidade = quantidade - 1

            self.servicos_atendimento[servico] = {
                'valor': valor,
                'quantidade': quantidade,
                'total': valor * quantidade
            }

            campo.value = quantidade
            campo.update()

            if quantidade == 0:
                btn_inverso.bgcolor = c.branco
                btn_inverso.content.color = c.textos

                controle.on_click = None
                controle.opacity = 0.2

                if servico in self.servicos_atendimento:      #   LIMPA O REGISTRO DO DICIONÁRIO PARA NÃO SER UM PROBLEMA NA H0RA DE LER
                    self.servicos_atendimento.pop(servico)

                controle.update()
                btn_inverso.update()

        totais_temporario = 0

        for servicos in self.servicos_atendimento:
            totais_temporario += self.servicos_atendimento[servicos]['total']

        self.totais = totais_temporario
        totalidade = f'{totais_temporario:.2f}'.replace('.', ',')
        controle.data['text_total'].value = f'R$ {totalidade}'

        controle.data['text_total'].update()

        totais_temporario = 0

        print(self.totais)
        print(self.servicos_atendimento)
    
    def stepper_control(self, servico = None, valor = None, text_total = ft.Control):
        campo = ft.Text(
            value = 0,
            width = 50,
            max_lines = 1,
            text_align = ft.TextAlign.CENTER,
            overflow = ft.TextOverflow.ELLIPSIS,
        
            style = ft.TextStyle(
                size = 18, color = c.preto_icons, font_family = 'inter'
            )
        )

        btn_menos = ft.Container(          #   BOTÃO DE SUBTRAÇÃO
            width = 54,
            height = 54,
            opacity = 0.2,
            border_radius = 22,
            bgcolor = c.branco,
            shadow = c.shadow_leve(),
            alignment = ft.Alignment.CENTER,
                
            content = ft.Icon(
                icon = ft.CupertinoIcons.MINUS,
                size = 16, color = c.textos
            )
        )

        btn_mais = ft.Container(           #   BOTÃO DE ADIÇÃO
            width = 54,
            height = 54,
            border_radius = 22,
            bgcolor = c.branco,
            shadow = c.shadow_leve(),
            alignment = ft.Alignment.CENTER,
                                    
            content = ft.Icon(
                icon = ft.CupertinoIcons.PLUS,
                size = 16, color = c.textos
            ),

            on_click = self.status_quant_stepper
        )

        btn_mais.data = {
            'servico': servico,
            'valor': valor,
            'campo': campo,
            'btn_inverso': btn_menos,
            'text_total': text_total,

            'acao': 'somar'
        }

        btn_menos.data = {
            'servico': servico,
            'valor': valor,
            'campo': campo,
            'btn_inverso': btn_mais,
            'text_total': text_total,


            'acao': 'subtrair'
        }

        return ft.Row(
            spacing = 0,
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,

            data = {
                'servico': servico,
                'preco': valor,
                'campo': campo,
                'menos': btn_menos,
                'mais': btn_mais
            },

            controls = [
                btn_menos,
                campo,
                btn_mais
            ]
        )

