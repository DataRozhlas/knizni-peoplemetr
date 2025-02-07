def kristi_promin():

    # Naimportuje do altairu +- styl grafů na iRozhlasu.

    return {
        "config" : {
            "title": {'font': "Noticia Text",
                    'fontSize': 14,
                    'anchor': 'start',
                    'lineHeight': 21,
                    'fontWeight': 'bolder',
                    'subtitleFont': 'Noticia Text',
                    'subtitleFontSize': 12,
                    'subtitleFontWeight': 'lighter',
                    'subtitlePadding': 12,
                    'dy': -12,
                    },
            "axis": {
                "labelFont": "Asap",
                "titleFont": "Asap",
                "fontWeight": "lighter",
                "titleFontWeight": "lighter",
                "labelFontSize": 10,
                "titleFontSize": 10,
                'labelPadding': 2,
                'titlePadding': 10,
                'domainOpacity': 0,
                'tickColor': '#DCDDD6',
            },
            "legend": {
                "labelFont": "Asap",
                "labelFontWeight": "normal",
                "titleFont": "Asap",
                "titleFontWeight": "normal",
                "labelFontSize": 10,
                "titleFontSize": 10
            }
        }
    }