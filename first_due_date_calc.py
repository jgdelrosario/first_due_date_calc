import datetime
from dateutil.relativedelta import relativedelta
import calendar

## setup (change values here to your liking)
SALARY_COMPANY_CONFIG = {
    1 : { # MONTHLY
        'company_name': 'ONETOOL SOLUTIONS INC.',
        'first_ded_date': 10,
        'second_ded_date': 10,
        'collection_gper': 6,
        'billing_date': 2,
        'lpt_payment_frequency': 1,
        'lpt_payment_unit': 'monthly',
    },
    2 : { # BIMONTHLY
        'company_name': 'MANOK KO PO, INC.',
        'first_ded_date': 15,
        'second_ded_date': 30,
        'collection_gper': 5,
        'billing_date': False,
        'lpt_payment_frequency': 2,
        'lpt_payment_unit': 'bimonthly',
    }
}

PAYMENT_UNITS = {
    'monthly': 'monthly', 
    'bimonthly': 'bimonthly'
}

## calculate first due date
def _get_first_due_date(date_today, salary_company_config):
    today = datetime.datetime.strptime(date_today, '%m/%d/%Y')
    first_due_date = False
    available_days = _get_available_days(salary_company_config) # step 1: get available days
    
    # step 2: get first due date, depends if monthly, bimonthly
    if salary_company_config['lpt_payment_unit'] == PAYMENT_UNITS['monthly']:
        first_due_date = _get_first_due_date_monthly(today, available_days, salary_company_config)
    elif salary_company_config['lpt_payment_unit'] == PAYMENT_UNITS['bimonthly']:
        first_due_date = _get_first_due_date_bimonthly(today, available_days)
    
    return first_due_date

# other functions
def _get_first_due_date_monthly(due_date, available_days, salary_company_config):
    first_ded_date = _get_first_ded_date(due_date, salary_company_config)
    first_due_date = first_ded_date.replace(day=available_days[0])

    billing_date = _get_billing_date(first_ded_date)
    if due_date >= billing_date: # need to add 1 cutoff because due_date is not covered within billing date
        first_due_date += relativedelta(months=1)

    return first_due_date

def _get_first_ded_date(due_date, salary_company_config):
    due_day = due_date.day # 30
    first_ded_day = salary_company_config['first_ded_date']

    if due_day > first_ded_day: # go to next month if cannot insert to curr month
        due_date += relativedelta(months=1)

    due_date = due_date.replace(day=first_ded_day)
    return due_date


# monthly ONLY! bimonthly does not have concept of this yet
def _get_billing_date(first_ded_date):
    BILLING_DATE_FORMULA = 8 # 8 days BEFORE payroll date of company. (acdg to SAL/Ms Mao)
    first_billing_date = first_ded_date - relativedelta(days=BILLING_DATE_FORMULA)
    
    billing_end_of_month = calendar.monthrange(first_billing_date.year, first_billing_date.month)[1] 
    did_month_reduced = True if first_ded_date.month != first_billing_date.month else False # needed when first_ded is decreased with 8 days and month changed.

    if billing_end_of_month == 31 and did_month_reduced == True:
        first_billing_date -= relativedelta(days=1) # SAL: does not consider Day 31 in months that has them.

    # return datetime.datetime.strftime(first_billing_date, '%m/%d/%Y')
    return first_billing_date


## _get_first_due_date_bimonthly - check the date today then adds 1 month, 
## then gets nearest collection date (basically getting the THIRD cutoff) 
def _get_first_due_date_bimonthly(due_date, available_days):
    due_date = due_date + relativedelta(months=1)
    due_day = due_date.day
    due_month = due_date.month
    due_year = due_date.year

    end_of_months = [28, 29, 30]
    standard_end_of_month = 30
    
    if due_day == available_days[0] \
            or due_day not in available_days and due_day > available_days[0] and due_day < available_days[1]:
        new_due_day = available_days[1]

    if due_day == available_days[1] \
            or due_day not in available_days and (due_day < available_days[0] or due_day > available_days[1]):
        new_due_day = available_days[0]

    if due_day >= available_days[1]:
        due_date += relativedelta(months=1)

    if available_days[1] == standard_end_of_month and new_due_day in end_of_months:
        new_due_day = calendar.monthrange(due_year, due_month)[1] # auto adjusts if leap year
        new_due_day = standard_end_of_month if new_due_day not in end_of_months else new_due_day

    due_date = due_date.replace(day=new_due_day)
    return due_date

## get_available_days - gets dates when TGLFC will collect money from company.
def _get_available_days(salary_company_config):
    first_ded = salary_company_config['first_ded_date']
    second_ded = salary_company_config['second_ded_date']
    collection_gper = salary_company_config['collection_gper']
    divisibility_by = 30 

    first_ded_date = (first_ded + collection_gper) % divisibility_by # i.e (15 + 5) % 30 = 20 % 30 = 20
    second_ded_date = (second_ded + collection_gper) % divisibility_by # i.e (30 + 5) % 30 = 35 % 30 = 5

    standard_end_of_month = 30
    first_ded_date = standard_end_of_month if first_ded_date == 0 else first_ded_date
    second_ded_date = standard_end_of_month if second_ded_date == 0 else second_ded_date
    available_days = [first_ded_date, second_ded_date] # [20, 5]
    available_days.sort() # [5, 20]

    return available_days

def print_config(example_num):
    print("==========  " + str(example_num) + "  ==========")
    print("[Company Name]: " + salary_company_config['company_name'])
    print("[Payment Frequency]: {}, [Payment Unit]: {}".format(salary_company_config['lpt_payment_frequency'], salary_company_config['lpt_payment_unit']) )
    print("[First Ded Date]: {}, [Second Ded Date]: {}".format(salary_company_config['first_ded_date'], salary_company_config['second_ded_date']))
    print("[Collection GPER]: {}".format(salary_company_config['collection_gper']))
    print("[Billing Date]: {}\n".format(salary_company_config['billing_date']))
    print("Date Today: " + date_today)

    if choice == 1:
        print("Expected answer for monthly is: " + repr(expected_first_due_date_answer))
    else: print("Expected answer for bimonthly is: " + repr(expected_first_due_date_answer))

    print("Actual result: " + repr(first_due_date) +"\n\n" )

## (Manually SET your values and expectations here)
date_format = '%m/%d/%Y'

### EXAMPLE 1
date_today = '10/02/2022'
expected_first_due_date_answer = '11/16/2022' #
choice = 1  # change here 1 (monthly) or 2 (bimonthly)
salary_company_config = SALARY_COMPANY_CONFIG[choice]
first_due_date = _get_first_due_date(date_today, salary_company_config)
first_due_date = datetime.datetime.strftime(first_due_date, date_format)
print_config(1)

### EXAMPLE 2
date_today = '09/30/2022'
expected_first_due_date_answer = '11/05/2022'
choice = 2  # change here 1 (monthly) or 2 (bimonthly)
salary_company_config = SALARY_COMPANY_CONFIG[choice]
first_due_date = _get_first_due_date(date_today, salary_company_config)
first_due_date = datetime.datetime.strftime(first_due_date, date_format)
print_config(2)

### EXAMPLE 3
date_today = '09/30/2022'
expected_first_due_date_answer = '10/16/2022'
choice = 1  # change here 1 (monthly) or 2 (bimonthly)
salary_company_config = SALARY_COMPANY_CONFIG[choice]
first_due_date = _get_first_due_date(date_today, salary_company_config)
first_due_date = datetime.datetime.strftime(first_due_date, date_format)
print_config(3)
