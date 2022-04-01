import { Router, Request, Response } from 'express'
import { Esteem, esteemModel } from '../../models/esteem'
import { waitingPatientModel } from '../../models/waiting_patient'
import { getLatestSimulationId } from '../../utils/simulation'

const monitorRoutes = Router()

monitorRoutes.use(async (req: Request, res: Response, next) => {
  // TODO: Security (?) Only the monitors can access
  next()
})

type PatientEsteem = Esteem & { emergency_code: Number; arrival_time: Date }

async function populatePatientId(esteem: PatientEsteem) {
  console.debug('esteem before', esteem)

  const waitingPatient = await waitingPatientModel.findOne(
    { patient_id: esteem.patient_id },
    { _id: 0, emergency_code: 1, arrival_time: 1 }
  )

  if (!waitingPatient)
    throw new Error(
      'Unable to find waiting patient for ID=' + esteem.patient_id
    )

  console.debug('waitingPatient', waitingPatient)

  esteem.emergency_code = waitingPatient.emergency_code
  esteem.arrival_time = waitingPatient.arrival_time

  // TODO: ecmascript 2019 (?)
  esteem.waiting_times = Object.fromEntries(esteem.waiting_times)

  console.debug('esteem after', esteem)
}

monitorRoutes.get('/all', async (req: Request, res: Response) => {
  let latestSimulationId
  try {
    latestSimulationId = await getLatestSimulationId()
  } catch (error) {
    return res.status(404).send('Cannot find any simulation')
  }

  const latestEsteems = await esteemModel.find(
    { simulation_id: latestSimulationId },
    { _id: 0, patient_id: 1, waiting_times: 1 }
  )

  if (!latestEsteems) return res.status(404).send('Cannot get latests esteems')

  const esteemsObject = latestEsteems.map((esteem) => esteem.toObject())

  const allPromises: Promise<void>[] = []
  esteemsObject.forEach((esteem) => {
    allPromises.push(populatePatientId(esteem as any))
  })

  await Promise.all(allPromises)

  console.debug('esteemsObject', esteemsObject)

  return res.json(esteemsObject)
})

export default monitorRoutes
