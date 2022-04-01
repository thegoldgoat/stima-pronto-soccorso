import { simulationModel } from '../models/simulation'

async function getLatestSimulationId() {
  const latestSimulation = await simulationModel.find().limit(1).sort({
    simulation_time: -1,
  })

  if (!latestSimulation || latestSimulation.length === 0)
    throw new Error('No simulation found')

  return latestSimulation[0]._id
}

export { getLatestSimulationId }
