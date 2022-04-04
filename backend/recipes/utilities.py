from django.utils.translation import gettext_lazy as _
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.image('./logo/logo.png', 10, 8, 50)
        self.add_font('DejaVu', fname='./fonts/DejaVuSerif.ttf')
        self.set_font('DejaVu', '', 15)
        self.cell(80)
        self.cell(30, 10, _('Продуктовый помощник'), 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, _('Страница {}/{{nb}}')
                  .format(self.page_no()), 0, 0, "C")


def generate_pdf(data):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('DejaVu', '', 20)
    pdf.cell(200, 10, txt=_('Ваш список покупок по выбранным рецептам:'),
             ln=2, align='C')
    pdf.set_font('DejaVu', '', 16)
    pdf.cell(200, 10, txt='', ln=2, align='L')
    for i, item in enumerate(data):
        item_str = (f'{i + 1}. {item.name} - {item.total_amount}'
                    f' {item.measurement_unit.name}')
        pdf.cell(200, 10, txt=item_str, ln=2, align='L')
    return pdf
