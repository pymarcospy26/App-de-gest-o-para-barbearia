import flet as ft
import banco as bd
import icons as ic
import colors as c
import unicodedata
import asyncio
import variaveis_globais as vg

class AlertDialog_atendimento:
    def __init__(
        self, page,
    ):
        self.page = page
        self.titulo = ''

        self.servicos_atendimento = {}
        self.totais = 0

        self.margin_lateral_interna = 25
        self.largura_page = self.page.width

        self.dialog_aberto = False

        self.armazenamento_controles = {}
        self.armazenamento_tags = {}

        self.cliente_cadastrados = [
            "João Pedro",
            "Lucas Henrique",
            "Gabriel Silva",
            "Matheus Oliveira",
            "Rafael Costa",
            "Felipe Santos",
            "Bruno Almeida",
            "Carlos Eduardo",
            "Diego Ferreira",
            "Vinícius Souza",
            "Gustavo Lima",
            "André Luiz",
            "Thiago Martins",
            "Leonardo Rocha",
            "Pedro Henrique",
        ]

        self.alertdialog_global = ft.AlertDialog(
            modal = False,
            expand = True,
            actions_padding = 0,
            content_padding = 0,
            bgcolor = c.background,
            shape = ft.RoundedRectangleBorder(radius = 34),
            inset_padding = ft.Padding(left = vg.margin_left, right = vg.margin_right, bottom = 0),

            data = {},
            
            title_padding = ft.Padding(
                left = self.margin_lateral_interna,
                right = self.margin_lateral_interna,
                top = 26,
            )
        )

    def adicao_steppers(self, setor, servico, valor):
        stepper = self.stepper_control(
            servico = servico,
            valor = valor,
            text_total = self.alertdialog_global.data['barra_inferior_atendimento'].content.controls[0].controls[1]
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
        
        self.alertdialog_global.data['lista_atendimento'].controls.append(controle)
#       AQUI ^ ADICIONA OS CONTROLES/LISTA NA TELA ATRAVÉZ DO DATA DO ALERTDIALOG

        return controle
#       RETORNA O CONTROLE PARA ADICIONÁ-LO A UM DICIONÁRIO DE ARMAZENAMENTO QUANDO A FUNÇÃO É CHAMADA

    def recarregar_lista(self, e):
        botao = e.control
        setor = botao.data['setor']
        lista = self.alertdialog_global.data['lista_atendimento']

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
            self.alertdialog_global.data['tags_atendimento'].update()

        self.page.run_task(carregar_nova_lista)

    async def inicializar(self, e = None):
        self.dados_carregados = False

        await self.pages_dialog()

    async def carregar_dados(self):
        setores = await bd.setores()
        servicos_valors = await bd.servico_valor()

        self.alertdialog_global.data['lista_atendimento'].alignment = ft.MainAxisAlignment.START

        self.alertdialog_global.data['lista_atendimento'].controls.clear()

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

        self.alertdialog_global.data['tags_atendimento'].controls.append(tag_todos)

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
            self.alertdialog_global.data['tags_atendimento'].controls.append(tag)
            self.alertdialog_global.data['tags_atendimento'].update()
                
        for setor_reserva, servico, valor in servicos_valors:
            controle = self.adicao_steppers(setor_reserva, servico, valor)
            self.armazenamento_controles[controle.data['servico']] = controle
#           AQUI ^ SÃO ADICIONADOS AO DICIONÁRIO OS RETURN'S (CONTROLES) DA DEF DE CONTROLES/LISTA
    
        self.alertdialog_global.data['lista_atendimento'].update()
        self.alertdialog_global.data['tags_atendimento'].update()

        self.dados_carregados = True

    def pesquisa_servicos(self, e):
        digitado = e.control.value
        self.alertdialog_global.data['lista_atendimento'].controls.clear()

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
                self.alertdialog_global.data['lista_atendimento'].alignment = ft.MainAxisAlignment.START
                controles.append(self.armazenamento_controles[servico])

        if len(controles) == 0:
            not_found = ft.Column(
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

            self.alertdialog_global.data['lista_atendimento'].alignment = ft.MainAxisAlignment.CENTER
            self.alertdialog_global.data['lista_atendimento'].controls.append(not_found)

            return
        
        self.alertdialog_global.data['lista_atendimento'].controls.extend(controles)

    def barra_pesquisa(
        self,
        text_interno = 'Busca rápida',

        on_focus: ft.Event = None,
        on_change: ft.Event = None,
    ):
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
                        border_color = ft.Colors.TRANSPARENT,
                        focused_border_color = c.lilas_calmo,

                        text_style = ft.TextStyle(
                            size = 16, color = c.textos,
                            font_family = 'inter'
                        ),

                        hint_text = text_interno,
                        hint_style = ft.TextStyle(
                            size = 16, color = c.sub_textos,
                            font_family = 'inter'
                        ),

                        on_focus = on_focus,
                        on_change = on_change
                    )
                ),
                
                ic.svg_icon(
                    path = 'lupa',
                    size = 30, color = c.sub_textos,
                    left = 38
                )
            ]
        )

    def abrir(self, e = None):
        if self.alertdialog_global.open:
            return

        self.totais = 0
        self.servicos_atendimento.clear()

        self.alertdialog_global.content.height = self.page.height * 3 / 4
        self.alertdialog_global.content.width = self.page.width

        self.dialog_aberto = True

        self.page.show_dialog(self.alertdialog_global)
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

    async def pages_dialog(self):
        servicos_inseridos = []
        mapa = ['dinheiro/0', 'pix/1', 'cartão/2']

        async def carregar_page_now(titulo_new):
            self.titulo = titulo_new
            self.alertdialog_global.title = ft.Row(
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
                ]
            )

            self.alertdialog_global.content.height = self.page.height * 3 / 4
            self.alertdialog_global.content.width = self.page.width
        async def return_atendimento(e):
            await asyncio.sleep(0.26)
            self.alertdialog_global.content = self.page_servico
            await carregar_page_now('Atendimento')  
            self.alertdialog_global.update()
        async def go_conclusao(e):
            self.alertdialog_global.content = self.page_conclusao
            await carregar_page_now('Conclusão')
            nova_coluna = ft.Column(
                spacing = 0,
                expand = True,
                alignment = ft.MainAxisAlignment.START,
                horizontal_alignment = ft.CrossAxisAlignment.START,
            )
            caminho = self.lista_options_conclusao.controls[2].content
            lista_antiga = caminho.controls[0]
            caminho.controls.remove(lista_antiga)
            for servico in self.servicos_atendimento:
                print('adicionando linha pra:', servico)

                servicos_inseridos.append(servico)
                linha_servico = ft.Column(
                        spacing = 0,
                        height = 64,
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.START,
                        margin = ft.Margin(left = self.margin_lateral_interna, right = self.margin_lateral_interna),
    
                        controls = [
                            ft.Row(
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment = ft.CrossAxisAlignment.CENTER,
    
                                controls = [
                                    ft.Text(
                                        value = f'{self.servicos_atendimento[servico]['quantidade']}x {servico}',
                                        size = 16, color = c.preto_icons, font_family = 'inter'
                                    ),
                                    ft.Text(
                                        value = f'R$ {self.servicos_atendimento[servico]['total']}',
                                        size = 16, color = c.preto_icons, font_family = 'inter'
                                    ),
                                ]
                            ),
    
                            ft.Row(
                                alignment = ft.MainAxisAlignment.START,
                                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                
                                controls = [
                                    ft.Text(
                                        value = f'Und R$ {self.servicos_atendimento[servico]['valor']}',
                                        size = 16, color = c.sub_textos, font_family = 'inter'
                                    )
                                ]
                            )
                        ]
                    )
                nova_coluna.controls.append(linha_servico)
            caminho.controls.insert(0, nova_coluna)

            self.alertdialog_global.update()

        anterior = {}
        def conversao_campo(campo):
            valor = str(campo.value)
            if valor in ['', 'None']:
                valor = '0,00'
            if ',' not in valor and '.' in valor:
                valor = valor.split('.')
                if len(valor) >= 2:
                    if valor[0] == '':
                        valor = '0' + (',' + valor[-1])
                    else:
                        valor = ''.join(valor[:-1]) + (',' + valor[-1])
                else:
                    valor = f'{valor[0]},00'
            else:
                valor = valor.replace('.', '')
                valor = valor.split(',')
                if len(valor) >= 2:
                    if valor[0] == '':
                        valor = '0' + (',' + valor[-1])
                    else:
                        valor = ''.join(valor[:-1]) + (',' + valor[-1])
                else:
                    valor = f'{valor[0]},00'
            campo.value = valor
        def change_values_campos_CONCLUSAO(e):
            campo = e.control
            conversao_campo(campo)
            anterior[campo] = float(campo.value.replace(',', '.'))
            referencia = self.lista_options_conclusao.controls[3].controls[0].controls
            quantiade_controls = len(referencia)
            for fields in referencia:
                if quantiade_controls - len(anterior) > 0:
                    if fields.controls[0] not in anterior:
                        fields.controls[0].value = f'{((self.totais - sum(float(anterior[x]) for x in anterior)) / (quantiade_controls - len(anterior))):.2f}'
                conversao_campo(fields.controls[0])
        def campos_pagamento_CONCLUSAO(button):
            campo = button.data['campo']

            if campo in self.lista_options_conclusao.controls[3].controls[0].controls:
                self.lista_options_conclusao.controls[3].controls[0].controls.remove(campo)
                anterior.clear()

            else:
                pagamentos_list = []
                pix_map = {
                    ('dinheiro', 'cartão'): 1,
                    ('dinheiro',): 1,
                    ('cartão',): 0,
                    (): 0,
                }
                for x in  mapa:
                    print('rodou')

                    if x.split('/')[0] == button.data['modalidade'].lower():
                        if x.split('/')[0].lower() == 'pix':

                            for pagamentos in self.lista_options_conclusao.controls[3].controls[0].controls:
                                pagamentos_list.append(pagamentos.data['campo'].lower())

                            for posicao in pix_map:
                                if posicao == tuple(pagamentos_list):
                                    x = int(pix_map[posicao])

                        else:
                            x = int(x.split('/')[1])

                        print('stop')
                        break

                print('x:', x)
                print('tipo:', type(x))

                campo.value = ''
                
                self.lista_options_conclusao.controls[3].controls[0].controls.insert(x, campo)

            for campos_on in self.lista_options_conclusao.controls[3].controls[0].controls:
                quantidade = len(self.lista_options_conclusao.controls[3].controls[0].controls)
                campos_on.controls[0].value = f'{self.totais / quantidade:.2f}'
                conversao_campo(campos_on.controls[0])
                
            self.lista_options_conclusao.controls[3].update()
        def pagamento_select(e):
            button = e.control
            campo = button.data['campo']
            state = button.data['ativo']
            radio = button.data['radio']
            radio_interno = radio.content
            icon = button.content.controls[1].controls[0]
            text = button.content.controls[1].controls[1]

            if state == False:
                button.data['ativo'] = not button.data['ativo']

                button.border = ft.Border.all(width = 2, color = c.azul_violeta)
                radio.border = ft.Border.all(width = 2, color = c.azul_violeta)
                radio_interno.bgcolor = c.azul_violeta
                icon.color = c.azul_violeta
                text.color = c.azul_violeta
                campos_pagamento_CONCLUSAO(button = button)
                
                print(f'on {text.value}')

            else:
                button.data['ativo'] = not button.data['ativo']

                button.border = ft.Border.all(width = 0, color = ft.Colors.TRANSPARENT)
                radio.border = ft.Border.all(width = 2, color = c.bordas)
                radio_interno.bgcolor = c.background
                icon.color = c.sub_textos
                text.color = c.sub_textos
                campos_pagamento_CONCLUSAO(button = button)

                print(f'off {text.value}')

            button.update()
        def cards_pagamento_CONCLUSAO(
            icon = 'triangulo_alerta',
            text = 'Vazio',

            top = 0, left = 0, right = 0, bottom = 0,
        ):
            campo = ft.Stack(
                margin = ft.Margin(
                    top = vg.margin_top,
                ),
                data = {
                    'campo': text,
                },
                controls = [                            
                    ft.TextField(
                        expand = True,
                        hint_text = f'Recebido em {text.lower()}',
                        bgcolor = c.branco,

                        hint_style = ft.TextStyle(
                            size = 16, color = c.sub_textos, font_family = 'inter'
                        ),
                        text_style = ft.TextStyle(
                            size = 16, color = c.preto_icons, font_family = 'inter'
                        ),

                        content_padding = ft.Padding(top = 22, left = 50, bottom = 22),
                        keyboard_type = ft.KeyboardType.NUMBER,
                        focused_border_color = c.lilas_calmo,

                        border_color = c.bordas,
                        border_radius = 24,

                        margin = ft.Margin(
                            left = self.margin_lateral_interna,
                            right = self.margin_lateral_interna
                        ),

                        on_blur = change_values_campos_CONCLUSAO
                    ),

                    ft.Column(
                        top = 0,
                        left = 38,
                        bottom = 0,
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.START,

                        controls = [
                            ic.svg_icon(
                                icon,
                                size = 30, color = c.sub_textos
                            )
                            if isinstance(icon, str) else
                            ft.Icon(
                                icon = icon,
                                size = 30, color = c.sub_textos
                            ),
                        ]
                    )
                ]
            )
            
            radio = ft.Container(
                top = 12,
                left = 12,
                width = 30,
                height = 30,
                border_radius = 15,
                bgcolor = c.background,
                alignment = ft.Alignment.CENTER,
                border = ft.Border.all(width = 2, color = c.bordas),

                content = ft.Container(
                    width = 20,
                    height = 20,
                    border_radius = 10,
                    bgcolor = c.background
                )
            )

            return ft.Container(
                col = 1,
                height = 180,
                bgcolor = c.branco,
                border_radius = 24,
                shadow = c.shadow_leve(),
                on_click = pagamento_select,
                ink = True,

                width = (
                    self.page.width - (
                        ((2 * vg.margin_left) + (2 * self.margin_lateral_interna) + (2 * 12))
                    )
                ) / 3,

                # ^ DEVOLVE A LARGURA TOTAL DISPONÍVEL DA TELA DESCONTANDO AS MARGINS E SPAÇOS,
                # ^ DIVIDE-OS PELA QUANTIDADE DE BOTÕES E SE OBTEM UMA LARGURA IGUAL PARA TODOS

                data = {
                    'radio': radio,
                    'ativo': False,
                    'modalidade': text,
                    'campo': campo,
                },

                margin = ft.Margin(
                    top = top,
                    left = left,
                    right = right,
                    bottom = bottom
                ),
                
                content = ft.Stack(
                    height = 140,
                    alignment = ft.Alignment.CENTER,
                    
                    controls = [
                        radio,
                                
                        ft.Column(
                            top = 45,
                            bottom = 35,
                            height = 70,
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                            controls = [
                                ic.svg_icon(
                                    icon,
                                    size = 30, color = c.sub_textos,
                                )

                                if isinstance(icon, str) else

                                ft.Icon(
                                    icon = icon,
                                    size = 30, color = c.sub_textos
                                ),
                                
                                ft.Text(
                                    value = text,
                                    size = 16, color = c.sub_textos,
                                    font_family = 'inter',
                                ),
                            ]
                        ),
                    ]
                )

                # ^ CAMINHO PARA ICON: e.control.content.controls[1].controls[0]
                # ^ CAMINHO PARA TEXT: e.control.content.controls[1].controls[1]
                # ^ CAMINHO PARA RADIO: e.control.content.controls[0]
                # ^ CAMINHO PARA RADIO_INTERNO: e.control.content.controls[0].content
            )
        def atualizar_nome_cliente_CONCLUSAO(e):
            drop = e.control
            if drop.value:
                text = drop.value
            else:
                text = 'Cliente ##'
            self.lista_options_conclusao.controls[2].content.controls[0].controls[0].value = text
            self.lista_options_conclusao.controls[2].content.controls[0].controls[0].update()
        
        self.lista_options_conclusao = ft.Column(
            spacing = 0,
            expand = True,
            scroll = ft.ScrollMode.AUTO,
            alignment = ft.MainAxisAlignment.START,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,

            controls = [
                ft.Stack(
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
                                left = self.margin_lateral_interna,
                                right = self.margin_lateral_interna
                            ),

                            content = ft.Dropdown(
                                height = 64,
                                expand = True,
                                editable = True,
                                bgcolor = c.branco,
                                border_radius = 26,
                                enable_search = True,
                                color = c.preto_icons,
                                fill_color = c.branco,

                                trailing_icon = ic.svg_icon(
                                    'seta_bottom',
                                    size = 30, color = c.preto_icons
                                ),

                                selected_trailing_icon = ic.svg_icon(
                                    'seta_top',
                                    size = 30, color = c.preto_icons
                                ),

                                hint_text = 'Buscar cliente',
                                hint_style = ft.TextStyle(
                                    size = 16, color = c.sub_textos,
                                    font_family = 'inter',
                                ),

                                menu_style = ft.MenuStyle(
                                    bgcolor = c.branco,
                                    shape = ft.RoundedRectangleBorder(radius = 26),
                                    shadow_color = ft.Colors.with_opacity(color = c.sombra, opacity = 0.2),

                                    max_size = ft.Size(
                                        height = self.page.height * 0.22,
                                        width = self.page.width - ((2 * 16) + (2 * self.margin_lateral_interna))
                                    ),
                                ),

                                border_color = ft.Colors.TRANSPARENT,
                                focused_border_color = c.lilas_calmo,
                                content_padding = ft.Padding(left = 50, top = 21, bottom = 21),
                                on_select = atualizar_nome_cliente_CONCLUSAO,
                                on_text_change = atualizar_nome_cliente_CONCLUSAO,

                                options = [
                                    ft.DropdownOption(
                                        text = cliente_cadastrado,
                                        style = ft.ButtonStyle(
                                            bgcolor = {
                                                ft.ControlState.FOCUSED: c.lilas_calmo,
                                                ft.ControlState.HOVERED: c.lilas_calmo,
                                                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT
                                            },

                                            color = {
                                                ft.ControlState.FOCUSED: c.branco,
                                                ft.ControlState.HOVERED: c.branco,
                                                ft.ControlState.DEFAULT: c.preto_icons
                                            },

                                            text_style = ft.TextStyle(size = 16, color = c.preto_icons, font_family = 'inter')
                                        )
                                    )

                                    for cliente_cadastrado in self.cliente_cadastrados
                                ]
                            )
                        ),
                        
                        ic.svg_icon(
                            path = 'user',
                            size = 30, color = c.sub_textos,
                            left = 38
                        )
                    ]
                ),

                ft.Row(
                    spacing = 12,
                    expand = True,
                    alignment = ft.MainAxisAlignment.START,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,

                    controls = [
                        cards_pagamento_CONCLUSAO(
                            icon = 'dinheiro', text = 'Dinheiro',
                            top = vg.margin_top,
                            left = self.margin_lateral_interna,
                        ),

                        cards_pagamento_CONCLUSAO(
                            icon = ft.Icons.PIX, text = 'Pix',
                            top = vg.margin_top,
                        ),

                        cards_pagamento_CONCLUSAO(
                            icon = 'cartao', text = 'Cartão',
                            top = vg.margin_top,
                            right = self.margin_lateral_interna,
                        ),
                    ]
                ),

                ft.Container(
                    expand = True,
                    bgcolor = c.branco,
                    border_radius = 26,
                    shadow = c.shadow_leve(),
                    alignment = ft.Alignment.CENTER,
                    height = self.page.height * 0.3,
                    margin = ft.Margin(
                        top = vg.margin_top,
                        left = self.margin_lateral_interna,
                        right = self.margin_lateral_interna
                    ),

                    content = ft.Column(
                        spacing = 0,
                        expand = True,
                        alignment = ft.MainAxisAlignment.START,
                        horizontal_alignment = ft.CrossAxisAlignment.START,

                        controls = [
                            ft.Row(
                                alignment = ft.MainAxisAlignment.START,
                                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                margin = ft.Margin(
                                    top = self.margin_lateral_interna,
                                    left = self.margin_lateral_interna,
                                    bottom = self.margin_lateral_interna / 2,
                                ),

                                controls = [
                                    ft.Text(
                                        value = 'Cliente ##',
                                        size = 22, color = c.preto_icons,
                                        font_family = 'inter', weight = ft.FontWeight.W_500
                                    )
                                ]
                            ),

                            ft.Column(
                                spacing = 0,
                                expand = True,
                                scroll = ft.ScrollMode.AUTO,
                                alignment = ft.MainAxisAlignment.START,
                                horizontal_alignment = ft.CrossAxisAlignment.START
                            )
                        ]                        
                    )
                ),

                ft.Column(
                    expand = True,
                    alignment = ft.MainAxisAlignment.START,
                    horizontal_alignment = ft.CrossAxisAlignment.START,

                    controls = [
                        ft.Column(
                            spacing = 0,
                            expand = True,
                            alignment = ft.MainAxisAlignment.START,
                            horizontal_alignment = ft.CrossAxisAlignment.START,
                        ),

                        ft.Column(height = 200)
                    ]
                )
            ]
        
        )                  
        self.barra_inferior_conclusao = ft.Container(
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
                    ft.Container(
                        height = 58,
                        bgcolor = c.branco,
                        shadow = c.shadow_leve(y = 2, opc = 0.4),

                        margin = ft.Margin(
                            left = self.margin_lateral_interna,
                        ),
                                        
                        border_radius = 24,
                        alignment = ft.Alignment.CENTER,
        
                        content = ft.Row(
                            spacing = 6,
                            alignment = ft.MainAxisAlignment.CENTER,
                            vertical_alignment = ft.CrossAxisAlignment.CENTER,
                            
                            margin = ft.Margin(left = 26, right = 36),

                            controls = [
                                ic.svg_icon(
                                    'seta_exit',
                                    size = 26, color = c.rosa
                                ),
                                        
                                ft.Text(
                                    value = 'Voltar',
                                    style = ft.TextStyle(
                                        size = 16, color = c.rosa, font_family = 'inter',
                                    ),
                                )
                            ]
                        ),

                        on_click = return_atendimento,
                        ink = True
                    ),

                    ft.Container(
                        height = 58,
                        shadow = c.shadow_buttons(),

                        gradient = c.gradiente_top_bottom(c.gradiente_botoes),
                        margin = ft.Margin(
                            right = self.margin_lateral_interna,
                        ),
                                        
                        border_radius = 24,
                        alignment = ft.Alignment.CENTER,
        
                        content = ft.Text(
                            value = 'Finalizar',
                            style = ft.TextStyle(
                                size = 16, color = c.branco, font_family = 'inter',
                            ),
                            margin = ft.Margin(left = 36, right = 36)
                        ),

                        on_click = True,
                        ink = True
                    )
                ]
            )
        )
        self.page_conclusao = ft.Column(
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
                            self.lista_options_conclusao,
                        ]
                    ),

                    self.barra_inferior_conclusao,
                ]
            )

        self.tags_sugestoes = ft.Row(
                margin = ft.Margin(top = 6),
                scroll = ft.ScrollMode.AUTO,
                alignment = ft.MainAxisAlignment.START,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = []
            )
        self.lista_options = ft.Column(
                spacing = 0,
                expand = True,
                scroll = ft.ScrollMode.AUTO,

                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [ft.ProgressRing(color = c.lilas_calmo, height = 100, width = 100)]
            )      
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
                                    value = 'Subtotal', margin = ft.Margin(left = self.margin_lateral_interna),
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
                            shadow = c.shadow_buttons(),
                            gradient = c.gradiente_top_bottom(c.gradiente_botoes),

                            margin = ft.Margin(
                                right = self.margin_lateral_interna,
                            ),
                                            
                            border_radius = 24,
                            alignment = ft.Alignment.CENTER,
            
                            content = ft.Text(
                                value = 'Prosseguir',
                                style = ft.TextStyle(
                                    size = 16, color = c.branco, font_family = 'inter',
                                ),

                                margin = ft.Margin(left = 26, right = 26)
                            ),

                            on_click = go_conclusao,
                            ink = True
                        )
                    ]
                )
            )
        self.page_servico = ft.Column(
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
                        self.barra_pesquisa(
                            on_focus = self.pesquisa_servicos,
                            on_change = self.pesquisa_servicos
                        ),

                        self.tags_sugestoes,
                        self.lista_options,
                    ]
                ),

                self.barra_inferior,
            ]
        )

        self.alertdialog_global.content = self.page_servico
        self.alertdialog_global.data = {
            'tags_atendimento': self.tags_sugestoes,
            'lista_atendimento': self.lista_options,
            'barra_inferior_atendimento': self.barra_inferior,
            'barra_pesquisa_atendimento': self.barra_pesquisa,
            
            # 'tags_conclusao': self.tags_sugestoes,
            'lista_conclusao': self.lista_options_conclusao,
            'barra_inferior_conclusao': self.barra_inferior_conclusao,
            'barra_pesquisa_conclusao': self.barra_pesquisa,
        }

        await carregar_page_now('Atendimento')

