import { patientModel } from '../models/patient'
import { waitingPatientModel } from '../models/waiting_patient'
import { therapyPatientModel } from '../models/therapy_patient'
import { simulationModel } from '../models/simulation'
import { esteemModel } from '../models/esteem'
import { connect, disconnect } from 'mongoose'

function randomAverage() {
  return 2 + Math.floor(Math.random() * 3)
}

function randomDeviation() {
  return 1 + Math.floor(Math.random() * 2)
}

async function main() {
  let mongoClient
  try {
    console.log('Trying to connect to database...')
    mongoClient = await connect(
      process.env.DB_URI || 'mongodb://localhost:27017/stima-pronto-soccorso'
    )
    console.log('Connected to database')
  } catch (error) {
    console.error('Error while connecting to database:', error)
    process.exit(1)
  }

  console.log('Adding a fake simulation')

  const newSimulation = new simulationModel({
    simulation_time: new Date(),
  })
  await newSimulation.save()

  console.log('Adding waiting patients with their fake simulation results')
  for (let i = 0; i < 9; i++) {
    const newPatient = new patientModel()
    await newPatient.save()

    const arrival_time = new Date()
    arrival_time.setMinutes(arrival_time.getMinutes() + i)
    const waitingPatient = new waitingPatientModel({
      arrival_time: arrival_time,
      patient_id: newPatient._id,
      emergency_code: i % 3,
      average: randomAverage(),
      deviation: randomDeviation(),
    })

    await waitingPatient.save()

    const patientEsteem = new esteemModel({
      simulation_id: newSimulation._id,
      patient_id: newPatient._id,
      waiting_times: {
        0: i,
        1: i + i,
        2: i * i,
      },
    })

    await patientEsteem.save()
  }

  console.log('Adding therapy patients')
  for (let i = 0; i < 3; i++) {
    const newPatient = new patientModel()
    await newPatient.save()

    const entry_time = new Date()
    entry_time.setMinutes(entry_time.getMinutes() + i)
    const therapyPatient = new therapyPatientModel({
      patient_id: newPatient._id,
      entry_time: entry_time,
      average: randomAverage(),
      deviation: randomDeviation(),
    })

    await therapyPatient.save()
  }

  disconnect()
}

main()
