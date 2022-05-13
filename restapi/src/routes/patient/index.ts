import { Router, Request, Response } from 'express'
import { esteemModel } from '../../models/esteem'
import { getLatestSimulationId } from '../../utils/simulation'
import { waitingPatientModel } from '../../models/waiting_patient'
import { PatientEsteemAPI } from '../../types/PatientEsteemAPI'

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

    const patientData = await waitingPatientModel.findOne({
      patient_id: patientId,
    })

    if (!patientData)
      return res.status(404).send('Cannot find any data this patient')

    return res.json({
      waiting_times: patientEsteem.waiting_times,
      emergency_code: patientData.emergency_code,
      arrival_time: patientData.arrival_time,
    } as PatientEsteemAPI)
  } catch (error) {
    return res.sendStatus(500)
  }
})

export default patientRoutes
