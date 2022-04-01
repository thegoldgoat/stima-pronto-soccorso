import { Schema, model, ObjectId } from 'mongoose'

interface TherapyPatient {
  patient_id: ObjectId

  entry_time: Date

  average: Number
  deviation: Number
}

const therapyPatientSchema = new Schema<TherapyPatient>(
  {
    patient_id: {
      type: Schema.Types.ObjectId,
      ref: 'patients',
      required: true,
    },
    entry_time: {
      type: Schema.Types.Date,
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
    collection: 'therapy_patient_model',
  }
)

const therapyPatientModel = model('therapy', therapyPatientSchema)

export { therapyPatientModel, therapyPatientSchema, TherapyPatient }
