# Simulator

Explaination about how the simulator works

## Model

We model the state of the emergency room with:

1. Patients in wait queue: a priority queue based on the emergency code (codice rosso/giallo/verde) and time of arrival
2. Patients in terapy: patients currently being cured by doctors

Each patient, at their arrival, has been assigned a emergency code and a particular probability density function of their estimate terapy time (without empirical data, we suppose they are all truncated gaussians)

For each emergency code we model the inter-arrival of new patients as a exponential distribution with a different rate parameter.

## Simulation

The simulation consist in the repetition of an iteration algorithm until all the patients that were originally in the waiting queue are moved in therapy.

### Iteration

1. Find minimum sample between therapy and inter-arrive
2. Update current_time based on the minimum value
3.  If minimum is therapy, move a patient from the waiting queue
        to therapy (if the patient is real, add them to the self.result_dict
        and increment moved_in_therapy_patients)
    If the minimum is inter-arrive, add a new patient (fake aka ID=-1) to the waiting_queue
4. Update timing for each value in the waiting_queues, therapy_state, and leave_time
5. Goto 1

## Simulation results

The result of the simulation are then aggregated in the following structure:

```json
{
  "patient_id_1": {
    "1": 5, /* 'Patient 1' waited 1 unit of time for 5 times */
    "2": 3, /* 'Patient 1' waited 2 units of time for 3 times */
    "5": 1,
    "7": 1
  },
  "patient_id_2": {
    "1": 2,
    "2": 1,
    "3": 3,
    "4": 1,
    "5": 1,
    "6": 1,
    "9": 1
  }
  /* [...] */
}
```