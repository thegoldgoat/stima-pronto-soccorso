import { Schema, model } from 'mongoose'

interface Simulation {
  simulation_time: Date
}

const simulationSchema = new Schema<Simulation>(
  {
    simulation_time: {
      type: Schema.Types.Date,
      required: true,
    },
  },
  {
    collection: 'simulation_model',
    versionKey: false,
  }
)

const simulationModel = model('simulation', simulationSchema)

export { simulationSchema, simulationModel, Simulation }
