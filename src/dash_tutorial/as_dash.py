# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

def dispatcher(request):
    '''
    Main function
    @param request: Request object
    '''

    app = _create_app()
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request()
        except Exception as e:
            response = app.server.make_response(app.server.handle_exception(e))
        return response.get_data()

def _create_app():
    app = dash.Dash()
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])

if __name__ == '__main__':
    app = _create_app()
    app.run_server(debug=True)