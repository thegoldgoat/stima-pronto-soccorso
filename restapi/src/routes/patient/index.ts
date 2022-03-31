import { Router, Request, Response } from 'express'
import { simulationModel } from '../../models/simulation'
import { esteemModel } from '../../models/esteem'

const patientRoutes = Router()

patientRoutes.get('/:patientId', async (req: Request, res: Response) => {
  const patientId = req.params.patientId

  if (!patientId) return res.sendStatus(401)

  const latestSimulation = await simulationModel.find().limit(1).sort({
    simulation_time: -1,
  })

  if (!latestSimulation || latestSimulation.length === 0)
    return res.status(404).send('No simulation found')

  const patientEsteem = await esteemModel.findOne({
    patient_id: patientId,
    simulation_id: latestSimulation[0]._id,
  })

  if (!patientEsteem)
    return res.status(404).send('Cannot find any simulation for this patient')

  return res.json(patientEsteem.waiting_times)
})

export default patientRoutes
