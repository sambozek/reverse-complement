from distutils.log import debug
import dash
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([

    dcc.Textarea(
        id='fasta-DNA-input',
        value=""">Test1 
ACCAGTGCCGGACTTAACCGCGTTCACAACAGCCTTGTCCGCTTATGCCCAGGAGACAGT
AGTGATTGGCACCAAAGGGAAAGTCTAGAATTACCGCTAAGTCGTCCGAAGTCCGGGCAC
GATCCTCTACTAGTATACGCACCCTGCGGTAATACTAGGAAACTAAGGTGGTTTACACCG
CGAAACCAGTCCTACAGGACCCCTGCTTCCCCTCATGCGTATTCGTTGGCAGTTGTTTAT
AGGCCCTGGGAGCCTCAACTGCTAACCTGGTGCTCAAGTCAAATCGAGTATCCCAGGAGA
GCATCTTGACGAACCTTAGTGTATCAGGAATCTGGTAAAAATTAGGCCGGGGTAGTAGAG
CGGGCGGGCGTAGGACCAGATTCGCATCCGCTGTTGGCAAGGGATGAGGCTTTTATTTGG
CATAGCTGAGATATGTCGCTTGTGGCACTAGACACAATCCTACGAGTCCGGACAGCAGGG
ATGTGTGATGCCCGATCACTGATTCCTGGCGCATAACGCCACCTTATTTCGCCCTTCTCC
CGGGTTCAGGAATAGGGGGTTTTCATATCTCGGCAGGCATATGAACTCTAGCCTTATATA
ACCGAAAGTAAATCGACGGATGAAAAGCGGTCCCGATATTCTGGGCCGCTACACTAGCTA
TTCTCGCCTACGAATTGTTGGAACGTCCAAGTACTTCTATAAGAGAAGCTCTTTCTGGCT
GCAAACGTCTCCGTAACCGGTACTCGAACGCTTACCAGCCGCCATCCGTCTTCCATTGGG
TTAAGAGTTGAGTCTCCCCCATTTAA
        """,
        style={'width': '75%', 'height': 300},
    ),
    html.Div(id='reverse-complement',
             style={'whiteSpace': 'pre-line', 'wrap': True})

])


@app.callback(
    Output('reverse-complement', 'children'),
    Input('fasta-DNA-input', 'value')
)
def reverse_complement(value):
    return value


if __name__ == '__main__':
    app.run_server(debug=True)