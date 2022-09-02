from dash.dependencies import Input, Output
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    html.H1("Sam's Reverse Compositer for FASTA Files", style={'textAlign': 'center'}),

    html.Div("Copy And Paste Single FASTA Result for the Reverse Composite."),
    html.Div("Currently assuming only ACTG are in the DNA string"),
    html.Div("The output is updated live as the input changes provided that the input follows the correct format"),
    html.Div("Example of expected format is in the text area below:"),

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
        style={'width': '50%', 'height': 300, 'wrap': "hard"},
    ),
    html.H2(id='dna-label', style={'whiteSpace': 'pre-line', 'wrap': True}),
    html.Div(id='reverse-complement',
             style={'whiteSpace': 'pre-line', 'wrap': True})

])


def fasta_parse(fasta_text):
    """Parse the input FASTA data, if missing the 

    Args:
        fasta_text (str): Multiline file with name and info denoted by line containing '>' and followed by DNA Data afterwards
    Returns:
        pd.DataFrame: A dataframe containing the name of the data and the associated DNA string
    """
    if fasta_text.strip()[0] == '>':
        fasta_split = [fasta.split('\n', 1) for fasta in fasta_text.strip().split('>')[1:]]
        fasta_df = pd.DataFrame(fasta_split, columns=['Name', 'DNA_String'])
        return fasta_df
    else:
        return pd.DataFrame({'Name': ["Invalid"], 'DNA_String': ["Improperly Formatted FASTA input"]})


def dna_check(dna_str):
    """Check to make sure that there are no characters outside of the 
    Args:
        dna_str (str): DNA string portion from a FASTA file
    Returns:
        bool: If the DNA string has any non appropriate characters. 
    """
    nucleotides = set(['A', 'C', 'G', 'T', 'a', 'c', 'g', 't'])
    return set(dna_str.replace('\n', '')) <= nucleotides


def dna_reverse_complement(dna_str):
    """Generates the reverse complement of a dna string passed to it.
    Args:
        dna_str (str): A dna string
    Returns:
        str: the reverse complement of the input dna_str
    """
    complement = dict(zip("ACGTacgt\n", "TGCAtgca\n"))
    reverse_complement = ''.join([complement[base]
                                 for base in dna_str[::-1]])
    return reverse_complement


@app.callback(
    Output('dna-label', 'children'),
    Input('fasta-DNA-input', 'value')
)
def input_name(value):
    return ">{} Reverse Composite:".format(fasta_parse(value)['Name'][0])


@app.callback(
    Output('reverse-complement', 'children'),
    Input('fasta-DNA-input', 'value')
)
def reverse_complement(value):
    fasta_df = fasta_parse(value)
    dna_string = fasta_df['DNA_String'][0]
    if dna_check(dna_string):
        reverse_complement = dna_reverse_complement(dna_string).replace('\n', '')
        reverse_complement = '\n'.join([reverse_complement[i: i+60] for i in range(0, len(reverse_complement), 60)])
        return reverse_complement
    elif dna_string == 'Improperly Formatted FASTA input':
        return dna_string

    else:
        return "Invalid DNA String"
