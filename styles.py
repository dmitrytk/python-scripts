from openpyxl.styles import Border, Side, Alignment, Font, NamedStyle

font_basic = Font(name='Times New Roman',
                  size=10,
                  bold=False,
                  italic=False,
                  vertAlign=None,
                  underline='none',
                  strike=False,
                  color='FF000000')

font_bold = Font(name='Times New Roman',
                 size=10,
                 bold=True,
                 italic=False,
                 vertAlign=None,
                 underline='none',
                 strike=False,
                 color='FF000000')

alignment_center = Alignment(horizontal='center',
                             vertical='center',
                             text_rotation=0,
                             wrap_text=False,
                             shrink_to_fit=False,
                             indent=0)

thin = Side(border_style="thin", color="000000")
border = Border(top=thin, left=thin, right=thin, bottom=thin)

style_basic = NamedStyle(name="basic")
style_basic.font = font_basic
style_basic.border = border
style_basic.alignment = alignment_center

style_bold = NamedStyle(name="bold")
style_bold.font = font_bold
style_bold.border = border
style_bold.alignment = alignment_center
