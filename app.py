from distutils.log import debug
import dash
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    html.H2(id='dna-label', style={'whiteSpace': 'pre-line', 'wrap': True}),
    html.Div(id='reverse-complement',
             style={'whiteSpace': 'pre-line', 'wrap': True})

])

def fasta_parse(fasta_text):
    """Parse the input FASTA data

    Args:
        fasta_text (str): Multiline file with name and info denoted by line containing '>' and followed by DNA Data afterwards
    Returns:
        pd.DataFrame: A dataframe containing the name of the data and the associated DNA string
    """    
    fasta_split = [fasta.split('\n',1) for fasta in fasta_text.strip().split('>')[1:]]
    fasta_df = pd.DataFrame(fasta_split, columns=['Name', 'DNA_String'])
    return fasta_df

def dna_check(dna_str):
    """Check to make sure that there are no characters outside of the 
    Args:
        dna_str (str): DNA string portion from a FASTA file
    Returns:
        bool: If the DNA string has any non appropriate characters. 
    """
    nucleotides = set(['A', 'C', 'G', 'T', 'a', 'c', 'g', 't'])
    return set(dna_str.replace('\n', '')) <= nucleotides


@app.callback(
    Output('dna-label', 'children'),
    Input('fasta-DNA-input', 'value')
)
def input_name(value):
    return "Reverse Composite for {}:".format(fasta_parse(value)['Name'][0])


@app.callback(
    Output('reverse-complement', 'children'),
    Input('fasta-DNA-input', 'value')
)
def reverse_complement(value):
    fasta_df = fasta_parse(value)
    if dna_check(fasta_df['DNA_String'][0]):
        return fasta_df['DNA_String'][0]

    else:
        return "Not Valid DNA String"


if __name__ == '__main__':
    app.run_server(debug=True)