import { Schema, model, ObjectId } from 'mongoose'

interface Esteem {
  patient_id: ObjectId

  simulation_id: ObjectId

  waiting_times: Object
}

const esteemSchema = new Schema<Esteem>({
  patient_id: {
    type: Schema.Types.ObjectId,
    ref: 'patients',
    required: true,
  },
  simulation_id: {
    type: Schema.Types.ObjectId,
    ref: 'simulations',
    required: true,
  },
  waiting_times: {
    type: Schema.Types.Map,
    required: true,
  },
})

const esteemModel = model('esteem', esteemSchema)

export { esteemSchema, esteemModel, Esteem }
