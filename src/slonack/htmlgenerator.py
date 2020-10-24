import dominate
from dominate.tags import *


class HTMLGenerator:
    '''
    This Class instatiaties a HTML generator.

    '''
    def __init__(self, **kwargs):
        self.data = kwargs.get("data")


    def create_report(self, report_title, report_data):
        '''
        This Method creates a HTML report 
        '''
        doc = dominate.document(title=report_title, doctype='<!DOCTYPE html>')
        with doc.head:
            style('''h1{
                    color: #009879;
                    text-align: left;
                    font-family: "Comic Sans MS";
                    border-radius: 5px 5px 0 0;
                    text-align: center;
                    width: 100;
                    }
			        .table-stripped {
                    border-collapse: collapse;
                    margin: 25px 0;
                    font-size: 0.9em;
                    font-family: "Comic Sans MS";
                    min-width: 400px;
                    border-radius: 5px 5px 0 0;
                    overflow: hidden;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                    }
                .table-stripped thead tr {
                    background-color: #000009;
                    color: #ffffff;
                    text-align: left;
                    }
                .table-stripped th,
                .table-stripped td {
                    padding: 12px 15px;
                }
                .table-stripped tbody tr {
                    border-bottom: 1px solid #dddddd;
                    border-top: 2px solid #009879;
                }

                .table-stripped tbody tr:nth-of-type(even) {
                    background-color: #f3f3f3;
                }

                .table-stripped tbody tr:last-of-type {
                    border-bottom: 2px solid #009879;
                    border-top: 2px solid #009879;
                }
                .table-stripped tbody tr.active-row {
                    font-weight: bold;
                    color: #009879;
                }
                ''')
        with doc.body:
            with div(cls='container'):
                h1(report_title, syle="font-family: sans-serif;")
                with table(id='issues', cls='table-stripped'):
                    with thead():
                        th('S/N')
                        th('Associated Rule')
                        th('Component')
                        th('Message')
                        th('Issue Type')
                        th('Severity')
                        th('Line')
                        th('Estimated Effort')
                        th('Author')

                    with tbody():
                        for j in range(len(report_data)):
                            with tr():
                                td(j+1)
                                td(report_data[j].get('Associated Rule'))
                                td(report_data[j].get('Component'))
                                td(report_data[j].get('Message'))
                                td(report_data[j].get('Issue Type'))
                                td(report_data[j].get('Severity'))
                                td(report_data[j].get('Line'))
                                td(report_data[j].get('Estimated Effort'))
                                td(report_data[j].get('Author'))

        with open("report.html", "w") as f:
           print(doc, file=f)


