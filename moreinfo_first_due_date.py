import datetime
from dateutil.relativedelta import relativedelta
import calendar

def _get_first_due_date_monthly(due_date, available_days, salary_company_config):
    first_ded_date = _get_first_ded_date(due_date, salary_company_config)
    first_due_date = first_ded_date.replace(day=available_days[0])
    print( 'first_ded_date: ' + repr(first_ded_date) )

    billing_date = _get_billing_date(first_ded_date)
    if due_date >= billing_date: # need to add 1 cutoff because due_date is not covered within billing date
        billing_date += relativedelta(months=1)
        first_ded_date += relativedelta(months=1)
        first_due_date += relativedelta(months=1)
        print( 'first_ded_date READJUST= ADD 1mo: ' + repr(first_ded_date) )
    print( 'billing date: ' + repr(billing_date) )
    
    # Billing Date coverage (given billing_date 06/02/2022), coverage is (start 05/02/2022, end 06/01/2022)
    start_application_date = billing_date - relativedelta(months=1)
    end_application_date = billing_date - relativedelta(days=1)

    print('end_application_date: '  + repr(end_application_date) )
    print('start_application_date: '  + repr(start_application_date) )

    return first_due_date

#monthly ONLY! bimonthly does not have concept of this yet
def _get_billing_date(first_ded_date):
    BILLING_DATE_FORMULA = 8 # 8 days BEFORE payroll date of company. (acdg to SAL/Ms Mao)
    first_billing_date = first_ded_date - relativedelta(days=BILLING_DATE_FORMULA)
    
    billing_end_of_month = calendar.monthrange(first_billing_date.year, first_billing_date.month)[1] 
    did_month_reduced = True if first_ded_date.month != first_billing_date.month else False # needed when first_ded is decreased with 8 days and month changed.

    if billing_end_of_month == 31 and did_month_reduced == True:
        first_billing_date -= relativedelta(days=1) # SAL: does not consider Day 31 in months that has them.

    # return datetime.datetime.strftime(first_billing_date, '%m/%d/%Y')
    return first_billing_date

def _get_first_ded_date(due_date, salary_company_config):
    due_day = due_date.day # 30
    first_ded_day = salary_company_config['first_ded_date']

    if due_day > first_ded_day:
        due_date += relativedelta(months=1)

    due_date = due_date.replace(day=first_ded_day)
    return due_date

salary_company_config = {
    'first_ded_date': 10
}
today = datetime.datetime.strptime('10/02/2022', '%m/%d/%Y')
print('application date: ' + repr(today))
print('first_due_date: ' + repr( _get_first_due_date_monthly(today, [16, 16], salary_company_config) ) )