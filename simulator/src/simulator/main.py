from datetime import datetime, timedelta
from calendar import monthrange
import logging

from src.common.Models.month_arrivals_model import MonthArrivalsModel
from src.common.Models.hour_arrivals_model import HourArrivalsModel
from src.common.week_time import WeekTime
from src.simulator.generators.gauss_generator import GaussGenerator
from src.simulator.generators.exponential_generator import ExponentialGenerator
from src.simulator.generators.exponential_generator_time_variant import ExponentialGeneratorTimeVariant
from src.common.Rates.exponential_rate import ExponentialRate
from src.common.patient import Patient
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.EsiCodes.esi_constants import ESI_CODES
from src.common.logging.logger import createLogginWithName
from src.simulator.simulation_manager import SimulationManager

import mongoengine
from src.common.Models.waiting_patient_model import WaitingPatientModel
from src.common.Models.therapy_patient_model import TherapyPatientModel
import math

logger = createLogginWithName('Main', logging.INFO)

N = 1000000
NUM_OF_MONTHS = 12
NUM_OF_MONTHS_DATABASE = 40
NUM_OF_DAYS_IN_WEEK = 7
NUM_OF_HOUR_BINS = 6
MINUTES_IN_HOUR_BIN = 240
START_DATE_DATABASE = datetime(2014, 3, 1)
END_DATE_DATABASE = datetime(2017, 7, 1)


def normalizeTime(time: datetime):
    delta = time - datetime.now()
    return math.ceil(delta.total_seconds()/60)

def from_hour_bin_to_starting_and_ending_hours(hour_bin: str):
    '''
        Converts the hour bin in the database to a list with starting and ending hours.
    '''
    
    hours = hour_bin.split("-")
    return [int(hour) for hour in hours]

def average_num_days_of_week_in_month_between_dates(start_date, end_date):
    '''
        Gets the average number of week_day per month over the period start_date - end_date.
        start_date and end_date must be datetime objects with year != 0, month != 0 and day = 1.
    '''
    
    delta = timedelta(days=1)
    dict_days_of_the_week = {}
    
    while start_date < end_date:
        if start_date.weekday() not in dict_days_of_the_week.keys():
            dict_days_of_the_week[start_date.weekday()] = 1
        else:
            dict_days_of_the_week[start_date.weekday()] += 1
        start_date += delta
    
    for key in dict_days_of_the_week.keys():
        dict_days_of_the_week[key] /= NUM_OF_MONTHS_DATABASE
    
    return dict_days_of_the_week

def generate_exponential_generators_time_variant():
    
    '''
        Returns the exponential generators for the current month. The generators are used to determine interarrival times.
    '''
    
    # Get current month and days in current month
    current_date = datetime.now()
    current_month = current_date.month
    days_in_current_month = monthrange(current_date.year, current_date.month)[1]
    
    # Get arrivals for current_month from the database
    monthly_arrivals = {}
    for month_arrivals in MonthArrivalsModel.objects(month=current_month):
        monthly_arrivals[month_arrivals.emergency_code] = month_arrivals.arrivals
    
    # Calculate for each day of the week the average number of occurrencies per month over the period covered by the database
    dict_average_days_of_the_week_per_month = average_num_days_of_week_in_month_between_dates(START_DATE_DATABASE, END_DATE_DATABASE)
    
    # For each esi get arrivals divided by day of the week and hour bin with respet to the average
    # Determine the rates of the exponential for each hour bin of the month (hour bin 03-06 of the first monday
    # of the week is different from the hour bin 03-06 of the second monday of the week)
    list_of_exponential_generators_time_variant = []
    for esi in ESI_CODES:
        
        list_of_exponential_rates = []
        
        for hour_bin_arrivals in HourArrivalsModel.objects(emergency_code=esi):
            
            # Calculate the average number of arrivals per minute in hour bin as 
            
            #                               monthly_arrivals                                     arrivals_compared_to_average
            #                      ______________________________________________ + _____________________________________________________________
            #                     num_of_days_in_current_month * num_of_hour_bins   num_of_months_in_database * average_days_of_the_week_per_month
            #                  _______________________________________________________________________________________________________________________
            #                                                         number_of_minutes_per_hour_bin
            #
            # The average_days_of_the_week_per_month is referred to the same week day of arrivals_compared_to_average
            
            mean = (monthly_arrivals[esi]/(days_in_current_month*NUM_OF_HOUR_BINS)
                    + float(hour_bin_arrivals.arrivals_compared_to_average)/(NUM_OF_MONTHS_DATABASE*dict_average_days_of_the_week_per_month[hour_bin_arrivals.day_in_week - 1]))/MINUTES_IN_HOUR_BIN
            hour_bin = from_hour_bin_to_starting_and_ending_hours(hour_bin_arrivals.hours_interval)
            # Create exponential rate 
            list_of_exponential_rates.append(ExponentialRate(1/mean, WeekTime(hour_bin_arrivals.day_in_week - 1, hour_bin[0], 0), WeekTime(hour_bin_arrivals.day_in_week - 1, hour_bin[1], 0)))

        # Order the list of rates by weekday and starting hour
        list_of_exponential_rates.sort(key=lambda x: (x.time_begin.weekday, x.time_begin.hour))
        # Add rate to list of exponential_generators 
        list_of_exponential_generators_time_variant.append(ExponentialGeneratorTimeVariant(list_of_exponential_rates))
    
    return list_of_exponential_generators_time_variant

def main():
    mongoengine.connect("stima-pronto-soccorso")
    waiting_queues = WaitingQueue(len(ESI_CODES))

    for waiting_patient in WaitingPatientModel.objects:
        waiting_queues.push(
            Patient(
                str(waiting_patient.patient_id.pk),
                GaussGenerator(waiting_patient.average,
                               waiting_patient.deviation),
                # TODO get from db when implemented in the model
                ExponentialGenerator(1),
                waiting_patient.emergency_code,
                normalizeTime(waiting_patient.arrival_time)
            )
        )

    logger.info("Loaded {} patients in waiting queue".format(
        waiting_queues.get_patients_count()))

    therapy_patients_list = []
    # Add the patient currently in therapy_queue

    for therapy_patient in TherapyPatientModel.objects:
        therapy_patients_list.append(
            Patient(
                str(therapy_patient.pk),
                GaussGenerator(therapy_patient.average,
                               therapy_patient.deviation),
                # TODO get from db when implemented in the model
                ExponentialGenerator(1),
                None,
                normalizeTime(therapy_patient.entry_time)
            )
        )

    logger.info("Loaded {} patients in therapy state".format(
        len(therapy_patients_list)))
    
    # Create exponential generators for interarrival times and pass it to simulator manager
    exponential_generators_time_variant = generate_exponential_generators_time_variant()

    simulation_manager = SimulationManager(
        waiting_queues, therapy_patients_list, N, exponential_generators_time_variant)
    simulation_manager.run_all_simulation_sync()
    simulation_manager.plot_all()
    simulation_manager.store_all()


if __name__ == '__main__':
    main()