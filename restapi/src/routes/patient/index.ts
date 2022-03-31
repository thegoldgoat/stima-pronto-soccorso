import { Router, Request, Response } from 'express'

const patientRoutes = Router()

patientRoutes.get('/:patientId', async (req: Request, res: Response) => {
  const patientId = req.params.patientId

  if (!patientId) return res.sendStatus(401)

  res.send('Test')
})

export default patientRoutes
