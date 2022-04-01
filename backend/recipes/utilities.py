from fpdf import FPDF


def generate_pdf(data):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font('DejaVu', fname='fonts/DejaVuSerif.ttf')
    pdf.set_font('DejaVu', '', 20)
    pdf.cell(200, 10, txt='FoodStoGram',
             ln=1, align='C')
    pdf.cell(200, 10, txt='Ваш список покупок по выбранным рецептам:',
             ln=2, align='C')
    pdf.set_font('DejaVu', '', 16)
    pdf.cell(200, 10, txt='', ln=2, align='L')
    for i, item in enumerate(data):
        item_str = (f'{i + 1}. {item.name} - {item.total_amount}'
                    f' {item.measurement_unit.name}')
        pdf.cell(200, 10, txt=item_str, ln=2, align='L')
    return pdf
