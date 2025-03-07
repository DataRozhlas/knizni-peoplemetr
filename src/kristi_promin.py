def kristi_promin():

    # Naimportuje do altairu +- styl grafů na iRozhlasu.

    return {
        "config" : {
            "title": {'font': "Noticia Text",
                    'fontSize': 12,
                    'anchor': 'start',
                    'lineHeight': 19,
                    'fontWeight': 'bolder',
                    'subtitleFont': 'Noticia Text',
                    'subtitleFontSize': 10,
#                    'subtitleFontWeight': 'lighter', # nečitelné na mobilu
                    'subtitlePadding': 10,
                    'dy': -10,
                    },
            "axis": {
                "labelFont": "Asap",
                "titleFont": "Asap",
                "fontWeight": "lighter",
                "titleFontWeight": "lighter",
                "labelFontSize": 8,
                "titleFontSize": 8,
                'labelPadding': 2,
                'titlePadding': 8,
                'domainOpacity': 0,
                'tickColor': '#DCDDD6',
            },
            "legend": {
                "labelFont": "Asap",
                "labelFontWeight": "normal",
                "titleFont": "Asap",
                "titleFontWeight": "normal",
                "labelFontSize": 8,
                "titleFontSize": 8
            }
        }
    }