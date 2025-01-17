import flet as ft
import json
from functions import *


def main(page: ft.Page):
    page.title = 'Flet App'
    page.theme_mode = 'dark'
    page.window.width = 1200
    page.window.height = 900
    selected_partner = ft.Ref[str]()

    def set_selected_partner(e):
        for i in partner_field.controls:
            if i.width != None and i.height != None:
                i.width = 150
                i.height = 50
                i.bgcolor = 'white'
        e.control.width = 155
        e.control.height = 55
        e.control.bgcolor = 'green'

        selected_partner.current = e.control.data[0]
        snack_bar = ft.SnackBar(ft.Text(f"Выбран партнёр: {e.control.data[1]}"), duration=5000)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        for i in [input_field_set_policy, result_field_set_policy, result_field_set_cancellation]:
            i.border = ft.border.all(color='black') if page.theme_mode == 'light' else ft.border.all(color='white')
        for i in [partner_field, input_field_set_cancellation]:
            i.border_color = 'white' if page.theme_mode == 'dark' else 'black'
        page.update()

    def set_policy_method(e):
        result_field_set_policy.content.value = 'Идет процесс...'
        page.update()
        url = 'http://gateway.amanat.systems/api/ost/set-policy'
        body = input_field_set_policy.content.value
        if len(input_field_set_policy.content.value) == 0:
            result_field_set_policy.content.value = 'Поле пустое'
            page.update()
            return
        try:
            body = json.loads(body)
            body["from"] = "Support"
        except Exception as e:
            result_field_set_policy.content.value = e
            page.update()
            return

        headers = {'Authorization': 'Bearer ' + get_auth_token(selected_partner.current)}
        resp = requests.post(url, headers=headers, json=body)

        if resp.status_code == 200:
            result = {
                'message': resp.json()['message'],
                'policy_number': resp.json()['data'][0]['policy_number_ost'],
                'file': resp.json()['data'][0]['file']
            }
            result_field_set_policy.content.value = result
            page.update()
        else:
            result_field_set_policy.content.value = resp.json()
            page.update()

    def other_page(e):
        click = e.control.data
        page.clean()

        if click == 'setPolicy':
            page.add(set_policy)
        elif click == 'delete':
            page.add(set_cancellation)
        page.update()

    def set_cancellation_method(e):
        result_field_set_cancellation.content.value = 'Идет процесс...'
        page.update()
        url = 'http://gateway.amanat.systems/api/ost/set-cancellation-contract'
        headers = {'Authorization': 'Bearer ' + get_auth_token(int(partner_field.value))}
        policy_number = input_field_set_cancellation.value
        resp = requests.post(url, headers=headers, params={'policy_number': policy_number})

        result_field_set_cancellation.content.controls[
            0].value = f'{resp.json().get('success')}\n{resp.json().get('message')}'
        page.update()


    theme = ft.IconButton(icon=ft.Icons.SUNNY, on_click=change_theme)

    input_field_set_policy = ft.Container(
        content=ft.TextField(label='Введи тело полиса', multiline=True, border_color='transparent'),
        height=600,
        width=500,
        border=ft.border.all(color="white", width=1),
        padding=ft.padding.all(10)
    )

    partner_field = ft.Row([
        ft.Text('Выбери партнера:', size=25, text_align='CENTER'),
        ft.ElevatedButton(text='Fun&Sun', width=150, height=50, bgcolor='white', on_click=set_selected_partner,
                          data=[1, 'Fun&Sun'], color='black'),
        ft.ElevatedButton(text='Kompas', width=150, height=50, bgcolor='white', on_click=set_selected_partner,
                          data=[2, 'Kompas'], color='black'),
        ft.ElevatedButton(text='JoinUp', width=150, height=50, bgcolor='white', on_click=set_selected_partner,
                          data=[3, 'JoinUp'], color='black'),
    ],

    )

    result_field_set_policy = ft.Container(
        content=ft.TextField(label='Результат', multiline=True, border_color='transparent'),
        height=600,
        width=400,
        border=ft.border.all(color="white", width=1),
        padding=ft.padding.all(10)
    )

    click_button_set_policy = ft.ElevatedButton(text='Обработать', on_click=set_policy_method, height=50, width=200,
                                                bgcolor='blue')

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()
        if index == 0:
            page.add(set_policy)
        elif index == 1:
            page.add(set_cancellation)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EDIT_DOCUMENT, label='Set Policy'),
            ft.NavigationBarDestination(icon=ft.Icons.DELETE, label='Set Cancellation'),
        ], on_change=navigate
    )

    input_field_set_cancellation = ft.TextField(label='Введи номер полиса', multiline=True, border_color='white',
                                                width=500)
    result_field_set_cancellation = ft.Container(
        content=ft.Column(
            [
                ft.Text('Результат')
            ],
            scroll=ft.ScrollMode.ALWAYS
        ),
        height=300,
        width=500,
        border=ft.border.all(color="white", width=1),
        padding=ft.padding.all(10)
    )

    click_button_set_cancellation = ft.ElevatedButton(
        text='Destroy The Policy!!',
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=40)),
        on_click=set_cancellation_method,
        width=500,
        height=200,
        bgcolor='blue',
        color='red'
    )

    set_policy = ft.Column(
        [
            theme,
            partner_field,
            ft.Row(
                [
                    input_field_set_policy,
                    click_button_set_policy,
                    result_field_set_policy

                ]
            )
        ]
    )

    set_cancellation = ft.Column(
        [
            theme,
            partner_field,
            ft.Row(
                [
                    input_field_set_cancellation
                ]
            ),
            result_field_set_cancellation,
            click_button_set_cancellation
        ]
    )
    page.add(set_policy)


ft.app(target=main)
