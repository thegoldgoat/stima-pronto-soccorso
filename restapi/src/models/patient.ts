import { Schema, model } from 'mongoose'

interface Patient {}

const patientSchema = new Schema<Patient>(
  {},
  { collection: 'patient_model', versionKey: false }
)

const patientModel = model('patient', patientSchema)

export { patientSchema, patientModel, Patient }
