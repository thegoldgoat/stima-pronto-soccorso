# Simulator

Explaination about how the simulator works

## Model

We model the state of the emergency room with:

1. Patients in wait queue: a priority queue based on the emergency code (codice rosso/giallo/verde) and time of arrival
2. Patients in terapy: patients currently being cured by doctors

Each patient, at their arrival, has been assigned a emergency code and a particular probability density function of their estimate terapy time.

For each emergency code we model the inter-arrival of new patients as a exponential distribution with a different rate parameter.

## Simulation

TODO
