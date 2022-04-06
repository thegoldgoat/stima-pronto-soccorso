import { Schema, model, ObjectId } from 'mongoose'

interface WaitingPatient {
  patient_id: ObjectId

  arrival_time: Date
  emergency_code: Number

  average: Number
  deviation: Number
}

const waitingPatientSchema = new Schema<WaitingPatient>(
  {
    patient_id: {
      type: Schema.Types.ObjectId,
      ref: 'patients',
      required: true,
    },
    arrival_time: {
      type: Schema.Types.Date,
      required: true,
    },
    emergency_code: {
      type: Number,
      enum: [0, 1, 2],
      required: true,
    },
    average: {
      type: Number,
      required: true,
    },
    deviation: {
      type: Number,
      required: true,
    },
  },
  {
    collection: 'waiting_patient_model',
    versionKey: false,
  }
)

const waitingPatientModel = model('waiting', waitingPatientSchema)

export { waitingPatientModel, waitingPatientSchema, WaitingPatient }
