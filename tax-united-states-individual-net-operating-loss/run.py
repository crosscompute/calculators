import json
from os import getenv
from pathlib import Path


input_folder = Path(getenv(
    'CROSSCOMPUTE_INPUT_FOLDER', 'tests/standard/input'))
output_folder = Path(getenv(
    'CROSSCOMPUTE_OUTPUT_FOLDER', 'tests/standard/output'))
output_folder.mkdir(parents=True, exist_ok=True)
with (input_folder / 'variables.dictionary').open('rt') as f:
    d = json.load(f)


adjusted_gross_income = d[
    'adjusted_gross_income']
standard_or_itemized_deductions = d[
    'standard_or_itemized_deductions']
non_business_capital_losses_before_limitation = d[
    'non_business_capital_losses_before_limitation']
non_business_capital_gains_before_exclusion = d[
    'non_business_capital_gains_before_exclusion']
non_business_deductions = d[
    'non_business_deductions']
non_business_income_other_than_capital_gains = d[
    'non_business_income_other_than_capital_gains']
business_capital_losses_before_limitation = d[
    'business_capital_losses_before_limitation']
business_capital_gains_before_exclusion = d[
    'business_capital_gains_before_exclusion']
schedule_d_loss_line_16 = d[
    'schedule_d_loss_line_16']
schedule_d_loss_line_21 = d[
    'schedule_d_loss_line_21']
section_1202_exclusion = d[
    'section_1202_exclusion']
nol_deduction_for_losses_from_other_years = d[
    'nol_deduction_for_losses_from_other_years']


line1 = adjusted_gross_income - standard_or_itemized_deductions
line2 = abs(non_business_capital_losses_before_limitation)
line3 = non_business_capital_gains_before_exclusion
line4 = line2 - line3 if line2 > line3 else 0
line5 = line3 - line2 if line3 > line2 else 0
line6 = non_business_deductions
line7 = non_business_income_other_than_capital_gains
line8 = line5 + line7
line9 = line6 - line8 if line6 > line8 else 0
line10 = line8 - line6 if line8 > line6 else 0
if line10 > line5:
    line10 = line5
line11 = abs(business_capital_losses_before_limitation)
line12 = business_capital_gains_before_exclusion
line13 = line10 + line12
line14 = line11 - line13
if line14 < 0:
    line14 = 0
line15 = line4 + line14
line16 = abs(schedule_d_loss_line_16)
if line16:
    line17 = abs(section_1202_exclusion)
    line18 = line16 - line17
    if line18 < 0:
        line18 = 0
    line19 = abs(schedule_d_loss_line_21)
    line20 = line18 - line19 if line18 > line19 else 0
    line21 = line19 - line18 if line19 > line18 else 0
    line22 = line15 - line20
    if line22 < 0:
        line22 = 0
else:
    line17 = 0
    line18 = 0
    line19 = 0
    line20 = 0
    line21 = 0
    line22 = line15
line23 = abs(nol_deduction_for_losses_from_other_years)
line24 = line1 + line9 + line17 + line21 + line23
if line24 >= 0:
    line24 = 0


with (output_folder / 'variables.dictionary').open('wt') as f:
    json.dump({
        'line1': line1,
        'line2': line2,
        'line3': line3,
        'line4': line4,
        'line5': line5,
        'line6': line6,
        'line7': line7,
        'line8': line8,
        'line9': line9,
        'line10': line10,
        'line11': line11,
        'line12': line12,
        'line13': line13,
        'line14': line14,
        'line15': line15,
        'line16': line16,
        'line17': line17,
        'line18': line18,
        'line19': line19,
        'line20': line20,
        'line21': line21,
        'line22': line22,
        'line23': line23,
        'net_operating_loss': line24,
    }, f)
