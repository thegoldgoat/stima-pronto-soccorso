import { Router, Request, Response } from 'express'
import { esteemModel } from '../../models/esteem'
import { waitingPatientModel } from '../../models/waiting_patient'
import { getLatestSimulationId } from '../../utils/simulation'

const monitorRoutes = Router()

monitorRoutes.use(async (req: Request, res: Response, next) => {
  // TODO: Security (?) Only the monitors can access
  next()
})

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

  return res.json(latestEsteems)
})

export default monitorRoutes
