import { Router, Request, Response } from 'express'
import { simulationModel } from '../../models/simulation'
import { esteemModel } from '../../models/esteem'
import { getLatestSimulationId } from '../../utils/simulation'

const patientRoutes = Router()

patientRoutes.get('/:patientId', async (req: Request, res: Response) => {
  const patientId = req.params.patientId

  if (!patientId) return res.sendStatus(401)

  try {
    const latestSimulationId = await getLatestSimulationId()

    const patientEsteem = await esteemModel.findOne({
      patient_id: patientId,
      simulation_id: latestSimulationId,
    })

    if (!patientEsteem)
      return res.status(404).send('Cannot find any simulation for this patient')

    return res.json(patientEsteem.waiting_times)
  } catch (error) {
    return res.sendStatus(500)
  }
})

export default patientRoutes
