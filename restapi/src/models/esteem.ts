import { Schema, model, ObjectId } from 'mongoose'

export type WaitingTimesType = Map<string, number>

export interface Esteem {
  patient_id: ObjectId

  simulation_id: ObjectId

  waiting_times: WaitingTimesType
}

export const esteemSchema = new Schema<Esteem>(
  {
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
  },
  {
    collection: 'esteem_model',
    versionKey: false,
  }
)

export const esteemModel = model('esteem', esteemSchema)
