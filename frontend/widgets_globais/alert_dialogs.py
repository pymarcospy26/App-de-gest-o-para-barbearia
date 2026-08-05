import flet as ft
import banco as bd
import icons as ic
import colors as c
import unicodedata
import variaveis_globais as vg

from backend import estado_do_atendimento as cofre

class AlertDialog_stepper:
    def __init__(
        self, page,
        titulo = 'Selecionar item', text_button = 'Salvar'
    ):
        self.page = page
        self.titulo = titulo
        self.text_button = text_button

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
            border = ft.Border(bottom = ft.BorderSide(width = 0.6, color = c.bordas)),
            margin = ft.Margin(left = self.margin_lateral_interna, right = self.margin_lateral_interna),
                                                                    
            data = {
                'setor': setor,
                'servico': servico,
                'valor': valor,
                'stepper': stepper
            },
                                                                        
            content = ft.Row(
                margin = 0,
                height = 80,
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
                                style = ft.TextStyle(size = 12, color = c.sub_textos, font_family = 'inter'),
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
            self.armazenamento_tags[tag].border = ft.Border.all(
                width = 0.6, color = c.bordas
            )
            self.armazenamento_tags[tag].content.color = c.textos

            self.armazenamento_tags[tag].update()

        botao.bgcolor = c.lilas
        botao.border = ft.Border.all(
            width = 0, color = ft.Colors.TRANSPARENT
        )
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

            self.dialog.data['lista'].controls.append(ft.Row(height = 80))
            
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
            alignment = ft.Alignment.CENTER,
            padding = ft.Padding(left = 26, right = 26),
            border = ft.Border.all(width = 0.6, color = c.bordas),
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
                alignment = ft.Alignment.CENTER,
                padding = ft.Padding(left = 26, right = 26),
                border = ft.Border.all(width = 0.6, color = c.bordas),
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

        self.dialog.data['lista'].controls.append(ft.Row(height = 80))
    
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
                        size = 40, color = c.sub_textos
                    ),

                    ft.Text(
                        value = 'Sem resultados\npara essa busca',
                        size = 14, color = c.sub_textos,
                        font_family = 'inter', text_align = ft.TextAlign.CENTER
                    ),

                    ft.Row(height = 80)
                ]
            )
            self.dialog.data['lista'].alignment = ft.MainAxisAlignment.CENTER
            self.dialog.data['lista'].controls.append(error)

            return
        
        self.dialog.data['lista'].controls.extend(controles)

    def alertdialog(self):        
        barra_inferior = ft.Container(
            left = 0,
            right = 0,
            bottom = 0,
            height = 80,
            bgcolor = c.branco,
            shadow = c.shadow_leve(x = 0, y = -2),

            border_radius = ft.BorderRadius(
                top_left = 0,
                top_right = 0,
                bottom_left = 34,
                bottom_right = 34
            ),

            content = ft.Row(
                height = 80,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment = ft.CrossAxisAlignment.END,
        
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
                                style = ft.TextStyle(size = 18, color = c.preto_icons, font_family = 'inter')
                            ),
                        ]
                    ),
        
                    ft.Container(
                        height = 56,
                        gradient = c.gradiente_top_bottom(c.gradiente_botoes),
                        margin = ft.Margin(
                            right = self.margin_lateral_interna,
                        ),
                                        
                        border_radius = 22,
                        alignment = ft.Alignment.CENTER,
        
                        content = ft.Text(
                            value = self.text_button,
                            style = ft.TextStyle(
                                size = 14, color = c.branco, font_family = 'inter',
                            ),

                            margin = ft.Margin(left = 26, right = 26)
                        ),
                    )
                ]
            )
        )

        lista_options = ft.Column(
            top = 142,
            left = 0,
            right = 0,
            bottom = 0,
            spacing = 0,
            expand = True,
            scroll = ft.ScrollMode.AUTO,

            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,

            controls = [ft.ProgressRing(color = c.lilas_calmo, height = 80, width = 80)]
        )

        barra_pesquisa = ft.Stack(
            top = 0,
            left = 0,
            right = 0,
            height = 64,

            alignment = ft.Alignment.CENTER,

            controls = [
                ft.Container(
                    left = 0,
                    right = 0,
                    expand = True,
                    bgcolor = c.branco,
                    border_radius = 24,
                    
                    margin = ft.Margin(
                        left = self.margin_lateral_interna, right = self.margin_lateral_interna
                    ),

                    content = ft.TextField(
                        expand = True,
                        border_radius = 24,
                        content_padding = ft.Padding(left = 50, top = 21, bottom = 21),

                        bgcolor = c.branco,
                        border = ft.Border.all(width = 0.6),
                        border_color = c.bordas,
                        focused_border_color = c.lilas_calmo,

                        text_style = ft.TextStyle(
                            size = 14, color = c.textos,
                            font_family = 'inter'
                        ),

                        hint_text = 'Buscar servico',
                        hint_style = ft.TextStyle(
                            size = 14, color = c.sub_textos,
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

        tags_sugestoes = ft.Row(
            top = 78,
            left = 0,
            right = 0,
            scroll = ft.ScrollMode.AUTO,
            alignment = ft.MainAxisAlignment.START,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,

            controls = []
        )

        return ft.AlertDialog(
            modal = False,             #   ATIVAR QUANDO TIVER O BOTÃO DE FECHAR
            expand = True,
            bgcolor = c.branco,
            content_padding = 0,
            shape = ft.RoundedRectangleBorder(radius = 34),
            inset_padding = ft.Padding(left = vg.margin_left, right = vg.margin_right),

            data = {
                'tags': tags_sugestoes,
                'lista': lista_options,
                'barra_inferior': barra_inferior,
                'barra_pesquisa': barra_pesquisa,
            },

            title = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Text(
                        value = self.titulo,
                        style = ft.TextStyle(size = 18, color = c.textos, font_family = 'inter')
                    ),

                    ft.Container(
                        width = 45,
                        height = 45,
                        border_radius = 45 * 0.388,
                        bgcolor = ft.Colors.TRANSPARENT,
                        alignment = ft.Alignment.CENTER,

                        content = ft.Icon(
                            icon = ft.CupertinoIcons.XMARK,
                            size = 18, color = c.sub_textos
                        ),

                        on_click = self.fechar,
                        ink = True
                    )
                ],
            ),
            
            title_padding = ft.Padding(
                left = self.margin_lateral_interna,
                right = self.margin_lateral_interna,
                top = 25
            ),

            content = ft.Stack(
                margin = ft.Margin(top = 15),

                controls = [
                    barra_pesquisa,
                    tags_sugestoes,
                    lista_options,
                    barra_inferior,
                ]
            )
        )

    def abrir(self, e = None):
        if self.dialog.open:
            return

        self.dialog.content.height = self.page.height * 3 / 5
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

            cofre.servicos_atendimento[servico] = {
                'valor': valor,
                'quantidade': quantidade,
                'total': valor * quantidade
            }

            campo.value = quantidade
            campo.update()

        else:
            quantidade = int(campo.value)
            quantidade = quantidade - 1

            cofre.servicos_atendimento[servico] = {
                'valor': valor,
                'quantidade': quantidade,
                'total': valor * quantidade
            }

            campo.value = quantidade
            campo.update()

            if quantidade == 0:
                btn_inverso.bgcolor = c.branco
                btn_inverso.border = ft.Border.all(width = 0.6, color = c.bordas)
                btn_inverso.content.color = c.textos

                controle.on_click = None
                controle.opacity = 0.4

                if servico in cofre.servicos_atendimento:      #   LIMPA O REGISTRO DO DICIONÁRIO PARA NÃO SER UM PROBLEMA NA H0RA DE LER
                    cofre.servicos_atendimento.pop(servico)

                controle.update()
                btn_inverso.update()

        totais_temporario = 0

        for servicos in cofre.servicos_atendimento:
            totais_temporario += cofre.servicos_atendimento[servicos]['total']

        cofre.totais = totais_temporario
        totalidade = f'{totais_temporario:.2f}'.replace('.', ',')
        controle.data['text_total'].value = f'R$ {totalidade}'

        controle.data['text_total'].update()

        totais_temporario = 0

        print(cofre.totais)
        print(cofre.servicos_atendimento)
    
    def stepper_control(self, servico = None, valor = None, text_total = ft.Control):
        campo = ft.Text(
            value = 0,
            width = 40,
            max_lines = 1,
            text_align = ft.TextAlign.CENTER,
            overflow = ft.TextOverflow.ELLIPSIS,
        
            style = ft.TextStyle(
                size = 14, color = c.preto_icons, font_family = 'inter'
            )
        )

        btn_menos = ft.Container(          #   BOTÃO DE SUBTRAÇÃO
            width = 54,
            height = 54,
            opacity = 0.4,
            border_radius = 22,
            bgcolor = c.branco,
            border = ft.Border.all(width = 0.6, color = c.bordas),
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
            border = ft.Border.all(width = 0.6, color = c.bordas),
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

class AlertDialog_check:
    def __init__(self):
        pass

        # def status_check_box_control(self, e):
    #     if 'check' in e.control.data:
    #         check = e.control.data['check']
    #         item = e.control.data['item']

    #     else:
    #         check = e.control
    #         item = e.control.data['item']
            
    #     if not check.data['ativo']:
    #         check.bgcolor = c.verde
    #         check.border = ft.Border.all(width = 0, color = ft.Colors.TRANSPARENT)
    #         check.data['ativo'] = True

    #         print(item)

    #     else:
    #         check.bgcolor = c.branco
    #         check.border = ft.Border.all(width = 1, color = c.sub_textos)
    #         check.data['ativo'] = False

    #     e.control.update()

    # def check_box_control(self, item):
    #     return ft.Container(
    #         width = 25,
    #         height = 25,
    #         border_radius = 8,
    #         bgcolor = c.branco,
    #         border = ft.Border.all(width = 1, color = c.sub_textos),

    #         data = {
    #             'ativo': False,
    #             'item': item
    #         },

    #         content = ft.Icon(
    #             icon = ft.CupertinoIcons.CHECK_MARK,
    #             size = 20, color = c.branco
    #         ),

    #         on_click = self.status_check_box_control
    #     )


    # def adicionar_itens_dialog_CHECK(self):
            # self.dialog.content.controls[0].controls.clear()
    
            # for item in self.plug_dados:
            #     check = self.check_box_control(item)
                
            #     self.dialog.content.controls[0].controls.extend([
            #         ft.Container(
            #             border_radius = 0,
            #             border = ft.Border(bottom = ft.BorderSide(width = 0.6, color = c.bordas)),
            #             margin = ft.Margin(left = self.margin_lateral_interna, right = self.margin_lateral_interna),
                                        
            #             data = {
            #                 'item': item,
            #                 'check': check
            #             },
                                            
            #             content = ft.Row(
            #                 margin = 0,
            #                 height = 70,
            #                 expand = True,
            #                 alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            #                 vertical_alignment = ft.CrossAxisAlignment.CENTER,
    
            #                 controls = [
            #                     ft.Text(
            #                         value = item,
            #                         style = ft.TextStyle(size = 16, color = c.sub_textos, font_family = 'inter')
            #                     ),
                
            #                     check
            #                 ]
            #             ),
    
            #             on_click = self.status_check_box_control
            #         )
            #     ])