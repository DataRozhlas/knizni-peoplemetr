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
                    'subtitleLineHeight': 15,
#                    'subtitleFontWeight': 'lighter', # nečitelné na mobilu
                    'subtitlePadding': 10,
                    'dy': -10,
                    },
            "axis": {
                "labelFont": "Asap",
                "titleFont": "Asap",
                "fontWeight": "lighter",
                "titleFontWeight": "lighter",
                "labelFontSize": 9,
                "titleFontSize": 9,
                'labelPadding': 2,
                'titlePadding': 9,
                'domainOpacity': 0,
                'tickColor': '#DCDDD6',
            },
            "legend": {
                "labelFont": "Asap",
                "labelFontWeight": "normal",
                "titleFont": "Asap",
                "titleFontWeight": "normal",
                "labelFontSize": 9,
                "titleFontSize": 9
            }
        }
    }